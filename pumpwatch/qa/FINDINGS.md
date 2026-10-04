# PumpWatch engine core: QA findings

> **Review date:** 4 October 2026
> **Reviewed commit:** `e7a145f` ("PumpWatch: engine core")
> **Scope:** everything in `src/pumpwatch/` except the CLI and the generator.
> **Who reviewed it:**
> - Team A: code correctness.
> - Team B: backtest integrity.
> - Team C: red team. Their evasion results are in [`RED_TEAM.md`](RED_TEAM.md).
>
> **How each finding was accepted:**
> 1. It was **reproduced by the head of QA**.
> 2. It is **pinned by a test in `tests/test_qa_*.py`**, marked `xfail(strict=True, reason="QA-n")`.
> 3. **The proposed fix was applied to a scratch copy of `src/` and the whole suite was run.**
>
> Team suggestions that failed this check were dropped. They are listed at the end.

**Applying all the fixes at once:**
```
cd pumpwatch && patch -p0 < qa/proposed_fixes.patch
python -m pytest -q --runxfail      # 102 passed (with the patch applied)
```
After the patch, delete the `xfail` markers, because `strict=True` turns each now-passing test into a failure. The snippets below are the important parts of that patch.

## Summary

| Severity | Count | IDs |
|---|---|---|
| **Critical** | 2 | QA-1, QA-2 |
| **High** | 7 | QA-3 to QA-9 |
| **Medium** | 11 | QA-10 to QA-20 |
| **Low** | 5 | QA-21 to QA-25 |
| **Total** | **25** | |

**The top 3:**
1. **QA-1:** the engine's own "no look-ahead" guarantee is false. The score for day D changes when data dated after D exists.
2. **QA-2:** a ticker with two cases always lands in both the calibration half and the holdout half. The holdout is then not clean.
3. **QA-3:** one NaN or inf in a price bar makes S1 fire at full strength (1.0).

**Gate C warning.** Until QA-1, QA-2, QA-8 and QA-9 are fixed, the backtest numbers cannot be used for Gate C. These four bugs inflate recall and lead time, and they leak holdout information into the threshold.

---

## Critical

### QA-1: renormalisation reads the whole dataset, so day D depends on later data (look-ahead)
**Where:** `engine.py:37-49` (`available_signals`), used at `engine.py:68-69` and `engine.py:111`.

**What goes wrong:** a signal counts toward the denominator if its data source has *any* row anywhere in the dataset.
- That includes rows dated after D, and rows for unrelated tickers.
- So adding a post, broker-flow row or victim report dated next year changes today's score.
- In live use, the day a broker feed is switched on, every historical score shrinks.
- The thresholds calibrated in the backtest then no longer mean the same thing.

**Failing input** (`test_qa_no_lookahead.py::test_engine_score_identical_whatever_lies_after_scored_day`, `::test_engine_score_ignores_future_rows_of_other_tickers`):
- Take 30 flat bars for AAA with a 50x volume spike. The spike day scores **66.67**.
- Add one post dated 200 days later: the spike day scores **30.77**.
- Add rows for an unrelated ticker: the spike day scores **20.0**.
- On the synthetic pump, a victim report dated a year later for another ticker moves PUMP's spike-day score.

**Fix:** use as-of coverage start dates for each source, and compute the denominator per day.
```python
def available_signals(data: Dataset) -> dict[str, date]:
    """First day each signal's data source has coverage (as-of, never look-ahead)."""
    out = {"S1_abnormal_volume": date.min, "S2_quiet_accumulation": date.min}
    for names, rows in ((("S3_suspicious_filings",), data.filings),
                        (("S4_hype_burst", "S5_coordinated_promotion"), data.posts),
                        (("S6_broker_flow",), data.broker_flow),
                        (("S7_victim_reports",), data.reports)):
        if rows:
            first = min(r.day for r in rows)
            for n in names:
                out[n] = first
    return out

# score_ticker: inside the day loop
active = [n for n in ALL_SIGNALS if starts.get(n, date.max) <= day]
denom = sum(cfg.weights.get(n, 0.0) for n in active) or 1.0
```
Better still: let `Dataset` carry an explicit `coverage: dict[source, date]` declared by the loader (the date a feed contract started), so that "first row seen" stops being a proxy.

