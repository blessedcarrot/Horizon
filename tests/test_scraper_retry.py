"""Tests for the shared scraper retry helper."""

import httpx
import pytest

from src.scrapers.retry import get_with_retry


class _StubClient:
    """Async client stub returning a scripted sequence of responses."""

    def __init__(self, statuses, headers=None):
        self._statuses = list(statuses)
        self._headers = headers or {}
        self.calls = 0

    async def get(self, url, **kwargs):
        self.calls += 1
        status = self._statuses.pop(0)
        if isinstance(status, Exception):
            raise status
        request = httpx.Request("GET", url)
        return httpx.Response(status, request=request, headers=self._headers)


@pytest.fixture(autouse=True)
def _no_sleeping(monkeypatch):
    """Backoff is real time; tests should not spend it."""

    async def _instant(_seconds):
        return None

    monkeypatch.setattr("src.scrapers.retry.asyncio.sleep", _instant)


@pytest.mark.asyncio
async def test_returns_first_successful_response():
    client = _StubClient([200])
    response = await get_with_retry(client, "https://example.com", source="Test")
    assert response.status_code == 200
    assert client.calls == 1


@pytest.mark.asyncio
async def test_retries_transient_server_error_then_succeeds():
    client = _StubClient([503, 200])
    response = await get_with_retry(client, "https://example.com", source="Test")
    assert response.status_code == 200
    assert client.calls == 2


@pytest.mark.asyncio
async def test_gives_up_after_configured_attempts():
    client = _StubClient([503, 503, 503])
    with pytest.raises(httpx.HTTPStatusError):
        await get_with_retry(client, "https://example.com", source="Test", attempts=3)
    assert client.calls == 3


@pytest.mark.asyncio
async def test_does_not_retry_client_refusal():
    """A 403 says 'not for you' and will say it again; retrying wastes the run."""
    client = _StubClient([403, 200])
    with pytest.raises(httpx.HTTPStatusError):
        await get_with_retry(client, "https://example.com", source="Test")
    assert client.calls == 1


@pytest.mark.asyncio
async def test_does_not_retry_not_found():
    client = _StubClient([404, 200])
    with pytest.raises(httpx.HTTPStatusError):
        await get_with_retry(client, "https://example.com", source="Test")
    assert client.calls == 1


@pytest.mark.asyncio
async def test_retries_rate_limit():
    client = _StubClient([429, 200])
    response = await get_with_retry(client, "https://example.com", source="Test")
    assert response.status_code == 200
    assert client.calls == 2


@pytest.mark.asyncio
async def test_retries_timeout():
    client = _StubClient([httpx.TimeoutException("slow"), 200])
    response = await get_with_retry(client, "https://example.com", source="Test")
    assert response.status_code == 200
    assert client.calls == 2


@pytest.mark.asyncio
async def test_honours_retry_after_header(monkeypatch):
    """A server saying when to return beats any backoff formula."""
    slept = []

    async def _record(seconds):
        slept.append(seconds)

    monkeypatch.setattr("src.scrapers.retry.asyncio.sleep", _record)
    client = _StubClient([429, 200], headers={"Retry-After": "7"})
    await get_with_retry(client, "https://example.com", source="Test")
    assert slept == [7.0]


@pytest.mark.asyncio
async def test_caps_hostile_retry_after(monkeypatch):
    """A server must not be able to stall the whole run."""
    slept = []

    async def _record(seconds):
        slept.append(seconds)

    monkeypatch.setattr("src.scrapers.retry.asyncio.sleep", _record)
    client = _StubClient([503, 200], headers={"Retry-After": "86400"})
    await get_with_retry(client, "https://example.com", source="Test")
    assert slept and slept[0] <= 30.0


@pytest.mark.asyncio
async def test_backoff_grows_between_attempts(monkeypatch):
    slept = []

    async def _record(seconds):
        slept.append(seconds)

    monkeypatch.setattr("src.scrapers.retry.asyncio.sleep", _record)
    client = _StubClient([503, 503, 200])
    await get_with_retry(client, "https://example.com", source="Test", base_delay=2.0)
    assert len(slept) == 2
    assert slept[1] > slept[0]
