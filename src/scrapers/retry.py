"""Shared retry with exponential backoff for scraper HTTP requests.

Sources fail transiently often enough that a single attempt loses a whole
channel for a run: Google News returned one 503 on 2026-08-17 and the
vendor-watch coverage for that day vanished. On a once-daily cadence that is a
full day blind, so a retry is worth more than the seconds it costs.

Design choices worth knowing:

* **Only transient failures are retried.** A 403 or 404 means "not for you" or
  "not there" and will say the same thing three times; retrying it wastes the
  run's time and hammers a host that already refused. Retries apply to 408, 429
  and 5xx, plus connection and timeout errors.
* **Retry-After is honoured** when a server sends it, capped so a hostile value
  cannot stall a run. A server telling you when to come back is better
  information than any backoff formula.
* **Jitter is added** so several sources retrying after a shared upstream blip
  do not resend in lockstep.
* **The caller still handles final failure.** This raises the last error rather
  than returning a sentinel, so existing `except httpx.HTTPError` blocks around
  call sites keep working unchanged.
"""

from __future__ import annotations

import asyncio
import logging
import random
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)

RETRYABLE_STATUS = frozenset({408, 425, 429, 500, 502, 503, 504})
DEFAULT_ATTEMPTS = 3
DEFAULT_BASE_DELAY = 2.0
MAX_DELAY = 30.0


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (httpx.TimeoutException, httpx.ConnectError, httpx.ReadError)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRYABLE_STATUS
    return False


def _delay_for(attempt: int, base_delay: float, exc: Exception) -> float:
    """Seconds to wait before the next attempt.

    Prefers the server's own Retry-After when present, otherwise exponential
    backoff. Jitter keeps concurrent sources from retrying in lockstep.
    """
    retry_after: Optional[float] = None
    if isinstance(exc, httpx.HTTPStatusError):
        raw = exc.response.headers.get("Retry-After")
        if raw:
            try:
                retry_after = float(raw)
            except ValueError:  # HTTP-date form; fall back to backoff
                retry_after = None

    if retry_after is not None:
        return min(retry_after, MAX_DELAY)

    backoff = base_delay * (2**attempt)
    return min(backoff + random.uniform(0, base_delay / 2), MAX_DELAY)


async def get_with_retry(
    client: httpx.AsyncClient,
    url: str,
    *,
    source: str,
    attempts: int = DEFAULT_ATTEMPTS,
    base_delay: float = DEFAULT_BASE_DELAY,
    **kwargs: Any,
) -> httpx.Response:
    """GET a URL, retrying transient failures with exponential backoff.

    Args:
        client: Shared async HTTP client.
        url: URL to fetch.
        source: Human-readable source name, used in log messages so a reader
            can tell which source is struggling.
        attempts: Total attempts including the first.
        base_delay: Seconds for the first backoff; doubles per attempt.
        **kwargs: Passed through to ``client.get`` (params, headers, ...).

    Returns:
        The successful response.

    Raises:
        httpx.HTTPError: The last error, when every attempt failed or the
            failure was not transient.
    """
    last_exc: Exception | None = None

    for attempt in range(attempts):
        try:
            response = await client.get(url, **kwargs)
            response.raise_for_status()
            if attempt:
                logger.info("%s succeeded on attempt %d", source, attempt + 1)
            return response
        except Exception as exc:  # noqa: BLE001 - re-raised below
            last_exc = exc
            if not _is_retryable(exc) or attempt == attempts - 1:
                raise
            delay = _delay_for(attempt, base_delay, exc)
            logger.warning(
                "%s attempt %d/%d failed (%s); retrying in %.1fs",
                source,
                attempt + 1,
                attempts,
                exc,
                delay,
            )
            await asyncio.sleep(delay)

    raise last_exc or RuntimeError(f"{source}: request failed")