### QA-2: `split_cases` always puts the same ticker in both halves
**Where:** `backtest.py:61-70`, and its consequences at `backtest.py:180-181, 194, 205-206`.

**What goes wrong:**
- Cases are sorted by `sha1(ticker)`. Two cases for one ticker get the same hash, so they sit next to each other and take opposite parity. **They are split every time** (500 of 500 random trials).
- Each half's universe then contains that ticker. The other half's pump-window alerts count as **false alerts in both halves**.
- The calibrated threshold depends on alerts inside the holdout case's window. Team B moved only holdout-period scores and the chosen threshold went from 25 to 59.
- A pump case and a legit case for the same ticker are hashed in separate groups, so they can also end up split.

**Failing input** (`test_qa_backtest.py::test_ticker_never_appears_in_both_halves`, `::test_twice_pumped_ticker_causes_no_phantom_false_alerts`):
- Cases: AAA pumped in January 2024 and again in June 2024, plus BBB and CCC.
- Calibration gets `[AAA, BBB]`, holdout gets `[AAA, CCC]`.
- Each half reports 1 false alert. The correct count is 0.

**Fix:** split by ticker. Every case for a ticker goes to the same half.
```python
def split_cases(cases):
    by_ticker: dict[str, list[Case]] = {}
    for c in cases:
        by_ticker.setdefault(c.ticker, []).append(c)
    calib, hold = [], []
    for label in ("pump", "legit"):
        group = sorted((t for t, cs in by_ticker.items()
                        if ("pump" if any(c.label == "pump" for c in cs) else "legit") == label),
                       key=lambda t: hashlib.sha1(t.encode()).hexdigest())
        for i, t in enumerate(group):
            (calib if i % 2 == 0 else hold).extend(by_ticker[t])
    return calib, hold
```

---

## High

### QA-3: a NaN or inf bar makes S1 (and S2) fire at full strength
**Where:** `signals/market.py:17-33` (S1) and `signals/market.py:51-76` (S2).

**What goes wrong:** both signals keep going when they should stop.
- `nan < 5.0` is `False`, so the trigger check passes.
- `min(1.0, nan)` returns `1.0`.

Missing prints are commonly encoded as NaN by vendors and pandas. They become the strongest possible market evidence.

**Failing input** (`test_qa_signals.py::test_s1_ignores_non_finite_bar[...]`, `::test_s2_ignores_nan_close_on_scored_day`):
- 29 normal bars, then a bar with `volume=nan`. Result: `S1 strength=1.0, evidence "dollar volume nanx …"`. The same happens with `close=nan` or `inf`.
- A 20-session climb that ends on a NaN close gives `S2 strength=1.0, "+nan%"`.

**Fix:**
```python
# S1
if bar is None or not math.isfinite(bar.dollar_volume) or bar.dollar_volume < 0:
    return None
# S2, after seq = window + [today]
if not all(math.isfinite(b.close) and math.isfinite(b.volume) for b in seq):
    return None
```
Also reject non-finite values when data is loaded (CLI / `Bar.__post_init__`).

### QA-4: weekend posts are never scored by S4, and they hide Monday's burst
**Where:** `signals/social.py:17-22`, with `engine.py:72` (the engine only visits bar days).

**What goes wrong:**
- S4 only reads `posts_on(day)`, and `day` is always a trading day, so a Saturday or Sunday blast is never measured.
- Worse, the weekend posts enter Monday's 30-day baseline and push Monday's ratio under 5x.
- Promoters warm up channels at weekends, before the Monday open.

**Failing input** (`::test_s4_detects_saturday_burst_on_next_session`, `::test_s4_weekend_burst_does_not_hide_monday_burst`):

| Posts | S4 hit |
|---|---|
| 10 hype posts Monday | fires |
| 100 hype posts Saturday | **never fires** |
| 100 Saturday + 10 Monday | **none** |

**Fix:** score every post since the previous session, against a baseline scaled to that span.
```python
i = ctx.index(day)
prev = ctx.days[i - 1] if i else day - timedelta(days=1)
start = prev + timedelta(days=1)            # every post since the previous session
today = ctx.posts_between(start, day)
...
history = ctx.daily_mentions(start, cfg.mention_baseline_days)
base = mean(history) * (day - prev).days if history else 0.0
```

