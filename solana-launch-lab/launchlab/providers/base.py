"""Shared HTTP plumbing for read-only public-data providers: timeout, retry, backoff, rate limiting."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from .. import __version__

# transport(method, url, headers, body, timeout) -> (status, response_headers, body_bytes)
Transport = Callable[[str, str, Mapping[str, str], bytes | None, float], tuple[int, Mapping[str, str], bytes]]

USER_AGENT = f"solana-launch-lab/{__version__} (read-only research client)"


class ProviderError(Exception):
    """A provider call failed. `kind` is one of: rate_limited, http, timeout, bad_json, not_found,
    disabled, forbidden_method, bad_response."""

    def __init__(self, provider: str, kind: str, message: str, *, status: int | None = None, retry_at: float | None = None):
        super().__init__(f"{provider}: {kind}: {message}")
        self.provider = provider
        self.kind = kind
        self.message = message
        self.status = status
        self.retry_at = retry_at


def urllib_transport(method: str, url: str, headers: Mapping[str, str], body: bytes | None, timeout: float) -> tuple[int, Mapping[str, str], bytes]:
    if not url.startswith("https://"):
        raise ValueError("only https:// URLs are fetched")
    req = urllib.request.Request(url, data=body, method=method, headers=dict(headers))  # noqa: S310 - https only, checked above
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 - scheme checked above
            return resp.status, dict(resp.headers.items()), resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()) if exc.headers else {}, exc.read() or b""


@dataclass
class FetchResult:
    url: str
    fetched_at: float
    status: int
    body: bytes
    data: Any


@dataclass
class HttpClient:
    """One instance per provider. Serialises calls to respect the provider's documented rate limit."""

    provider: str
    min_interval_s: float
    timeout_s: float = 20.0
    max_retries: int = 3
    backoff_s: float = 2.0
    max_backoff_s: float = 30.0
    transport: Transport = urllib_transport
    sleep: Callable[[float], None] = time.sleep
    clock: Callable[[], float] = time.time
    enabled: bool = True
    on_fetch: Callable[[FetchResult, Any], None] | None = None  # called with (result, request body) after each success
    _last_call: float = field(default=0.0, repr=False)
    _cooldown_until: float = field(default=0.0, repr=False)

    def request_json(self, url: str, *, method: str = "GET", body: Any = None, headers: Mapping[str, str] | None = None) -> FetchResult:
        if not self.enabled:
            raise ProviderError(self.provider, "disabled", "network access is off (demo/offline mode)")
        if self.clock() < self._cooldown_until:
            raise ProviderError(self.provider, "rate_limited", "cooling down after a rate-limit response", retry_at=self._cooldown_until)
        hdrs = {"accept": "application/json", "user-agent": USER_AGENT}
        payload: bytes | None = None
        if body is not None:
            payload = json.dumps(body).encode()
            hdrs["content-type"] = "application/json"
        hdrs.update(headers or {})
        last: ProviderError | None = None
        for attempt in range(self.max_retries + 1):
            wait = self.min_interval_s - (self.clock() - self._last_call)
            if wait > 0:
                self.sleep(wait)
            self._last_call = self.clock()
            try:
                status, resp_headers, raw = self.transport(method, url, hdrs, payload, self.timeout_s)
            except (TimeoutError, OSError) as exc:
                last = ProviderError(self.provider, "timeout", type(exc).__name__)
                self.sleep(min(self.backoff_s * 2**attempt, self.max_backoff_s))
                continue
            if status == 429:
                retry_after = _retry_after(resp_headers)
                delay = retry_after if retry_after is not None else self.backoff_s * 2**attempt
                last = ProviderError(self.provider, "rate_limited", "HTTP 429", status=429)
                if attempt >= self.max_retries or delay > self.max_backoff_s:
                    self._cooldown_until = self.clock() + min(max(delay, self.backoff_s), 600.0)
                    last.retry_at = self._cooldown_until
                    break
                self.sleep(delay)
                continue
            if status == 404:
                raise ProviderError(self.provider, "not_found", "HTTP 404", status=404)
            if status >= 500:
                last = ProviderError(self.provider, "http", f"HTTP {status}", status=status)
                self.sleep(min(self.backoff_s * 2**attempt, self.max_backoff_s))
                continue
            if status >= 400:
                raise ProviderError(self.provider, "http", f"HTTP {status}", status=status)
            try:
                data = json.loads(raw)
            except (ValueError, UnicodeDecodeError) as exc:
                raise ProviderError(self.provider, "bad_json", "response was not valid JSON", status=status) from exc
            result = FetchResult(url=url, fetched_at=self.clock(), status=status, body=raw, data=data)
            if self.on_fetch is not None:
                self.on_fetch(result, body)
            return result
        assert last is not None
        raise last


def _retry_after(headers: Mapping[str, str]) -> float | None:
    for key, value in headers.items():
        if key.lower() == "retry-after":
            try:
                return max(0.0, float(value))
            except ValueError:
                return None
    return None


def num(value: Any) -> float | None:
    """Parse a provider number that may be a string, null or garbage. Never guesses."""
    if value is None or isinstance(value, bool):
        return None
    try:
        out = float(value)
    except (TypeError, ValueError):
        return None
    return out if out == out and out not in (float("inf"), float("-inf")) else None


def missing_fields(payload: Mapping[str, Any], required: tuple[str, ...]) -> list[str]:
    return [name for name in required if payload.get(name) is None]
