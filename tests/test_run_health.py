"""Tests for the post-run health check.

The script gates the build, so both directions matter equally: a run that
published a complete digest must stay green, and a run where a stage silently
produced nothing must go red. Getting the first wrong makes the red X
meaningless; getting the second wrong is the failure the script exists for.
"""

import importlib.util
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_run_health.py"


def _load():
    spec = importlib.util.spec_from_file_location("run_health", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


health = _load()


def _parse(tmp_path: Path, body: str):
    log = tmp_path / "run.log"
    log.write_text(body, encoding="utf-8")
    return health.parse_log(log)


HEALTHY = """\
📥 Fetched 222 items from all sources
🤖 Analyzed 222 items with AI
⭐️ Selected 13 items with profile filters
⚖️ Balanced digest selected 13/13 items
   Enriched 13/13 items
🧮 Token usage this run: 100 tokens (input: 80, output: 20)
"""


def test_a_healthy_run_reports_nothing_collapsed(tmp_path):
    *_, collapsed = _parse(tmp_path, HEALTHY)
    assert collapsed == []


def test_a_gate_that_returned_no_verdict_is_fatal(tmp_path):
    body = HEALTHY + (
        "[08/20/26 21:54:09] WARNING  Gate returned no verdict for 247 items; "
        "keeping them for the ranker\n"
    )
    *_, collapsed = _parse(tmp_path, body)
    assert len(collapsed) == 1
    assert "gate did not run" in collapsed[0][1]


def test_a_batch_returning_nothing_is_fatal(tmp_path):
    body = HEALTHY + (
        "[08/20/26 21:54:09] WARNING  Batch msgbatch_01GAJX returned 0 of 7 "
        "results\n"
    )
    *_, collapsed = _parse(tmp_path, body)
    assert len(collapsed) == 1
    assert "Every entry in it failed" in collapsed[0][1]


def test_only_a_wholly_empty_ranking_chunk_is_fatal(tmp_path):
    """A ranker dropping one id of twenty-five is sloppiness, not a failure.

    Failing the build on that would make the signal unreadable again, which is
    the mistake this check was corrected for once already.
    """
    body = HEALTHY + (
        "[08/20/26 21:54:15] WARNING  Ranker omitted 1 of 25 ids; appending "
        "them unranked\n"
        "[08/20/26 21:55:56] WARNING  Ranker omitted 25 of 25 ids; appending "
        "them unranked\n"
    )
    *_, collapsed = _parse(tmp_path, body)
    assert len(collapsed) == 1
    assert "whole ranking chunk" in collapsed[0][1]


def test_an_enrichment_failure_alone_stays_green(tmp_path):
    """The item published; only its depth was lost. This must not go red."""
    body = HEALTHY.replace("Enriched 13/13", "Enriched 12/13") + (
        "[08/20/26 21:55:00] ERROR    Error enriching item rss:x:abc: "
        "Invalid enrichment artifact\n"
    )
    _, _, totals, errors, _, collapsed = _parse(tmp_path, body)
    fatal, degrading, escalated = health.split_by_severity(
        health.group_errors(errors), totals
    )
    assert collapsed == []
    assert fatal == []
    assert escalated is False
    assert sum(c for _, c in degrading) == 1


def test_analysis_collapsing_on_every_item_stays_fatal(tmp_path):
    body = HEALTHY + "".join(
        f"[08/20/26 21:55:00] ERROR    Error analyzing item rss:x:{i}: "
        "BadRequestError 400\n"
        for i in range(30)
    )
    _, _, totals, errors, _, _ = _parse(tmp_path, body)
    fatal, _, _ = health.split_by_severity(health.group_errors(errors), totals)
    assert sum(c for _, c in fatal) == 30
