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
    which surface in the Annotations box at the top of the run page, the
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
# Per-sub-source breakdown lines, e.g. "      • The Verge - AI: 1" or
# "      • OpenAI News: 0 (FAILED)". Only those printed during fetching are
# collected, the same format is reused later for selected items.
DETAIL_RE = re.compile(r"^\s*•\s*(?P<name>.+?):\s*(?P<count>\d+)(?P<failed>\s*\(FAILED\))?\s*$")
FETCHED_RE = re.compile(r"Fetched (\d+) items? from all sources")
ANALYZED_RE = re.compile(r"Analyzed (\d+) items? with AI")
SELECTED_RE = re.compile(r"Selected (\d+) items? with profile filters")
# The rest of the funnel. Reporting only fetched/analyzed/cleared made the
# footer contradict the page it sits on: a run that cleared 24 and published
# 17 looked like it had lost 7 items, when topic dedup had merged them.
MERGED_RE = re.compile(r"Merged (\d+) cross-source duplicates")
TOPIC_DEDUP_RE = re.compile(r"Removed (\d+) topic duplicates")
BALANCED_RE = re.compile(r"Balanced digest selected (\d+)/(\d+) items")
ENRICHED_RE = re.compile(r"Enriched (\d+)/(\d+) items")
TOKENS_RE = re.compile(
    r"Token usage this run: (\d+) tokens \(input: (\d+), output: (\d+)\)"
)
# Log records wrap when rich falls back to 80 columns, putting the item id and
# the actual cause on the lines below the one carrying the ERROR level. The
# workflow now sets COLUMNS so this should not happen, but downloaded logs from
# before that change still wrap, and a long enough message wraps at any width.
CONTINUATION_RE = re.compile(r"^\s{8,}(?![\u2022])\S")
# Item ids vary per failure and would defeat grouping once the continuation is
# joined back on. Collapse them so N failures of one kind stay one signature.
ITEM_ID_RE = re.compile(r"[\w.\-]+:[\w.\-]+:[0-9a-f]{8,}")
HASH_RE = re.compile(r"\b[0-9a-f]{12,}\b")


def parse_log(path: Path):
    per_source: dict[str, int] = {}
    per_feed: dict[str, tuple[int, bool]] = {}
    totals = {
        "fetched": None, "merged": None, "analyzed": None, "selected": None,
        "topic_dupes": None, "published": None,
        "enriched": None, "enrich_attempted": None,
        "tokens": None, "tokens_in": None, "tokens_out": None,
    }
    errors: list[str] = []
    warnings = 0
    fetching = True  # detail lines only count before fetching ends
    current_source = None
    open_error: int | None = None  # index in errors awaiting wrapped remainder

    for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = ISO_PREFIX_RE.sub("", ANSI_RE.sub("", raw))
        if m := FOUND_RE.search(line):
            current_source = m.group(2)
            per_source[current_source] = int(m.group(1))
        # Only RSS reports what it attempted, so only its breakdown can show a
        # feed that returned nothing. Other scrapers' breakdowns are derived
        # from returned items (Google News lists ~50 publishers), which would
        # bury the signal this section exists for.
        elif fetching and current_source == "RSS Feeds" and (m := DETAIL_RE.match(line)):
            per_feed[m.group("name")] = (int(m.group("count")), bool(m.group("failed")))
        elif m := FETCHED_RE.search(line):
            totals["fetched"] = int(m.group(1))
            fetching = False
        elif m := ANALYZED_RE.search(line):
            totals["analyzed"] = int(m.group(1))
        elif m := SELECTED_RE.search(line):
            totals["selected"] = int(m.group(1))
        elif m := MERGED_RE.search(line):
            totals["merged"] = int(m.group(1))
        elif m := TOPIC_DEDUP_RE.search(line):
            totals["topic_dupes"] = int(m.group(1))
        elif m := BALANCED_RE.search(line):
            totals["published"] = int(m.group(1))
        elif m := ENRICHED_RE.search(line):
            totals["enriched"] = int(m.group(1))
            totals["enrich_attempted"] = int(m.group(2))
        elif m := TOKENS_RE.search(line):
            totals["tokens"] = int(m.group(1))
            totals["tokens_in"] = int(m.group(2))
            totals["tokens_out"] = int(m.group(3))
        if ERROR_RE.search(line):
            errors.append(line.strip()[:200])
            open_error = len(errors) - 1
        elif open_error is not None and CONTINUATION_RE.match(line):
            # A wrapped remainder of the record above: the part that names the
            # item and the cause. Join it back on, capped so a stack trace
            # cannot run away with the annotation.
            errors[open_error] = (errors[open_error] + " " + line.strip())[:400]
        elif line.strip():
            open_error = None
        if WARNING_RE.search(line):
            warnings += 1

    return per_source, per_feed, totals, errors, warnings


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
        sig = ITEM_ID_RE.sub("<item>", sig)
        sig = HASH_RE.sub("<hash>", sig)
        sig = " ".join(sig.split())
        groups[sig] = groups.get(sig, 0) + 1
    return sorted(groups.items(), key=lambda kv: -kv[1])


