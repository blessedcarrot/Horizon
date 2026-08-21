"""The orchestrator's routing between threshold selection and ranking."""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

from src.models import ContentItem, SourceType
from src.orchestrator import HorizonOrchestrator
from src.storage.manager import StorageManager


def _items(n):
    return [
        ContentItem(
            id=f"i{k}",
            source_type=SourceType.RSS,
            title=f"Item {k}",
            url=f"https://example.com/{k}",
            content=f"body {k}",
            published_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
            metadata={"feed_name": "Utility Dive"},
        )
        for k in range(n)
    ]


@pytest.fixture()
def orchestrator(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    storage = StorageManager()
    config = storage.load_config()
    return HorizonOrchestrator(config, storage)


def test_selection_and_synthesis_are_both_off(orchestrator) -> None:
    """Pins the deliberate state, so a change to either is a decision.

    Selection ran once, on 2026-08-20, and failed. Every entry of the gate batch
    errored because `output_config.effort` is rejected on Haiku 4.5, the
    keep-on-no-verdict fallback then passed all 247 items to the ranker, and the
    edition came out at one item. The parameter bug is fixed and covered by
    tests, but the fix has not itself been exercised against a live model, so
    the flag stays off until a run confirms it.
    """
    assert orchestrator.config.selection.enabled is False
    assert orchestrator.config.digest.synthesis_enabled is False

    # A floor that could publish an unbounded edition would defeat the point.
    assert orchestrator.config.selection.max_publish <= 10
    assert (
        orchestrator.config.selection.consider
        >= orchestrator.config.selection.max_publish
    )


def test_settings_map_config_onto_the_selection_module(orchestrator) -> None:
    settings = orchestrator._selection_settings()
    assert settings.gate_model == "claude-haiku-4-5"
    assert settings.max_publish == orchestrator.config.selection.max_publish
    assert settings.use_batch is True


def test_theme_questions_come_from_the_profiles(orchestrator) -> None:
    questions = orchestrator._theme_questions()
    assert set(questions) == set(orchestrator.config.processing.profile_settings)
    assert all(text for text in questions.values())


def test_ranking_maps_results_back_onto_pipeline_items(orchestrator, monkeypatch) -> None:
    """Selection speaks its own type; the ids are the join back to the pipeline."""
    from src.selection.contract import Candidate, SelectionResult

    items = _items(5)

    async def fake_select(candidates, client, themes, settings):
        chosen = [
            Candidate(
                id=c.id, title=c.title, summary="", source="", url="",
                theme="practice",
            )
            for c in list(candidates)[:2]
        ]
        return SelectionResult(
            selected=chosen,
            ranked_ids=[c.id for c in candidates],
            gate_kept=len(candidates),
        )

    monkeypatch.setattr("src.orchestrator.run_selection", fake_select)
    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda cfg: object())

    selected, result = asyncio.run(orchestrator.select_by_ranking(items))
    assert [i.id for i in selected] == ["i0", "i1"]
    assert all(isinstance(i, ContentItem) for i in selected)
    assert result.gate_kept == 5


def test_ranking_drops_ids_that_do_not_map_back(orchestrator, monkeypatch) -> None:
    from src.selection.contract import Candidate, SelectionResult

    async def fake_select(candidates, client, themes, settings):
        return SelectionResult(
            selected=[Candidate(id="ghost", title="", summary="", source="", url="")]
        )

    monkeypatch.setattr("src.orchestrator.run_selection", fake_select)
    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda cfg: object())

    selected, _ = asyncio.run(orchestrator.select_by_ranking(_items(3)))
    assert selected == []


def test_ranking_records_the_theme_the_gate_chose(orchestrator, monkeypatch) -> None:
    from src.selection.contract import Candidate, SelectionResult
    from src.models import ClassificationResult, ProcessingResult

    items = _items(1)
    items[0].processing = ProcessingResult(
        classification=ClassificationResult(profile="practice", method="ai_match")
    )

    async def fake_select(candidates, client, themes, settings):
        return SelectionResult(
            selected=[Candidate(
                id="i0", title="", summary="", source="", url="",
                theme="critical-infrastructure",
            )]
        )

    monkeypatch.setattr("src.orchestrator.run_selection", fake_select)
    monkeypatch.setattr("src.orchestrator.create_ai_client", lambda cfg: object())

    selected, _ = asyncio.run(orchestrator.select_by_ranking(items))
    assert selected[0].processing.classification.profile == "critical-infrastructure"
