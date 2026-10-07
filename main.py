"""Higgsfield API example: Seedance 2.5 text-to-video via the official Python SDK.

Credentials: HF_KEY="key_id:key_secret", read at runtime from the environment or
from .env.local (git-ignored). The value is never printed or logged.
Run: pip install -r requirements.txt && python3 main.py   (a billable generation)
"""
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env.local", override=False)

import higgsfield_client  # noqa: E402  (import after the env is loaded)

MODEL = "bytedance/seedance-2.5/text-to-video"
ARGUMENTS = {
    "prompt": "A cinematic scene at sunset",
    "duration": 5,
    "resolution": "720p",
    "aspect_ratio": "16:9",
}


def main() -> int:
    try:
        result = higgsfield_client.subscribe(
            MODEL,
            arguments=ARGUMENTS,
            on_enqueue=lambda rid: print(f"queued: request_id={rid}", flush=True),
            on_queue_update=lambda st: print(f"status: {type(st).__name__}", flush=True),
        )
    except higgsfield_client.CredentialsMissedError:
        print("error: HF_KEY is not set (add it to .env.local or the environment)", file=sys.stderr)
        return 2
    except higgsfield_client.HiggsfieldClientError as exc:
        print(f"error: request rejected by the API: {exc}", file=sys.stderr)
        return 1

    status = result.get("status")
    request_id = result.get("request_id")
    if status != "completed":
        reason = {"failed": "generation failed", "nsfw": "blocked by content moderation",
                  "canceled": "request was canceled"}.get(status, f"unexpected status {status!r}")
        detail = f" ({result['error']})" if result.get("error") else ""
        print(f"not successful: {reason}{detail} [request_id={request_id}]", file=sys.stderr)
        return 1

    url = (result.get("video") or {}).get("url")
    if not url:
        print(f"not successful: completed but no video URL in the response [request_id={request_id}]",
              file=sys.stderr)
        return 1
    print(f"completed [request_id={request_id}]")
    print(url)
    return 0


if __name__ == "__main__":
    sys.exit(main())
