"""The only place selection knows about the surrounding pipeline.

Keeping the conversion here means `contract`, `gate`, `rank` and `defend` have no
engine imports, so they can be lifted into a successor project unchanged.
"""

from __future__ import annotations

from typing import Iterable, List

from .contract import Candidate


def _first_nonempty(*values: object) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def to_candidate(item: object) -> Candidate:
    """Convert a pipeline ContentItem into a Candidate.

    Typed as `object` on purpose: this function is the boundary, and typing it
    against the engine's model would reintroduce the dependency it exists to
    contain.
    """
    processing = getattr(item, "processing", None)
    analysis = getattr(processing, "analysis", None) if processing else None
    metadata = getattr(item, "metadata", None) or {}

    summary = _first_nonempty(
        getattr(analysis, "summary", "") if analysis else "",
        getattr(item, "content", ""),
    )
    source = _first_nonempty(
        metadata.get("feed_name"),
        f"r/{metadata['subreddit']}" if metadata.get("subreddit") else "",
        metadata.get("repo"),
        getattr(getattr(item, "source_type", None), "value", ""),
        "unknown",
    )

    return Candidate(
        id=str(getattr(item, "id", "")),
        title=_first_nonempty(getattr(item, "title", ""), "Untitled"),
        summary=summary,
        source=source,
        url=str(getattr(item, "url", "")),
        published_at=getattr(item, "published_at", None),
        content=str(getattr(item, "content", "") or ""),
    )


def to_candidates(items: Iterable[object]) -> List[Candidate]:
    return [to_candidate(item) for item in items]
