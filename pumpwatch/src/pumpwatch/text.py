"""Text helpers: cashtag extraction, hype language, near-duplicate detection.

Everything here is deterministic and explainable on purpose: a compliance
analyst must be able to see exactly why a message counted as hype. An LLM
classifier can be plugged in later through ``HypeScorer`` without changing
the signals that consume it.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Callable, Iterable

CASHTAG = re.compile(r"(?<![\w$])\$([A-Za-z]{1,5})(?![A-Za-z])")

# Weighted hype phrases. Weights reflect how specific the phrase is to
# promotion rather than ordinary discussion. Hebrew phrases are included
# because Israeli Telegram groups are part of the target landscape.
HYPE_PHRASES: dict[str, float] = {
    "to the moon": 0.8,
    "next tesla": 0.9,
    "next nvidia": 0.9,
    "100x": 1.0,
    "50x": 0.9,
    "10x": 0.8,
    "1000%": 0.9,
    "going parabolic": 0.9,
    "before it explodes": 1.0,
    "about to explode": 1.0,
    "don't miss": 0.7,
    "dont miss": 0.7,
    "last chance": 0.7,
    "load up": 0.7,
    "buy now": 0.8,
    "get in now": 0.9,
    "huge news coming": 1.0,
    "big announcement": 0.6,
    "guaranteed": 1.0,
    "easy money": 0.9,
    "squeeze": 0.5,
    "undervalued gem": 0.7,
    "hidden gem": 0.6,
    "vip": 0.5,
    "insider": 0.6,
    "target price": 0.4,
    "pt $": 0.4,
    "תטוס": 0.9,
    "פי 10": 0.8,
    "פי 100": 1.0,
    "להיכנס עכשיו": 0.9,
    "הזדמנות של פעם בחיים": 1.0,
    "מובטח": 1.0,
    "לפני שזה מתפוצץ": 1.0,
}

HYPE_EMOJI: dict[str, float] = {"🚀": 0.6, "💎": 0.3, "🔥": 0.3, "💰": 0.4, "📈": 0.2}

HypeScorer = Callable[[str], float]


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return re.sub(r"\s+", " ", text).strip()


def extract_cashtags(text: str, known: Iterable[str] | None = None) -> tuple[str, ...]:
    """Return unique upper-case tickers mentioned as $TICKER.

    When ``known`` is given, only tickers in that universe are kept, which
    removes noise such as currency amounts written like "$5".
    """

    found = [m.group(1).upper() for m in CASHTAG.finditer(text)]
    if known is not None:
        allowed = {k.upper() for k in known}
        found = [t for t in found if t in allowed]
    return tuple(dict.fromkeys(found))


def hype_score(text: str) -> float:
    """Score 0..1 for how promotional a message reads.

    Uses a saturating sum (1 - product of misses) so several weak cues add up
    without any single message exceeding 1.
    """

    t = normalize(text)
    miss = 1.0
    for phrase, w in HYPE_PHRASES.items():
        if phrase in t:
            miss *= 1.0 - w
    for emoji, w in HYPE_EMOJI.items():
        n = min(text.count(emoji), 3)
        for _ in range(n):
            miss *= 1.0 - w
    exclam = min(text.count("!"), 5)
    miss *= 1.0 - 0.05 * exclam
    letters = [c for c in text if c.isalpha() and c.isascii()]
    if len(letters) >= 12:
        upper_ratio = sum(c.isupper() for c in letters) / len(letters)
        if upper_ratio > 0.6:
            miss *= 0.7
    return round(1.0 - miss, 4)


def shingles(text: str, k: int = 4) -> frozenset[str]:
    words = re.findall(r"\w+", normalize(CASHTAG.sub(" ", text)))
    if len(words) < k:
        return frozenset([" ".join(words)]) if words else frozenset()
    return frozenset(" ".join(words[i : i + k]) for i in range(len(words) - k + 1))


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def near_duplicate_clusters(
    items: list[tuple[str, str]], threshold: float = 0.6, k: int = 4
) -> list[list[int]]:
    """Group (author, text) items whose texts are near-duplicates.

    Single-link clustering with a union-find. Quadratic, which is fine for
    the handful of messages per ticker per day the engine looks at.
    """

    sh = [shingles(text, k) for _, text in items]
    parent = list(range(len(items)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if jaccard(sh[i], sh[j]) >= threshold:
                parent[find(i)] = find(j)

    groups: dict[int, list[int]] = {}
    for i in range(len(items)):
        groups.setdefault(find(i), []).append(i)
    return [g for g in groups.values() if len(g) > 1]
