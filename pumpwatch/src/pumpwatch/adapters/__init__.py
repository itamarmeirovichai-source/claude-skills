"""Turn public social-media data into ``Post`` records.

Every adapter follows the same privacy rules (see
``research/social_data_access.md``):

* Authors are never stored as names, handles or platform ids. They become
  opaque ids: a keyed hash (HMAC-SHA256) of the platform id with a secret
  salt the operator keeps outside the data. The same author gets the same id
  within one salt, which is all S5 needs to count distinct accounts.
* Only the fields the engine uses are kept: source, opaque author, day, text
  and tickers. Names, phone numbers, media and reply graphs are dropped.
* Adapters only accept data that is public at the source. They refuse
  exports of private chats instead of silently processing them.
"""

from __future__ import annotations

import hashlib
import hmac

AUTHOR_ID_HEX = 16


def hash_author(raw_id: str, salt: str | bytes, namespace: str) -> str:
    """Return an opaque, salted id for an author.

    ``namespace`` (usually the platform name) keeps the same raw id on two
    platforms from colliding. The salt must be secret and non-empty: without
    it the hash of a public id could be reversed by hashing candidates.
    """

    key = salt.encode("utf-8") if isinstance(salt, str) else bytes(salt)
    if not key:
        raise ValueError("a non-empty secret salt is required to hash author ids")
    msg = f"{namespace}\x1f{raw_id}".encode("utf-8")
    digest = hmac.new(key, msg, hashlib.sha256).hexdigest()
    return f"{namespace}:{digest[:AUTHOR_ID_HEX]}"
