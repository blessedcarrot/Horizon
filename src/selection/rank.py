"""Pass two: order the survivors.

The only stage that sees more than one item at a time, which is what makes it the
only stage able to answer "which of these matters most". Large sets are ranked in
chunks and the winners run off against each other, so the comparison stays inside
a context the model can actually hold.
"""

from __future__ import annotations

import json
import logging
from typing import Awaitable, Callable, Dict, List, Sequence

from .contract import Candidate
from .prompts import RANK_SCHEMA, format_entries, rank_system, rank_user

logger = logging.getLogger(__name__)

DEFAULT_CHUNK_SIZE = 25
DEFAULT_CARRY = 10

Completer = Callable[[str, str], Awaitable[str]]


def _parse_order(text: str) -> List[str]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end <= start:
            return []
        try:
            payload = json.loads(text[start : end + 1])
        except json.JSONDecodeError:
            return []
    order = payload.get("order") if isinstance(payload, dict) else None
    if not isinstance(order, list):
        return []
    return [str(value) for value in order]


def reconcile(order: Sequence[str], group: Sequence[Candidate]) -> List[Candidate]:
    """Apply a returned order to a group, defensively.

    A model can drop an id, invent one, or repeat one. Unknown ids are discarded
    and anything it failed to mention is appended in its original position, so the
    stage degrades to "unranked" rather than to "silently lost items".
    """
    by_id = {c.id: c for c in group}
    ranked: List[Candidate] = []
    seen = set()
    for item_id in order:
        candidate = by_id.get(item_id)
        if candidate is None or item_id in seen:
            continue
        seen.add(item_id)
        ranked.append(candidate)

    missing = [c for c in group if c.id not in seen]
    if missing:
        logger.warning(
            "Ranker omitted %d of %d ids; appending them unranked",
            len(missing),
            len(group),
        )
    return ranked + missing


def _entries(group: Sequence[Candidate]) -> str:
    return format_entries(
        [
            {
                "id": c.id,
                "title": c.title,
                "source": f"{c.source}" + (f" · {c.theme}" if c.theme else ""),
                "summary": c.brief(300),
            }
            for c in group
        ]
    )


async def _rank_call(complete: Completer, group: Sequence[Candidate]) -> str:
    """Run one ranking call, logging a failure rather than swallowing it.

    An exception here used to surface only as "omitted N of N ids", which reads
    like a model that ignored instructions rather than a call that never
    returned. On 2026-08-20 two whole chunks failed this way and the log gave no
    reason for either.
    """
    try:
        return await complete(rank_system(), rank_user(_entries(group)))
    except Exception as exc:
        logger.error(
            "Rank call failed for a chunk of %d, leaving it unranked: %s",
            len(group),
            exc,
        )
        return ""


async def rank(
    candidates: Sequence[Candidate],
    complete: Completer,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    carry: int = DEFAULT_CARRY,
    _depth: int = 0,
) -> List[Candidate]:
    """Return candidates ordered most important first."""
    items = list(candidates)
    if len(items) <= 1:
        return items

    if len(items) <= chunk_size:
        text = await _rank_call(complete, items)
        return reconcile(_parse_order(text), items)

    # Too many to compare at once: rank in chunks, then run the winners off.
    groups = [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]
    winners: List[Candidate] = []
    for group in groups:
        text = await _rank_call(complete, group)
        winners.extend(reconcile(_parse_order(text), group)[:carry])

    # Guard against a runoff that cannot shrink, which would recurse forever.
    if len(winners) >= len(items) or _depth >= 3:
        return winners or items

    return await rank(
        winners, complete, chunk_size=chunk_size, carry=carry, _depth=_depth + 1
    )