### QA-5: the audit log cannot detect a deleted tail or a re-chained rewrite
**Where:** `audit.py:60-80`.

**What goes wrong:**
- `verify()` only checks that each record links to the previous one.
- **Deleting the last N records** (an embarrassing alert, say) leaves a valid chain.
- With no secret and no external anchor, anyone with file access can **drop or edit records and recompute every hash** using the module's own `_digest`.
- For a product that sells "a record nobody can change", this is the core promise.

**Failing input** (`test_qa_audit.py::test_detects_deleted_tail`, `::test_detects_rechained_rewrite`):
- Write 4 records and keep the first 2: `VerifyResult(ok=True, records=2)`.
- Drop record 1, zero every score and re-chain: `ok=True`.

**Fix:** write a head anchor (record count plus last hash) next to the log on every append, and check it in `verify`. For real protection:
- copy the head somewhere the writer cannot edit (WORM bucket, daily signed e-mail to the customer);
- replace bare SHA-256 with `hmac.new(key, body, sha256)`, using a key held outside the host.
```python
self.head_path = self.path.with_name(self.path.name + ".head")
# append(): after writing the line
self.head_path.write_text(json.dumps({"records": n + 1, "hash": record["hash"]}))
# verify():
res = self._verify_chain()
if res.ok and self.head_path.exists():
    head = json.loads(self.head_path.read_text())
    if head != {"records": res.records, "hash": res.head}:
        return VerifyResult(False, res.records, res.records + 1,
                            "log does not match its head anchor (truncated or rewritten)")
```

### QA-6: invisible Unicode characters defeat hype scoring, near-duplicate detection and cashtags
**Where:**
- `text.py:62-64`: `normalize` keeps format characters.
- `text.py:74`: `extract_cashtags` runs on raw text.
- `text.py:108`: `shingles` strips cashtags before normalising.

**What goes wrong:**
- NFKC does not remove zero-width spaces (U+200B), joiners, or soft hyphens (U+00AD).
- One invisible character inside a word changes its tokens. Hype phrases stop matching, every copy of a template gets different shingles, and a cashtag gets cut short.
- Copy-paste bots can add these at random for free, and readers cannot see them.

**Failing input** (`test_qa_text.py::test_hype_score_ignores_invisible_characters[...]`, `::test_zero_width_spaces_do_not_break_near_duplicate_detection`, `::test_zero_width_inside_cashtag_does_not_yield_wrong_ticker`):

| Input | Observed | Expected |
|---|---|---|
| `hype_score("to the m​oon")` | 0.0 | 0.8 |
| `"to the moo­n"` (soft hyphen) | 0.0 | 0.8 |
| Campaign text with 3 ZWSPs inside words, Jaccard against the original | 0.30 | 1.0 |
| `extract_cashtags("$AB​CD")` | `('AB',)` (a different, real ticker) | `('ABCD',)` |

**Fix:**
```python
QUOTES = str.maketrans({"’": "'", "‘": "'", "ʼ": "'", "“": '"', "”": '"'})

def clean(text: str) -> str:
    """NFKC, drop invisible format characters (Cf), fold typographic quotes."""
    text = unicodedata.normalize("NFKC", text)
    return "".join(c for c in text if unicodedata.category(c) != "Cf").translate(QUOTES)

def normalize(text: str) -> str:
    text = clean(text).lower()
    return re.sub(r"\s+", " ", text).strip()

# extract_cashtags:   CASHTAG.finditer(clean(text))
# shingles:           normalize(CASHTAG.sub(" ", clean(text)))
```
Homoglyphs (Cyrillic `о` for Latin `o`) need a confusables skeleton. That is a counter-measure in RED_TEAM.md, not part of this fix.

### QA-7: an all-zero volume history makes the S1 baseline 1.0, so a single small trade fires
**Where:** `signals/market.py:23-25`. Similar code in S2 is at `market.py:71`.

**What goes wrong:**
- Illiquid OTC names, which are the target universe, often have a median dollar volume of 0.
- `base` is then forced to `1.0`, so the ratio is simply the day's dollar volume.
- Team A's example: a thin stock with 11 of 20 days at zero, then an ordinary $500 day, gives **S1 = 1.0 ("500.0x")**.

