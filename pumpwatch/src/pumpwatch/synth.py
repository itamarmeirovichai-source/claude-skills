"""Synthetic market used to test the plumbing, never to prove the engine works.

It creates three kinds of tickers:

* **pump** - quiet accumulation, a dilutive filing, coordinated copy-paste
  promotion, a volume explosion, then a collapse. Difficulty varies: some
  pumps skip the filing, use paraphrased messages, or have no accumulation.
* **legit** - a real news filing (8-K/PR) followed by a big move and organic,
  varied chatter (some of it excited).
* **noise** - random micro-caps with occasional volume spikes and stray hype.

Numbers that come out of a backtest on this data only show the engine and the
backtest are wired correctly. Real performance must be measured on real cases.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import date, timedelta

from .backtest import Case
from .models import Bar, Dataset, Filing, Post

PROMO_TEMPLATES = [
    "${t} is about to explode!!! huge news coming, get in now before it's too late 🚀🚀",
    "Don't miss ${t}. Insider says the next tesla of its sector. Load up now 🚀 100x",
    "${t} going parabolic this week, last chance to buy now, guaranteed 10x 💰",
]

PARAPHRASES = [
    "everyone watching ${t}? feels like something big is coming soon, i'm adding more",
    "${t} chart looks ready, volume building, could run hard from here",
    "picked up more ${t} today, management hinted at a partnership",
    "${t} has a tiny float, if news drops this could move a lot",
]

ORGANIC = [
    "${t} reported results today, revenue up, margins still thin though",
    "anyone read the ${t} 8-K? the contract looks real but small",
    "${t} up a lot on the FDA news, taking some profits here",
    "not sure ${t} deserves this valuation after the announcement",
    "${t} conference call was decent, guidance unchanged",
    "great news for ${t} holders today, congrats to the longs 🔥",
]

NOISE_POSTS = [
    "${t} looks interesting, adding to watchlist",
    "${t} 🚀🚀 to the moon lol",
    "sold my ${t}, moving on",
]


@dataclass
class SynthSpec:
    n_pump: int = 20
    n_legit: int = 20
    n_noise: int = 20
    days: int = 260
    seed: int = 7


def _trading_days(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def _base_series(rng: random.Random, n: int) -> tuple[list[float], list[float]]:
    price = rng.uniform(0.05, 3.0)
    vol = rng.uniform(2e4, 5e5)
    prices, vols = [], []
    for _ in range(n):
        price *= max(0.5, 1 + rng.gauss(0, 0.035))
        prices.append(max(price, 0.0001))
        vols.append(max(100.0, vol * rng.lognormvariate(0, 0.45)))
    return prices, vols


def _bars(ticker: str, days: list[date], prices: list[float], vols: list[float], rng: random.Random) -> list[Bar]:
    bars = []
    prev = prices[0]
    for d, p, v in zip(days, prices, vols):
        hi = max(p, prev) * (1 + abs(rng.gauss(0, 0.01)))
        lo = min(p, prev) * (1 - abs(rng.gauss(0, 0.01)))
        bars.append(Bar(ticker, d, round(prev, 4), round(hi, 4), round(lo, 4), round(p, 4), round(v)))
        prev = p
    return bars


def _author(rng: random.Random, prefix: str) -> str:
    return f"{prefix}{rng.randrange(10**6):06d}"


def _background_posts(rng: random.Random, t: str, days: list[date], rate: float) -> list[Post]:
    posts = []
    for d in days:
        for _ in range(rng.choices([0, 1, 2], weights=[1 - rate, rate * 0.8, rate * 0.2])[0]):
            text = rng.choice(NOISE_POSTS + ORGANIC[:2]).replace("${t}", f"${t}")
            posts.append(Post(rng.choice(["telegram", "reddit", "x"]), _author(rng, "u"), d, text, (t,)))
    return posts


def make_pump(rng: random.Random, t: str, days: list[date]) -> tuple[Dataset, Case]:
    n = len(days)
    prices, vols = _base_series(rng, n)
    promo = rng.randrange(150, n - 40)
    crash = promo + rng.randrange(3, 9)
    acc_len = 20 if rng.random() < 0.7 else 0
    for i in range(promo - acc_len, promo):  # quiet accumulation
        prices[i] = prices[i - 1] * (1 + rng.uniform(0.005, 0.03))
        vols[i] *= rng.uniform(1.8, 3.5)
    for i in range(promo, crash):  # the pump
        prices[i] = prices[i - 1] * (1 + rng.uniform(0.15, 0.6))
        vols[i] *= rng.uniform(20, 80)
    for i in range(crash, n):  # the dump
        drop = rng.uniform(0.35, 0.6) if i == crash else rng.gauss(-0.01, 0.03)
        prices[i] = max(0.0001, prices[i - 1] * (1 - drop if i == crash else 1 + drop))
        vols[i] *= 6 if i < crash + 3 else 1
    data = Dataset(bars=_bars(t, days, prices, vols, rng))
    if rng.random() < 0.75:
        fday = days[promo - rng.randrange(10, 60)]
        form = rng.choice(["S-1", "S-3", "424B5", "S-8"])
        data.filings.append(Filing(t, fday, form, "registration of shares for resale"))
    if rng.random() < 0.4:
        data.filings.append(Filing(t, days[promo - rng.randrange(20, 80)], "8-K", "Name change and new business direction in artificial intelligence"))
    data.posts.extend(_background_posts(rng, t, days, 0.05))
    paraphrase_only = rng.random() < 0.25
    promoters = [_author(rng, "p") for _ in range(rng.randrange(4, 12))]
    for i in range(promo - 1, crash):
        d = days[i]
        for a in promoters:
            if rng.random() < 0.7:
                pool = PARAPHRASES if paraphrase_only else PROMO_TEMPLATES
                text = rng.choice(pool).replace("${t}", f"${t}")
                data.posts.append(Post(rng.choice(["telegram", "x"]), a, d, text, (t,)))
        for _ in range(rng.randrange(3, 15)):  # victims echoing
            data.posts.append(Post("reddit", _author(rng, "v"), d, f"just bought ${t}, hope this runs 🚀", (t,)))
    return data, Case(t, "pump", days[promo], days[crash], "synthetic")


def make_legit(rng: random.Random, t: str, days: list[date]) -> tuple[Dataset, Case]:
    n = len(days)
    prices, vols = _base_series(rng, n)
    news = rng.randrange(150, n - 40)
    jump = rng.uniform(0.4, 2.0)
    prices[news] = prices[news - 1] * (1 + jump)
    vols[news] *= rng.uniform(15, 60)
    for i in range(news + 1, n):
        prices[i] = prices[i - 1] * (1 + rng.gauss(0.0, 0.03))
        vols[i] *= 3 if i < news + 5 else 1
    data = Dataset(bars=_bars(t, days, prices, vols, rng))
    form = rng.choice(["8-K", "PR", "6-K"])
    data.filings.append(Filing(t, days[news], form, rng.choice(["FDA approval", "contract award", "quarterly results"])))
    if rng.random() < 0.3:  # real companies raise money too
        data.filings.append(Filing(t, days[news - rng.randrange(20, 80)], "S-3", "shelf registration"))
    data.posts.extend(_background_posts(rng, t, days, 0.05))
    for i in range(news, min(n, news + 4)):
        for _ in range(rng.randrange(5, 25)):
            text = rng.choice(ORGANIC).replace("${t}", f"${t}")
            data.posts.append(Post(rng.choice(["reddit", "x", "telegram"]), _author(rng, "o"), days[i], text, (t,)))
    return data, Case(t, "legit", days[news], days[min(n - 1, news + 10)], "synthetic")


def make_noise(rng: random.Random, t: str, days: list[date]) -> Dataset:
    prices, vols = _base_series(rng, len(days))
    for _ in range(rng.randrange(0, 3)):
        i = rng.randrange(80, len(days))
        vols[i] *= rng.uniform(5, 15)
    data = Dataset(bars=_bars(t, days, prices, vols, rng))
    data.posts.extend(_background_posts(rng, t, days, 0.08))
    return data


def generate(spec: SynthSpec | None = None) -> tuple[Dataset, list[Case]]:
    spec = spec or SynthSpec()
    rng = random.Random(spec.seed)
    days = _trading_days(date(2025, 1, 2), spec.days)
    data = Dataset()
    cases: list[Case] = []
    names = iter(f"{a}{b}{c}{d}" for a in "BCDFG" for b in "AEIOU" for c in "KLMNPRST" for d in "QXZ")
    for _ in range(spec.n_pump):
        d, c = make_pump(rng, next(names), days)
        data.extend(d)
        cases.append(c)
    for _ in range(spec.n_legit):
        d, c = make_legit(rng, next(names), days)
        data.extend(d)
        cases.append(c)
    for _ in range(spec.n_noise):
        data.extend(make_noise(rng, next(names), days))
    return data, cases