# Errors that cost an item its depth while still publishing it. These are a
# different kind of event from a broken run, and conflating the two is how a
# build ends up permanently red: every content-producing run between
# 2026-08-17 and 2026-08-18 failed on exactly two of these, out of seventeen
# items published successfully. A red X that appears every day stops being read,
# which is the failure this whole script exists to prevent.
DEGRADING_RE = re.compile(r"Error enriching item")
# Above this share of the items that reached enrichment, a degradation is no
# longer a couple of awkward abstracts; something systemic is wrong with the
# contract or the model, and the run should go red.
DEGRADED_FATAL_SHARE = 0.25


def split_by_severity(grouped, totals):
    """Separate errors that break a run from errors that only thin an item.

    Returns (fatal, degrading, escalated). `escalated` is True when the
    degrading errors are numerous enough to be a systemic problem rather than
    a few items, in which case they count as fatal after all.
    """
    fatal = [(s, c) for s, c in grouped if not DEGRADING_RE.search(s)]
    degrading = [(s, c) for s, c in grouped if DEGRADING_RE.search(s)]

    attempted = totals.get("enrich_attempted")
    degraded_count = sum(c for _, c in degrading)
    escalated = bool(degrading) and (
        not attempted
        or totals.get("enriched") == 0
        or degraded_count / attempted > DEGRADED_FATAL_SHARE
    )
    if escalated:
        fatal = fatal + degrading
        degrading = []
    return fatal, degrading, escalated


def annotate(level: str, message: str) -> None:
    """Emit a workflow command; shows in the run page's Annotations box."""
    clean = message.replace("\r", " ").replace("\n", " ").strip()
    print(f"::{level}::{clean}")


def emit_annotations(per_source, per_feed, totals, grouped, warnings) -> None:
    headline = (
        f"Radar run: {funnel(totals).replace('**', '')}. "
        f"{sum(c for _, c in grouped)} errors, {warnings} warnings"
    )
    if totals["tokens"]:
        headline += f", {totals['tokens']:,} tokens"
    annotate("notice", headline)

    if note := enrichment_note(totals):
        annotate("warning", note.lstrip("- ").replace("**", ""))

    if zero := sorted(n for n, c in per_source.items() if c == 0):
        annotate(
            "warning",
            f"Sources returning zero items: {', '.join(zero)}. "
            "Zero across several consecutive runs means dead.",
        )

    if failed := sorted(n for n, (_, f) in (per_feed or {}).items() if f):
        # Warning, not error: Horizon logs feed failures as warnings and the job
        # stays green, so a red annotation here would contradict the job status.
        # Still louder than a zero-item feed, which may simply be quiet.
        annotate("warning", f"Feeds that FAILED to fetch: {', '.join(failed)}")

    fatal, degrading, escalated = split_by_severity(grouped, totals)
    if escalated:
        annotate(
            "error",
            "Enrichment failed on more than a quarter of the items that reached "
            "it. Treating this as a broken run, not a few thin items.",
        )
    for sig, count in fatal[:MAX_ANNOTATIONS]:
        annotate("error", f"{count}x {sig[:300]}")
    if len(fatal) > MAX_ANNOTATIONS:
        annotate(
            "error",
            f"{len(fatal) - MAX_ANNOTATIONS} further distinct error type(s) "
            "not shown. See the run log.",
        )
    # Degradation is reported at warning level so the job stays green. The
    # item published; only its depth was lost.
    for sig, count in degrading[:MAX_ANNOTATIONS]:
        annotate("warning", f"{count}x {sig[:300]}")


def funnel(totals) -> str:
    """The whole chain from raw pull to published, as one line.

    Reporting fetched, analyzed and cleared alone left the biggest drop
    invisible: a reader comparing "cleared 24" against a page of 17 items had
    no way to tell merged duplicates from lost coverage.
    """
    steps = []
    if totals["fetched"] is not None:
        steps.append(f"{totals['fetched']} fetched")
    if totals["merged"]:
        steps.append(f"{totals['merged']} cross-source duplicates merged")
    if totals["analyzed"] is not None:
        steps.append(f"{totals['analyzed']} analyzed")
    if totals["selected"] is not None:
        steps.append(f"{totals['selected']} cleared threshold")
    if totals["topic_dupes"]:
        steps.append(f"{totals['topic_dupes']} topic duplicates merged")
    if totals["published"] is not None:
        steps.append(f"**{totals['published']} published**")
    return " → ".join(steps)