**Failing input** (`test_qa_signals.py::test_s1_tiny_trade_after_zero_volume_history_is_not_abnormal`): a $6 stock with 29 days of zero volume, then 1 share traded, gives `S1 strength 0.458, "6.0x"`.

**Fix:** take the baseline from days that traded, require enough of them, and apply a dollar floor (new config field `vol_min_dollar_base = 5_000`).
```python
history = [b.dollar_volume for b in ctx.bars_before(day, cfg.vol_lookback)]
traded = [v for v in history if math.isfinite(v) and v > 0]
if len(history) < cfg.vol_min_history or len(traded) < cfg.vol_min_history // 2:
    return None
base = max(median(traded), cfg.vol_min_dollar_base)
```

### QA-8: an alert up to 30 days before the promotion counts as an early catch and inflates lead time
**Where:** `backtest.py:139, 142, 144`.

**What goes wrong:**
- The catch window starts at `c.start - 30 days`.
- An unrelated alert from a month before any promotion is credited as the catch, and its 30+ day "lead" goes into the median.
- The real, later alert is absorbed as "used". It is neither credited nor counted as false.
- This inflates the two Gate C metrics that matter most (catch rate and lead time).

**Failing input** (`test_qa_backtest.py::test_alert_a_month_before_promotion_is_not_credited_as_early_warning`):
- Case: pump starts 1 March, collapses 5 March.
- Alerts on 1 February and 3 March.
- Observed `lead_days == [33]`. Expected `[2]`.

**Fix:** use a short, explicit pre-start allowance (default 5 days, which covers quiet accumulation). Report anything earlier separately, not as a catch.
```python
def evaluate(..., pre_start_days: int = 5):
    ...
    lo = c.start - timedelta(days=pre_start_days)
```

### QA-9: one alert can be credited to two cases
**Where:** `backtest.py:137-155`.

**What goes wrong:** `used` is filled, but it is never checked.
- A ticker pumped twice in quick succession gets **two catches from one alert**. The second catch gets a lead measured from before the first collapse.
- A legit window (end + 30 days) can reach into a later pump on the same ticker. The same alert is then both a catch and a "legit flagged".

**Failing input** (`::test_one_alert_cannot_catch_two_pumps`, `::test_pump_alert_is_not_also_a_legit_flag`):
- AAA pumps Jan 10 to Feb 1 and Feb 20 to Mar 1, with one alert on Jan 25: observed `caught=2`, expected 1. The second lead is 36 days.
- BBB legit Jan 10 to Feb 10, then pump Mar 1 to Mar 20, with one alert on Mar 5: observed `legit_flagged=1`, expected 0.

**Fix:**
- process cases in date order per ticker;
- start each pump's window after the previous pump's collapse;
- skip alerts already used;
- leave pump windows out of the legit flagging.
```python
for c in sorted(cases, key=lambda c: (c.ticker, c.start)):
    ...
    if c.label == "pump":
        lo = c.start - timedelta(days=pre_start_days)
        if c.ticker in prev_end:
            lo = max(lo, prev_end[c.ticker] + timedelta(days=1))
        prev_end[c.ticker] = c.end
        early = [a for a in ticker_alerts if lo <= a.day < c.end and (c.ticker, a.day) not in used]
    else:
        flagged = [a for a in ticker_alerts
                   if lo <= a.day <= c.end + timedelta(days=lookback_days)
                   and not any(s <= a.day < e for s, e in pump_windows.get(c.ticker, []))]
```

---

## Medium

### QA-10: S6 fires on the first day of a broker feed
**Where:** `signals/client.py:23-24`, `context.py:82-88`.

**What goes wrong:**
- On the first day of the feed there is no baseline, so `base` is `None`, the ratio is `inf`, and `ratio_part` is 1.
- On the day a customer turns the feed on, **every ticker with 20 or more new buyers fires S6 at 0.6 or more**. A median of 0 behaves the same way.
- S4 has the same cold start ("from ~0") on the first day of a post feed. QA-1's as-of coverage reduces that, and RED_TEAM.md S4-1 covers the rest.

**Failing input** (`test_qa_signals.py::test_s6_needs_a_baseline_before_firing`): one flow row with 20 buyers gives `S6 0.6, "20 new buyers (from ~0)"`.

