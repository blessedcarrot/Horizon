#!/usr/bin/env python3
"""Post-run health check for Horizon scheduled runs.

Parses the tee'd run log to distinguish "quiet run" from "broken run"
(BACKLOG #5/#6): a digest saying "no items met the threshold" reads
identically whether items scored low or every item silently failed.

Usage:
  python scripts/check_run_health.py horizon-run.log [--append-digest docs/_posts]

Effects:
  - Prints a health report; also writes it to $GITHUB_STEP_SUMMARY when set.
  - With --append-digest: appends a compact health footer to today's
    digest file(s) (docs/_posts/YYYY-MM-DD-summary-*.md).
  - Writes the error count to health_errors.txt so a later workflow step
    can fail the job AFTER the Pages deploy has published the digest.
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
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
        line = ANSI_RE.sub("", raw)
        if m := FOUND_RE.search(line):
            per_source[m.group(2)] = int(m.group(1))
        elif m := FETCHED_RE.search(line):
            totals["fetched"] = int(m.group(1))
        elif m := ANALYZED_RE.search(line):
            totals["analyzed"] = int(m.group(1))
        elif m := SELECTED_RE.search(line):
            totals["selected"] = int(m.group(1))
        if " ERROR " in line or line.lstrip().startswith("ERROR"):
            errors.append(line.strip()[:200])
        if " WARNING " in line:
            warnings += 1

    return per_source, totals, errors, warnings


def build_report(per_source, totals, errors, warnings) -> str:
    zero_sources = sorted(n for n, c in per_source.items() if c == 0)
    lines = ["## Run health", ""]
    lines.append(
        f"- **Fetched:** {totals['fetched']} | **Analyzed:** {totals['analyzed']}"
        f" | **Cleared threshold:** {totals['selected']}"
        f" | **Errors:** {len(errors)} | **Warnings:** {warnings}"
    )
    if per_source:
        counts = ", ".join(f"{n}: {c}" for n, c in sorted(per_source.items()))
        lines.append(f"- **Per-source items:** {counts}")
    if zero_sources:
        lines.append(
            f"- ⚠️ **Sources returning zero items:** {', '.join(zero_sources)}"
            " — quiet or dead? Zero across several consecutive runs means dead."
        )
    if errors:
        lines.append(
            f"- 🔴 **{len(errors)} ERROR line(s) in this run** — an empty digest"
            " may mean failures, not low scores. First errors:"
        )
        lines += [f"  - `{e}`" for e in errors[:5]]
    else:
        lines.append(
            "- ✅ **No errors** — if the digest is empty, items genuinely"
            " scored below threshold."
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("logfile", type=Path)
    ap.add_argument("--append-digest", type=Path, default=None,
                    help="posts dir; appends footer to today's summary files")
    args = ap.parse_args()

    per_source, totals, errors, warnings = parse_log(args.logfile)
    report = build_report(per_source, totals, errors, warnings)
    print(report)

    import os
    if summary_path := os.environ.get("GITHUB_STEP_SUMMARY"):
        with open(summary_path, "a", encoding="utf-8") as f:
            f.write(report)

    if args.append_digest and args.append_digest.is_dir():
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        for post in sorted(args.append_digest.glob(f"{today}-summary-*.md")):
            with open(post, "a", encoding="utf-8") as f:
                f.write("\n\n---\n\n" + report)
            print(f"Appended health footer to {post}")

    Path("health_errors.txt").write_text(str(len(errors)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
