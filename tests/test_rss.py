from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from unittest.mock import AsyncMock
from unittest.mock import MagicMock

from src.models import RSSSourceConfig
from src.scrapers.rss import RSSScraper

_FEED = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"><channel><title>Test</title>
  <item>
    <guid>entry-1</guid>
    <title>Item 1</title>
    <link>https://example.com/item-1</link>
    <pubDate>Fri, 24 Apr 2026 12:00:00 GMT</pubDate>
    <description>Short summary from feed.</description>
  </item>
</channel></rss>
"""
_SINCE = datetime(2026, 4, 24, 0, 0, tzinfo=timezone.utc)


def _make_feed_client(feed_text: str) -> AsyncMock:
    response = MagicMock()
    response.text = feed_text
    response.raise_for_status.return_value = None
    client = AsyncMock()
    client.get.return_value = response
    return client


def test_rss_ids_are_deterministic() -> None:
    client = _make_feed_client(_FEED)
    source = RSSSourceConfig(
        name="Test", url="https://example.com/feed.xml", profile="rss-profile"
    )
    scraper = RSSScraper([source], client)

    first_item = asyncio.run(scraper.fetch(_SINCE))[0]
    first = first_item.id
    second = asyncio.run(scraper.fetch(_SINCE))[0].id

    assert first == second
    assert first == "rss:example.com_feed.xml:5e2d5d1e58e94d76"
    assert first_item.profile == "rss-profile"


def _make_registry(name: str, extractor):
    registry = MagicMock()
    registry.get.side_effect = lambda n: extractor if n == name else None
    return registry


def test_content_extractor_replaces_feed_content() -> None:
    client = _make_feed_client(_FEED)
    extractor = AsyncMock()
    extractor.extract.return_value = "Full article text from extractor."

    source = RSSSourceConfig(
        name="Test", url="https://example.com/feed.xml", content_extractor="my-ext"
    )
    scraper = RSSScraper([source], client, extractors=_make_registry("my-ext", extractor))
    items = asyncio.run(scraper.fetch(_SINCE))

    assert len(items) == 1
    assert items[0].content == "Full article text from extractor."
    extractor.extract.assert_awaited_once_with("https://example.com/item-1", client)


def test_content_extractor_falls_back_on_none() -> None:
    client = _make_feed_client(_FEED)
    extractor = AsyncMock()
    extractor.extract.return_value = None  # extraction failed

    source = RSSSourceConfig(
        name="Test", url="https://example.com/feed.xml", content_extractor="my-ext"
    )
    scraper = RSSScraper([source], client, extractors=_make_registry("my-ext", extractor))
    items = asyncio.run(scraper.fetch(_SINCE))

    assert len(items) == 1
    assert items[0].content == "Short summary from feed."


def test_unknown_extractor_name_ignored() -> None:
    client = _make_feed_client(_FEED)
    source = RSSSourceConfig(
        name="Test", url="https://example.com/feed.xml", content_extractor="nonexistent"
    )
    scraper = RSSScraper([source], client, extractors=_make_registry("other", AsyncMock()))
    items = asyncio.run(scraper.fetch(_SINCE))

    assert len(items) == 1
    assert items[0].content == "Short summary from feed."


_MULTI_FEED = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0"><channel><title>Busy</title>
  <item><guid>e-1</guid><title>Oldest</title><link>https://example.com/1</link>
    <pubDate>Fri, 24 Apr 2026 01:00:00 GMT</pubDate><description>a</description></item>
  <item><guid>e-2</guid><title>Middle</title><link>https://example.com/2</link>
    <pubDate>Fri, 24 Apr 2026 05:00:00 GMT</pubDate><description>b</description></item>
  <item><guid>e-3</guid><title>Newest</title><link>https://example.com/3</link>
    <pubDate>Fri, 24 Apr 2026 09:00:00 GMT</pubDate><description>c</description></item>
</channel></rss>
"""


def _fetch(source: RSSSourceConfig, feed_text: str = _MULTI_FEED):
    scraper = RSSScraper([source], _make_feed_client(feed_text))
    return asyncio.run(scraper.fetch(_SINCE))


def test_max_items_keeps_the_newest_entries() -> None:
    source = RSSSourceConfig(
        name="Busy", url="https://example.com/feed.xml", max_items=2
    )
    items = _fetch(source)
    assert [item.title for item in items] == ["Newest", "Middle"]


def test_max_items_unset_returns_everything() -> None:
    source = RSSSourceConfig(name="Busy", url="https://example.com/feed.xml")
    items = _fetch(source)
    assert len(items) == 3


def test_max_items_larger_than_feed_is_harmless() -> None:
    source = RSSSourceConfig(
        name="Busy", url="https://example.com/feed.xml", max_items=99
    )
    assert len(_fetch(source)) == 3


def test_max_items_counts_in_window_items_not_raw_entries() -> None:
    """Three entries exist; only two are in window, and the cap applies to those."""
    late_since = datetime(2026, 4, 24, 4, 0, tzinfo=timezone.utc)
    source = RSSSourceConfig(
        name="Busy", url="https://example.com/feed.xml", max_items=1
    )
    scraper = RSSScraper([source], _make_feed_client(_MULTI_FEED))
    items = asyncio.run(scraper.fetch(late_since))
    assert [item.title for item in items] == ["Newest"]


def test_uncapped_order_is_left_as_the_feed_had_it() -> None:
    """Recency ordering is a consequence of capping, not a promise of the scraper.

    Pinning this so a later change that always sorts is a deliberate decision
    rather than an accident.
    """
    late_since = datetime(2026, 4, 24, 4, 0, tzinfo=timezone.utc)
    source = RSSSourceConfig(name="Busy", url="https://example.com/feed.xml")
    scraper = RSSScraper([source], _make_feed_client(_MULTI_FEED))
    items = asyncio.run(scraper.fetch(late_since))
    assert [item.title for item in items] == ["Middle", "Newest"]


def test_max_items_rejects_zero() -> None:
    import pytest

    with pytest.raises(Exception):
        RSSSourceConfig(name="Busy", url="https://example.com/f.xml", max_items=0)


def test_capped_feed_still_reports_its_attempted_count() -> None:
    """The health footer counts what a feed contributed, which is the capped number."""
    source = RSSSourceConfig(
        name="Busy", url="https://example.com/feed.xml", max_items=1
    )
    scraper = RSSScraper([source], _make_feed_client(_MULTI_FEED))
    asyncio.run(scraper.fetch(_SINCE))
    assert scraper.attempted_counts == {"Busy": 1}