**Fix:** add a new config field `flow_min_history = 10`.
```python
hist = ctx.flow_history(day)              # new_buyers for the 30 days before `day`
if len(hist) < cfg.flow_min_history:
    return None
base = max(sorted(hist)[len(hist) // 2], 1)
ratio = flow.new_buyers / base
```

### QA-11: `verify()` crashes on non-object lines, accepts duplicate keys, and `append()` chains onto a corrupt log
**Where:** `audit.py:36-44` and `audit.py:70-78`.

**What goes wrong:**
- A line `[]`, `5`, `"x"` or `null` raises `TypeError`/`AttributeError` instead of returning `ok=False`.
- A line with a forged first `"alert"` key passes `verify()`, because Python keeps the last duplicate. Yet `grep`, and any parser that keeps the first key, shows the forgery.
- `append()` after a `{"hash": 1}` line chains onto the bad record without complaint.

**Failing input** (`test_qa_audit.py::test_verify_reports_non_object_line_instead_of_crashing[...]`, `::test_verify_rejects_duplicate_keys`, `::test_append_refuses_to_chain_onto_corrupt_log`).

**Fix:**
```python
def _strict_object(pairs):
    out = {}
    for k, v in pairs:
        if k in out:
            raise ValueError(f"duplicate key {k!r}")
        out[k] = v
    return out

rec = json.loads(line, object_pairs_hook=_strict_object)   # ValueError -> VerifyResult(False, ...)
if not isinstance(rec, dict):
    return VerifyResult(False, n, i, "record is not a JSON object")

def _last_hash(self) -> str:
    res = self.verify()
    if not res.ok:
        raise RuntimeError(f"refusing to append to a broken log: line {res.broken_at}: {res.reason}")
    return res.head
```

### QA-12: with zero catches, "false alerts per catch" is the raw false count, so a total miss passes the ≤5 gate
**Where:** `backtest.py:99-101`.

**What goes wrong:**
- With 0 caught and 4 false, `false_per_catch` reports 4.0, which passes `<= 5`.
- So zero-recall thresholds are eligible in calibration.

**Failing input** (`::test_zero_catches_never_pass_false_alert_gate`).

**Fix:**
```python
if self.caught:
    return self.false_alerts / self.caught
return float("inf") if self.false_alerts else 0.0
```

### QA-13: calibration that fails its constraint is not reported, and an empty grid crashes
**Where:** `backtest.py:189-209`.

**What goes wrong:**
- When no threshold meets `max_false_per_catch`, the code silently uses `max(thresholds)`. The report looks exactly like a successful calibration.
- `grid=[]` raises `max() arg is an empty sequence`.

**Failing input** (`::test_report_says_when_no_threshold_met_the_constraint`, `::test_empty_grid_raises_clear_error`).

**Fix:**
- add `constraint_met: bool = True` to `BacktestReport`;
- set it to `best is not None`;
- `if not thresholds: raise ValueError("empty threshold grid")`;
- in `render_markdown`, show a warning banner when `constraint_met` is false.

### QA-14: "Don’t miss" written with a typographic apostrophe scores 0
**Where:** `text.py:62-64`, `text.py:91`.

**What goes wrong:** iOS and most phone keyboards type `’` (U+2019), and NFKC leaves it as is. "Don’t miss" and "DON’T MISS" therefore score 0.0, while "Don't miss" scores 0.7.

**Failing input** (`test_qa_text.py::test_smart_apostrophe_counts_as_hype[...]`).

**Fix:** fold quotes in `clean()`, which is the `QUOTES` table shown in QA-6.

### QA-15: hype phrases match inside other words and ignore negation
**Where:** `text.py:90-92`.

**Failing input** (`::test_hype_phrases_match_whole_words_only[...]`, `::test_negated_guarantee_is_not_hype`):

| Text | Score | Matched phrase |
|---|---|---|
| "download updates here" | 0.7 | "load up" |
| "vipers game tonight" | 0.5 | "vip" |
| "a 10x10 grid" | 0.8 | "10x" |
| "Returns are not guaranteed, do your own research" | 1.0 | "guaranteed" |

The last one is a disclaimer. It is the most promotional message the engine can score.

