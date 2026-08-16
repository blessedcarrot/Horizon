#!/usr/bin/env python3
"""Post-run health check for Horizon scheduled runs.

Parses the tee'd run log to distinguish "quiet run" from "broken run"
(BACKLOG #5/#6): a digest saying "no items met the threshold" reads
identically whether items scored low or every item silently failed.

Usage:
  python scripts/check_run_health.py horizon-run.log [--append-digest docs/_posts]

Effects:
  - Prints a health report; also writes it to $GITHUB_STEP_SUMMARY when set.
  - Emits GitHub workflow-command annotations (::error/::warning/::notice),
    which surface in the Annotations box at the top of the run page — the
    only surface visible without opening logs or the summary tab.
  - With --append-digest: appends a compact health footer to today's
    digest file(s) (docs/_posts/YYYY-MM-DD-summary-*.md).
  - Writes the error count to health_errors.txt so a later workflow step
    can fail the job AFTER the Pages deploy has published the digest.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
# Downloaded Actions job logs prefix every line with an ISO timestamp that raw
# stdout doesn't have. Strip it so the same script works on either, which
# matters because after-the-fact debugging uses the downloaded job log.
ISO_PREFIX_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T[\d:.]+Z\s?")
TIMESTAMP_RE = re.compile(r"^\[?\d{2}/\d{2}/\d{2}[^]]*\]?\s*")
QUOTED_RE = re.compile(r"'[^']*'|\"[^\"]*\"")
# Match ERROR/WARNING only in the log-level column (line start, or after the
# timestamp bracket, followed by the level's padding) so a story title
# containing the word "ERROR" can't fail the job. This gates the build, so a
# false positive would cry wolf and erode trust in the signal.
ERROR_RE = re.compile(r"(?:^|\])\s*ERROR\s{2,}")
WARNING_RE = re.compile(r"(?:^|\])\s*WARNING\s{2,}")
# GitHub renders ~10 annotations per level per step; group and cap below that.
MAX_ANNOTATIONS = 8
FOUND_RE = re.compile(r"Found (\d+) items? from (.+?)\s*$")
FETCHED_RE = re.compile(r"Fetched (\d+) items? from all sources")
ANALYZED_RE = re.compile(r"Analyzed (\d+) items? with AI")
SELECTED_RE = re.compile(r"Selected (\d+) items? with profile filters")


def parse_log(path: Path):
    per_source: dict[str, int] = {}
    totals = {"fetched": None, "analyzed": None, "selected": None}
    errors: list[str] = []
    warnings = 0

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = ISO_PREFIX_RE.sub("", ANSI_RE.sub("", raw))
        if m := FOUND_RE.search(line):
            per_source[m.group(2)] = int(m.group(1))
        elif m := FETCHED_RE.search(line):
            totals["fetched"] = int(m.group(1))
        elif m := ANALYZED_RE.search(line):
            totals["analyzed"] = int(m.group(1))
        elif m := SELECTED_RE.search(line):
            totals["selected"] = int(m.group(1))
        if ERROR_RE.search(line):
            errors.append(line.strip()[:200])
        if WARNING_RE.search(line):
            warnings += 1

    return per_source, totals, errors, warnings


def group_errors(errors: list[str]) -> list[tuple[str, int]]:
    """Collapse per-item errors into distinct signatures with counts.

    Analysis failures repeat once per item with only the item title varying,
    so 74 raw lines are really one problem. Grouping keeps the annotation
    list under GitHub's per-step cap and makes the real failure obvious.
    """
    groups: dict[str, int] = {}
    for line in errors:
        sig = TIMESTAMP_RE.sub("", line)
        sig = QUOTED_RE.sub("'…'", sig)
        sig = " ".join(sig.split())
        groups[sig] = groups.get(sig, 0) + 1
    return sorted(groups.items(), key=lambda kv: -kv[1])


def annotate(level: str, message: str) -> None:
    """Emit a workflow command; shows in the run page's Annotations box."""
    clean = message.replace("\r", " ").replace("\n", " ").strip()
    print(f"::{level}::{clean}")