def enrichment_note(totals):
    """A failed enrichment leaves the item published and thin.

    A failed second pass still publishes the headline and the summary, with no
    background and no references, and the page gives no sign. Name it, or the
    only visible effect is a red X on a run that looks otherwise complete.
    """
    done, tried = totals["enriched"], totals["enrich_attempted"]
    if done is None or tried is None or done >= tried:
        return None
    return (
        f"- ⚠️ **{tried - done} of {tried} published items lost their background"
        " section** because enrichment failed. They carry a headline and a"
        " summary only."
    )


def build_report(per_source, per_feed, totals, grouped, warnings) -> str:
    zero_sources = sorted(n for n, c in per_source.items() if c == 0)
    fatal_head, degrading_head, _ = split_by_severity(grouped, totals)
    lines = ["## Run health", ""]
    lines.append(f"- **Funnel:** {funnel(totals)}")
    # Count the two kinds separately in the headline. One number covering both
    # is what made "2 errors" sit above a page where nothing had gone missing.
    tail = f"- **Errors:** {sum(c for _, c in fatal_head)}"
    if degrading_head:
        tail += f" | **Items published thin:** {sum(c for _, c in degrading_head)}"
    tail += f" | **Warnings:** {warnings}"
    if totals["tokens"]:
        tail += (
            f" | **Tokens:** {totals['tokens']:,}"
            f" ({totals['tokens_in']:,} in / {totals['tokens_out']:,} out)"
        )
    lines.append(tail)
    if note := enrichment_note(totals):
        lines.append(note)
    if per_source:
        counts = ", ".join(f"{n}: {c}" for n, c in sorted(per_source.items()))
        lines.append(f"- **Per-source items:** {counts}")
    if zero_sources:
        lines.append(
            f"- ⚠️ **Sources returning zero items:** {', '.join(zero_sources)}"
            ". Zero across several consecutive runs means dead."
        )
    if per_feed:
        failed = sorted(n for n, (_, f) in per_feed.items() if f)
        empty = sorted(n for n, (c, f) in per_feed.items() if c == 0 and not f)
        live = sorted(((n, c) for n, (c, f) in per_feed.items() if c > 0),
                      key=lambda kv: -kv[1])
        if failed:
            lines.append(f"- 🔴 **Feeds that FAILED to fetch:** {', '.join(failed)}")
        if live:
            lines.append("- **Feeds with items:** "
                         + ", ".join(f"{n}: {c}" for n, c in live))
        if empty:
            lines.append(f"- **Feeds with nothing in window ({len(empty)}):** "
                         + ", ".join(empty))
    fatal, degrading, escalated = split_by_severity(grouped, totals)
    if escalated:
        lines.append(
            "- 🔴 **Enrichment failed on more than a quarter of the items that"
            " reached it.** That is a broken run, not a few thin items."
        )
    if fatal:
        fatal_count = sum(c for _, c in fatal)
        lines.append(
            f"- 🔴 **{fatal_count} ERROR line(s), {len(fatal)} distinct type(s)**"
            ". The digest may be incomplete:"
        )
        lines += [f"  - **{count}x** `{sig[:300]}`" for sig, count in fatal]
    if degrading:
        degraded_count = sum(c for _, c in degrading)
        lines.append(
            f"- 🟡 **{degraded_count} item(s) published without background.**"
            " Everything that cleared the bar is on the page; those items carry"
            " a headline and a summary only:"
        )
        lines += [f"  - **{count}x** `{sig[:300]}`" for sig, count in degrading]
    if not fatal and not degrading:
        lines.append(
            "- ✅ **No errors**. If the digest is empty, items scored"
            " below threshold."
        )
    return "\n".join(lines) + "\n"


def todays_posts(posts_dir: Path) -> list[Path]:
    """This run's digest file(s), the newest per language for today.

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

    per_source, per_feed, totals, errors, warnings = parse_log(args.logfile)
    grouped = group_errors(errors)
    report = build_report(per_source, per_feed, totals, grouped, warnings)
    print(report)
    emit_annotations(per_source, per_feed, totals, grouped, warnings)

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

    fatal, degrading, escalated = split_by_severity(grouped, totals)
    # Only errors that actually damage the run fail the job. Items that
    # published thin are reported and stay green, so a red X keeps meaning
    # "go and look" rather than "another Tuesday".
    fatal_count = sum(c for _, c in fatal)
    Path("health_errors.txt").write_text(str(fatal_count), encoding="utf-8")
    # Machine-readable form for notify_telegram.py, so the notifier doesn't
    # have to re-parse the log and the two can't disagree about a run.
    Path("health_summary.json").write_text(json.dumps({
        "totals": totals,
        "per_source": per_source,
        "zero_sources": sorted(n for n, c in per_source.items() if c == 0),
        "errors": fatal_count,
        "degraded": sum(c for _, c in degrading),
        "degraded_escalated": escalated,
        "warnings": warnings,
        "posts": [str(p) for p in posts],
        "finished_utc": datetime.now(timezone.utc).strftime("%d %b %H:%M"),
    }, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
