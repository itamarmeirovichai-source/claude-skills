"""A small paced HTTPS GET client. Read-only by construction: it can only send GET requests."""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable

Transport = Callable[[str, dict[str, str], float], tuple[int, bytes]]

# Generic client name: no personal or project details are sent to providers.
HEADERS = {"User-Agent": "Mozilla/5.0", "Accept": "application/json"}
RETRY_WAITS = (2.0, 6.0, 15.0)


class FetchError(Exception):
    pass


def urllib_transport(url: str, headers: dict[str, str], timeout: float) -> tuple[int, bytes]:
    if not url.startswith("https://"):
        raise ValueError("https only")
    request = urllib.request.Request(url, headers=headers, method="GET")  # noqa: S310
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, b""
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise FetchError(str(error)) from error


class Http:
    def __init__(
        self,
        transport: Transport = urllib_transport,
        min_interval: float = 0.4,
        sleep: Callable[[float], None] = time.sleep,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self._transport = transport
        self._min_interval = min_interval
        self._sleep = sleep
        self._clock = clock
        self._last = float("-inf")
        self.calls = 0

    def get_json(self, url: str) -> object:
        for wait in (*RETRY_WAITS, None):
            pause = self._min_interval - (self._clock() - self._last)
            if pause > 0:
                self._sleep(pause)
            self._last = self._clock()
            self.calls += 1
            try:
                status, body = self._transport(url, HEADERS, 25.0)
            except FetchError:
                status, body = 599, b""
            if status == 200:
                try:
                    return json.loads(body)
                except ValueError as error:
                    raise FetchError(f"not JSON from {url.split('?')[0]}") from error
            if status not in (429, 500, 502, 503, 504, 599) or wait is None:
                raise FetchError(f"HTTP {status} from {url.split('?')[0]}")
            self._sleep(wait)
        raise FetchError("unreachable")
