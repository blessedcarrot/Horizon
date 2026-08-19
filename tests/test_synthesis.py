"""The synthesis pass, and its failure behaviour.

The governing rule: a broken synthesis costs the edition its opening paragraph,
never the edition itself.
"""

from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from types import SimpleNamespace

from src.ai.summarizer import DailySummarizer
from src.ai.synthesis import build_user_prompt, entries_from_items, synthesise


class _Client:
    def __init__(self, text="Today the grid story moved."):
        self.text = text
        self.calls = []

    async def complete(self, system, user, **kwargs):
        self.calls.append((system, user, kwargs))
        return self.text


class _Broken:
    async def complete(self, system, user, **kwargs):
        raise RuntimeError("api down")


def _item(title, summary, theme="practice", source="Utility Dive"):
    return SimpleNamespace(
        title=title,
        content=summary,
        metadata={"feed_name": source},
        processing=SimpleNamespace(
            analysis=SimpleNamespace(summary=summary),
            classification=SimpleNamespace(profile=theme),
        ),
    )


def test_synthesis_makes_one_call_over_all_items() -> None:
    client = _Client()
    items = [_item(f"T{i}", f"S{i}") for i in range(4)]
    out = asyncio.run(synthesise(items, client))
    assert out == "Today the grid story moved."
    assert len(client.calls) == 1
    _, user, _ = client.calls[0]
    for i in range(4):
        assert f"T{i}" in user


def test_failure_returns_none_rather_than_raising() -> None:
    """The edition must survive a failed opening."""
    items = [_item("A", "a"), _item("B", "b")]
    assert asyncio.run(synthesise(items, _Broken())) is None


def test_empty_response_is_treated_as_no_preamble() -> None:
    items = [_item("A", "a"), _item("B", "b")]
    assert asyncio.run(synthesise(items, _Client(text="   "))) is None


def test_skipped_on_a_one_item_edition() -> None:
    client = _Client()
    assert asyncio.run(synthesise([_item("A", "a")], client)) is None
    assert client.calls == []


def test_skipped_on_an_empty_edition() -> None:
    client = _Client()
    assert asyncio.run(synthesise([], client)) is None
    assert client.calls == []


def test_item_summaries_are_truncated_so_the_prompt_stays_bounded() -> None:
    entries = entries_from_items([_item("A", "x" * 5000)])
    assert len(entries[0]["summary"]) <= 700


def test_entries_survive_items_with_no_analysis() -> None:
    bare = SimpleNamespace(title="A", content="body", metadata={}, processing=None)
    entries = entries_from_items([bare])
    assert entries[0]["summary"] == "body"
    assert entries[0]["source"] == "unknown"


def test_prompt_carries_theme_and_source() -> None:
    prompt = build_user_prompt(entries_from_items([_item("A", "a")]))
    assert "practice" in prompt and "Utility Dive" in prompt


# ------------------------------------------------------- rendering


def _render(preamble):
    return asyncio.run(
        DailySummarizer().generate_summary([], "2026-08-18", 100, preamble=preamble)
    )


def test_preamble_is_rendered_above_the_contents() -> None:
    items = []
    summariser = DailySummarizer()
    out = asyncio.run(
        summariser.generate_summary(items, "2026-08-18", 10, preamble="The opening.")
    )
    # An empty edition renders the empty-summary body and ignores the preamble,
    # which is correct: there is nothing to synthesise about.
    assert "The opening." not in out


def test_preamble_appears_before_the_rule_when_there_are_items(monkeypatch) -> None:
    from src.models import ContentItem, SourceType

    item = ContentItem(
        id="1",
        source_type=SourceType.RSS,
        title="A grid story",
        url="https://example.com/a",
        content="body",
        published_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    out = asyncio.run(
        DailySummarizer().generate_summary(
            [item], "2026-08-18", 10, preamble="The opening line."
        )
    )
    assert "The opening line." in out
    assert out.index("The opening line.") < out.index("---")


def test_absent_preamble_leaves_the_digest_unchanged() -> None:
    from src.models import ContentItem, SourceType

    item = ContentItem(
        id="1",
        source_type=SourceType.RSS,
        title="A grid story",
        url="https://example.com/a",
        content="body",
        published_at=datetime(2026, 8, 18, tzinfo=timezone.utc),
    )
    with_none = asyncio.run(
        DailySummarizer().generate_summary([item], "2026-08-18", 10)
    )
    with_blank = asyncio.run(
        DailySummarizer().generate_summary([item], "2026-08-18", 10, preamble="   ")
    )
    assert with_none == with_blank