**Fix:**
- match on word boundaries. Hebrew phrases keep an open start, so prefixes like ו/ה/ל still match;
- fold `-`/`_` to spaces, so "to-the-moon" also matches;
- skip a negated "guaranteed"/"מובטח".
```python
NEGATABLE = {"guaranteed", "מובטח"}
NEGATION = re.compile(r"(?:\bnot|\bno|\bnever|לא)\s+(?:\S+\s+)?$")

t = re.sub(r"[-_]", " ", normalize(text))
for phrase, w in HYPE_PHRASES.items():
    pre = r"(?<!\w)" if phrase[0].isascii() and phrase[0].isalnum() else ""
    post = r"(?!\w)" if phrase[-1].isalnum() else ""
    for m in re.finditer(pre + re.escape(phrase) + post, t):
        if phrase in NEGATABLE and NEGATION.search(t[: m.start()]):
            continue
        miss *= 1.0 - w
        break
```

### QA-16: short generic replies count as a coordinated campaign
**Where:** `text.py:107-111`.

**What goes wrong:**
- A message shorter than k=4 words becomes one whole-message shingle.
- Three people asking "What happened?" (or "Thanks!", or "Bullish $AAA") therefore score Jaccard 1.0, and S5 fires at 0.6.
- This happens on every ticker with an active forum.

**Failing input** (`test_qa_signals.py::test_s5_ignores_short_generic_replies`): 3 Reddit users post "What happened?". Result: `S5 0.6, "3 near-identical messages from 3 different accounts"`.

**Fix:** messages under `k` words produce no shingles. This is part of the QA-20 rewrite below.

### QA-17: the cashtag regex drops Hebrew-prefixed and full-width tags, and truncates class shares
**Where:** `text.py:15`, `text.py:74`.

**What goes wrong:**
- The look-behind `(?<![\w$])` treats Hebrew letters as word characters. "ל$ABC" ("to $ABC") and "ו$ABC" ("and $ABC") therefore give `()`. Attaching these prefix letters is normal Hebrew, and Israeli Telegram groups are an explicit target.
- Full-width `＄ABC` and `$ＡＢＣ` give `()`.
- `$BRK.B` gives `BRK`, which is a different security.

**Failing input** (`test_qa_text.py::test_cashtag_regex_gaps[...]`).

**Already correct, and pinned in `test_cashtag_edge_cases_that_work`:** `$5`, `$1.2M`, `$TSLA's`, `$ABCDEF`, `$$ABC`, case-folding, and Hebrew text with spaces.

**Fix:**
```python
CASHTAG = re.compile(r"(?<![A-Za-z0-9_$])\$([A-Za-z]{1,5}(?:\.[A-Za-z])?)(?![A-Za-z0-9])")
# and run it on clean(text) (QA-6) so full-width forms are folded by NFKC
```

### QA-18: a post listing the same ticker twice is counted twice
**Where:** `context.py:104-106`.

**What goes wrong:**
- Three posts with `tickers=("AAA","AAA")` give `posts_on` = 6. That passes `mention_min_count=5`, and S4 fires.
- A lower-case `("aaa",)` never reaches AAA at all.

**Failing input** (`test_qa_signals.py::test_post_listing_a_ticker_twice_counts_once`).

**Fix:**
```python
for t in dict.fromkeys(x.upper() for x in p.tickers):
    posts[t].append(p)
```

### QA-19: `load_cases` silently loses every case on common CSV variants
**Where:** `backtest.py:43-58`.

**Silent failures (0 cases, no error):**
- an Excel UTF-8 BOM;
- a `Ticker,Label,…` header.

**Crashes and wrong results:**
- `ticker, label` (spaces) raises `KeyError`;
- an indented `  # TODO` row becomes a pump case;
- `$DDD` becomes a case that can never match any data;
- a short row raises `AttributeError`.

**Failing input** (`test_qa_backtest.py::test_load_cases_accepts_common_header_variants[...]`, `::test_load_cases_skips_indented_comments_and_strips_dollar`).

**Fix:** open with `encoding="utf-8-sig"`, then:
```python
reader.fieldnames = [f.strip().lower() for f in reader.fieldnames or []]
missing = {"ticker", "label", "start", "end"} - set(reader.fieldnames)
if missing:
    raise ValueError(f"{path}: missing columns {sorted(missing)}")
for line, row in enumerate(reader, start=2):
    ticker = (row.get("ticker") or "").strip().lstrip("$").upper()
    if not ticker or ticker.startswith("#"):
        continue
    if any(not (row.get(k) or "").strip() for k in ("label", "start", "end")):
        raise ValueError(f"{path}:{line}: incomplete row")
```

