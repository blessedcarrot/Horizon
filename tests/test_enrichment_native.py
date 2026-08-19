"""Native web-search enrichment: schema, parsing, and pause_turn handling."""

from __future__ import annotations

import asyncio
import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.ai.client import AnthropicClient
from src.ai.enrichment_native import (
    WEB_SEARCH_TOOL,
    build_schema,
    enrich_one,
    parse_artifact,
)
from src.models import AIConfig, AIProvider


def _block(bid, optional=False):
    return SimpleNamespace(id=bid, optional=optional)


BLOCKS = [_block("summary"), _block("background"), _block("impact", optional=True)]
IDS = ["summary", "background", "impact"]


# ------------------------------------------------------------------ schema


def test_schema_constrains_block_ids_to_the_profile() -> None:
    schema = build_schema(IDS)
    assert schema["properties"]["blocks"]["items"]["properties"]["id"]["enum"] == IDS
    assert schema["additionalProperties"] is False


# ----------------------------------------------------------------- parsing


def test_parse_accepts_a_well_formed_artifact() -> None:
    text = json.dumps({"title": "T", "blocks": [
        {"id": "summary", "title": "Summary", "content": "c"}]})
    assert parse_artifact(text, IDS)["title"] == "T"


def test_parse_drops_blocks_the_profile_never_declared() -> None:
    text = json.dumps({"title": "T", "blocks": [
        {"id": "summary", "title": "S", "content": "c"},
        {"id": "invented", "title": "X", "content": "c"},
    ]})
    assert [b["id"] for b in parse_artifact(text, IDS)["blocks"]] == ["summary"]


def test_parse_drops_empty_blocks() -> None:
    text = json.dumps({"title": "T", "blocks": [
        {"id": "summary", "title": "S", "content": "c"},
        {"id": "background", "title": "B", "content": "   "},
    ]})
    assert [b["id"] for b in parse_artifact(text, IDS)["blocks"]] == ["summary"]


def test_parse_ignores_a_repeated_block() -> None:
    text = json.dumps({"title": "T", "blocks": [
        {"id": "summary", "title": "S", "content": "one"},
        {"id": "summary", "title": "S", "content": "two"},
    ]})
    blocks = parse_artifact(text, IDS)["blocks"]
    assert len(blocks) == 1 and blocks[0]["content"] == "one"


def test_parse_extracts_json_wrapped_in_prose() -> None:
    text = 'Here:\n{"title":"T","blocks":[{"id":"summary","title":"S","content":"c"}]}\nend'
    assert parse_artifact(text, IDS) is not None


def test_parse_returns_none_when_unusable() -> None:
    assert parse_artifact("not json", IDS) is None
    assert parse_artifact(json.dumps({"title": "", "blocks": []}), IDS) is None
    assert parse_artifact(json.dumps({"title": "T", "blocks": []}), IDS) is None


# ------------------------------------------------------------------- call


class _Client:
    def __init__(self, text):
        self.text = text
        self.kwargs = None
        self.tools = None

    async def complete_with_tools(self, system, user, tools, **kwargs):
        self.tools = tools
        self.kwargs = kwargs
        return self.text


def test_enrich_one_requests_the_web_search_tool() -> None:
    client = _Client(json.dumps({"title": "T", "blocks": [
        {"id": "summary", "title": "S", "content": "c"}]}))
    out = asyncio.run(enrich_one(client, "profile", BLOCKS, "ctx"))
    assert out["title"] == "T"
    assert client.tools == [WEB_SEARCH_TOOL]
    assert client.kwargs["schema"]["properties"]["blocks"]["items"]["properties"]["id"]["enum"] == IDS


def test_enrich_one_returns_none_on_failure_so_the_item_still_publishes() -> None:
    class _Broken:
        async def complete_with_tools(self, *a, **k):
            raise RuntimeError("search unavailable")

    assert asyncio.run(enrich_one(_Broken(), "p", BLOCKS, "ctx")) is None


def test_enrich_one_returns_none_when_no_blocks_are_declared() -> None:
    assert asyncio.run(enrich_one(_Client("{}"), "p", [], "ctx")) is None


# ------------------------------------------------------- pause_turn


def _client(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "k")
    return AnthropicClient(AIConfig(
        provider=AIProvider.ANTHROPIC, model="claude-sonnet-5",
        api_key_env="ANTHROPIC_API_KEY", temperature=1.0, max_tokens=1024))


def _msg(text, stop="end_turn"):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        stop_reason=stop,
        usage=SimpleNamespace(input_tokens=1, output_tokens=1),
    )


def test_paused_tool_turn_is_resumed(monkeypatch) -> None:
    """Ignoring pause_turn yields a silently truncated answer with no error."""
    client = _client(monkeypatch)
    create = AsyncMock(side_effect=[_msg("partial", "pause_turn"), _msg("final")])
    client.client = MagicMock(messages=MagicMock(create=create))
    out = asyncio.run(client.complete_with_tools("s", "u", [WEB_SEARCH_TOOL]))
    assert out == "final"
    assert create.await_count == 2


def test_resume_gives_up_rather_than_looping(monkeypatch) -> None:
    client = _client(monkeypatch)
    create = AsyncMock(return_value=_msg("still going", "pause_turn"))
    client.client = MagicMock(messages=MagicMock(create=create))
    out = asyncio.run(
        client.complete_with_tools("s", "u", [WEB_SEARCH_TOOL], max_continuations=2)
    )
    assert out == "still going"
    assert create.await_count == 3


def test_tool_response_takes_the_last_text_not_the_first(monkeypatch) -> None:
    """The model narrates before searching; the answer is the final block."""
    client = _client(monkeypatch)
    message = SimpleNamespace(
        content=[
            SimpleNamespace(type="text", text="Let me search for that."),
            SimpleNamespace(type="web_search_tool_result"),
            SimpleNamespace(type="text", text='{"title":"T"}'),
        ],
        stop_reason="end_turn",
        usage=SimpleNamespace(input_tokens=1, output_tokens=1),
    )
    client.client = MagicMock(messages=MagicMock(create=AsyncMock(return_value=message)))
    assert asyncio.run(
        client.complete_with_tools("s", "u", [WEB_SEARCH_TOOL])
    ) == '{"title":"T"}'