def emit_annotations(per_source, totals, grouped, warnings) -> None:
    headline = (
        f"Radar run: {totals['fetched']} fetched, {totals['analyzed']} analyzed, "
        f"{totals['selected']} cleared threshold, "
        f"{sum(c for _, c in grouped)} errors, {warnings} warnings"
    )
    annotate("notice", headline)

    if zero := sorted(n for n, c in per_source.items() if c == 0):
        annotate(
            "warning",
            f"Sources returning zero items: {', '.join(zero)} — quiet or dead? "
            "Zero across several consecutive runs means dead.",
        )

    for sig, count in grouped[:MAX_ANNOTATIONS]:
        annotate("error", f"{count}x {sig[:300]}")
    if len(grouped) > MAX_ANNOTATIONS:
        annotate(
            "error",
            f"{len(grouped) - MAX_ANNOTATIONS} further distinct error type(s) "
            "not shown — see the run log.",
        )


def build_report(per_source, totals, grouped, warnings) -> str:
    zero_sources = sorted(n for n, c in per_source.items() if c == 0)
    error_count = sum(c for _, c in grouped)
    lines = ["## Run health", ""]
    lines.append(
        f"- **Fetched:** {totals['fetched']} | **Analyzed:** {totals['analyzed']}"
        f" | **Cleared threshold:** {totals['selected']}"
        f" | **Errors:** {error_count} | **Warnings:** {warnings}"
    )
    if per_source:
        counts = ", ".join(f"{n}: {c}" for n, c in sorted(per_source.items()))
        lines.append(f"- **Per-source items:** {counts}")
    if zero_sources:
        lines.append(
            f"- ⚠️ **Sources returning zero items:** {', '.join(zero_sources)}"
            " — quiet or dead? Zero across several consecutive runs means dead."
        )
    if grouped:
        lines.append(
            f"- 🔴 **{error_count} ERROR line(s), {len(grouped)} distinct type(s)**"
            " — an empty digest may mean failures, not low scores:"
        )
        lines += [f"  - **{count}x** `{sig[:300]}`" for sig, count in grouped]
    else:
        lines.append(
            "- ✅ **No errors** — if the digest is empty, items genuinely"
            " scored below threshold."
        )
    return "\n".join(lines) + "\n"


def todays_posts(posts_dir: Path) -> list[Path]:
    """This run's digest file(s) — the newest per language for today.

    Posts are named "<date>-<HHMM>-summary-<lang>.md" (the run time was added
    so a day's second run stops overwriting the first). Several files can
    therefore share a date, and only the one this run just wrote should get
    this run's health footer. The pre-timestamp "<date>-summary-<lang>.md"
    form is still matched so older digests aren't missed.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    newest_per_lang: dict[str, tuple[str, Path]] = {}
    for post in posts_dir.glob(f"{today}-*summary-*.md"):
        lang = post.stem.rsplit("summary-", 1)[-1]
        # Rank by the HHMM in the name, not mtime: this run wrote the latest
        # time for today, and filesystem timestamps can be reordered by
        # anything that touches the files (checkout, copy, deploy tooling).
        middle = post.stem[len(today) + 1:].rsplit("-summary-", 1)[0]
        stamp = middle if middle.isdigit() else ""  # legacy name sorts first
        if lang not in newest_per_lang or stamp > newest_per_lang[lang][0]:
            newest_per_lang[lang] = (stamp, post)
    return sorted(p for _, p in newest_per_lang.values())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", type=Path)
    ap.add_argument("--append-digest", type=Path, default=None,
                    help="posts dir; appends footer to today's summary files")
    args = ap.parse_args()

    per_source, totals, errors, warnings = parse_log(args.logfile)
    grouped = group_errors(errors)
    report = build_report(per_source, totals, grouped, warnings)
    print(report)
    emit_annotations(per_source, totals, grouped, warnings)

    import os
    if summary_path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report)

    posts: list[Path] = []
    if args.append_digest and args.append_digest.is_dir():
        posts = todays_posts(args.append_digest)
        for post in posts:
            # Digests already end with a horizontal rule; don't stack a second.
            existing = post.read_text(encoding="utf-8").rstrip()
            separator = "\n\n" if existing.endswith("---") else "\n\n---\n\n"
            with open(post, "a", encoding="utf-8") as f:
                f.write(separator + report)
            print(f"Appended health footer to {post}")

    Path("health_errors.txt").write_text(str(len(errors)), encoding="utf-8")
    # Machine-readable form for notify_telegram.py, so the notifier doesn't
    # have to re-parse the log and the two can't disagree about a run.
    Path("health_summary.json").write_text(json.dumps({
        "totals": totals,
        "per_source": per_source,
        "zero_sources": sorted(n for n, c in per_source.items() if c == 0),
        "errors": len(errors),
        "warnings": warnings,
        "posts": [str(p) for p in posts],
        "finished_utc": datetime.now(timezone.utc).strftime("%d %b %H:%M"),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