### QA-20: the near-duplicate threshold is beaten by a one- or two-word paraphrase
**Where:** `text.py:107-111` and `text.py:120-146` (4-word shingles, Jaccard ≥ 0.6), and `config.py:61`.

**What goes wrong:** with 4-word shingles, each changed word removes up to 4 shared shingles and adds 4 new ones.

**Measured with today's code:**
- Changing **one** word ("before" → "prior to") in an 18-word pitch gives J = **0.55**, below the 0.6 threshold.
- Two evenly spaced edits in a 19-word pitch give 0.36.

Team C's measurements:

| Message length | Evenly spaced edits needed to evade |
|---|---|
| 10 words | 2 |
| 20 words | 2 |
| 40 words | 4 |

LLM "spinning" per account makes this free (see RED_TEAM.md S5-1).

**Failing input** (`test_qa_text.py::test_one_word_paraphrase_still_counts_as_near_duplicate`).

**Fix:** use character 5-grams of the normalised words. Under one-word paraphrase they score 0.78 instead of 0.55, while unrelated messages about the same ticker stay at about 0.46. Keep the minimum-length gate from QA-16.
```python
def shingles(text: str, k: int = 4, n: int = 5) -> frozenset[str]:
    """Character n-grams of the normalised words; messages under k words get none."""
    words = re.findall(r"\w+", normalize(CASHTAG.sub(" ", clean(text))))
    if len(words) < k:
        return frozenset()
    s = " ".join(words)
    return frozenset(s[i : i + n] for i in range(len(s) - n + 1))
```
Re-tune `coord_similarity` on real labelled campaigns before relying on 0.6. For heavier paraphrase, use MinHash with containment, or embeddings; see RED_TEAM.md.

---

## Low

### QA-21: signal memory counts calendar days, not trading sessions
**Where:** `engine.py:77-78`.

**What goes wrong:** a hit on Friday lives for 3 sessions (Fri, Mon, Tue). A hit on Monday lives for 5. Whether a volume spike and the hype that follows it still meet depends on the weekday.

**Failing input** (`test_qa_engine.py::test_memory_lasts_the_same_number_of_sessions_whatever_the_weekday`): Monday spike gives 5 scored sessions, Friday spike gives 3.

**Fix:**
```python
i = ctx.index(day)
if i is not None:  # memory counts trading sessions, not calendar days
    recent = [h for h in recent
              if (j := ctx.index(h.day)) is not None and i - j < cfg.signal_memory_days]
```

### QA-22: duplicate bar dates are scored twice
**Where:** `context.py:27-31`.

**What goes wrong:** a vendor file with a repeated row yields two `DayScore`s for one day. `_bar_index` keeps the last bar, but `days` keeps both.

**Failing input** (`test_qa_engine.py::test_duplicate_bar_dates_score_each_day_once`): 41 scores for 40 distinct days.

**Fix:**
```python
self.bars[:] = sorted({b.day: b for b in self.bars}.values(), key=lambda b: b.day)
```
Logging a warning, or raising, in the loader is better still.

### QA-23: `signal_memory_days=0` silently zeroes every score
**Where:** `engine.py:77`, `config.py:83`.

**What goes wrong:** with memory 0, `horizon = day + 1`, so every hit is discarded. The spike-day score is 0.0 instead of 66.67.

**Failing input** (`::test_zero_signal_memory_is_rejected`).

**Fix:**
```python
def __post_init__(self) -> None:
    if self.signal_memory_days < 1:
        raise ValueError("signal_memory_days must be >= 1")
    if self.cooldown_days < 0 or self.min_families < 1:
        raise ValueError("cooldown_days must be >= 0 and min_families >= 1")
```

### QA-24: the audit `config_hash` does not cover the rule tables
**Where:** `audit.py:83-86`.

**What goes wrong:**
- `NEWS_FORMS`, `DILUTION_FORMS`, `RED_FLAG_TITLE_WORDS`, `HYPE_PHRASES` and `HYPE_EMOJI` all change engine behaviour, but the fingerprint only hashes `Config`.
- Two alerts produced under different rules therefore carry the same `config_hash`.

**Failing input** (`test_qa_audit.py::test_fingerprint_covers_rule_tables`).

**Fix:**
```python
from . import config, text
rules = {"news_forms": sorted(config.NEWS_FORMS), "dilution_forms": sorted(config.DILUTION_FORMS),
         "red_flag_words": list(config.RED_FLAG_TITLE_WORDS),
         "hype_phrases": text.HYPE_PHRASES, "hype_emoji": text.HYPE_EMOJI}
return _digest({**asdict(cfg), "rules": rules})[:16]
```

### QA-25: recall reads 0% when a half contains no pumps
**Where:** `backtest.py:95-97`.

**What goes wrong:** a half with no pump cases reports `recall 0.0`, which looks like total failure. It should read "n/a".

**Failing input** (`::test_recall_is_undefined_without_pumps`).

**Fix:**
- `return self.caught / self.pumps if self.pumps else None`;
- make `summary()` and `render_markdown` print `n/a`.

---

## Behaviour verified correct and now pinned (must stay so)

**No look-ahead:**
- Every signal S1–S7 returns *identical* hits on day D whether or not data after D exists.
- Records after D with extreme values (1e9 volume, 20 bot posts, an 8-K name change, 10,000 new buyers, victim reports) change nothing on or before D.
- At engine level, once every source has started by D, truncating after D changes nothing.
- Tests: `test_qa_no_lookahead.py`.

**Engine:**
- One family alone never alerts, however loud.
- Missing families leave the denominator.
- Cooldown counts from the last *emitted* alert.
- A volume spike and next-day hype meet through memory.
- A news filing on the spike day vetoes S1. This is pinned deliberately, so that fixing the press-release cover evasion is a visible decision.

**Backtest:**
- An alert on or after the collapse day is never a catch.
- Lead is measured to the collapse.
- Legit and unlabelled alerts count as false.
- The split is deterministic, stratified and disjoint for unique tickers.

**Audit:** detects an edit, a reorder, a deleted middle record and a deleted first record.

**Numerics:**
- A single bar and an all-zero price produce no hits.
- A NaN inside S1's *history* (not on the scored bar) does not misfire.

## Observations (real, but not defects with a failing test)

- **Lead time is overstated by up to a day.** Posts and filings carry only a date. So an 8:30 pm post, or an 8-K filed after the close, is used to score that day's close, and a day-D alert gets a D-based lead.
  - Proposal: add `ts: datetime` (UTC) to `Post`/`Filing` and only use records up to the 16:00 ET close.
  - Alternatively, treat date-only records as known on D+1.
  - Also add `min_lead_days=2` (the PLAN's Gate C target) to the definition of "caught".
  - Team B measured the effect: removing the posts dated on the alert day drops that alert's score from 78.6 to 43.6.
- **Legit-mover alerts are double-penalised.** They count both as `legit_flagged` and as `false_alerts`. The module docstring says this is intended, but the report should say so in words.
- **Routine filings keep the corporate family switched on.** An S-8 (employee stock plan) or a Form D keeps S3 at 0.25 for 120 calendar days (about 87 sessions). For most active small caps the corporate family is therefore almost always on, which weakens the two-family rule. See RED_TEAM.md S3-5.
- **Engine-level rules are calibrated on all data.** Only the alert threshold is calibrated on the calibration half. Every other `Config` number and rule table was hand-picked, presumably while looking at the same cases. Freeze `Config` (its fingerprint, QA-24) before the holdout run, and record that in the decision log.

## Suggestions that were refuted or dropped

- **"A NaN in S1 history misfires":** not reproduced. The guard test is kept.
- **"`$5`, `$1.2M`, `$TSLA's`, `$ABCDEF` mis-parse":** all correct today, and pinned.
- **"Cooldown resets on suppressed days":** refuted. `last` only moves on emitted alerts, and this is pinned.
- **"Background (unlabelled) tickers leak between halves":** refuted. They are split disjointly. The only leak is through QA-2.
- **"Lemon squeeze recipe" as a substring bug:** dropped. "squeeze" is a whole word, so word boundaries do not help. It is a vocabulary issue, covered in RED_TEAM.md.
