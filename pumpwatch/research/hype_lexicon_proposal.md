# Hype lexicon proposal (HYPE_PHRASES / HYPE_EMOJI)

> Team C (Hype & Coordination Modelling), Detection Science. Written 4 October 2026.
> Status: **proposal only**. Nothing in `src/` was changed. The CEO merges the dict in §7 by hand.
> Anything I could not tie to a source I read is marked **UNVERIFIED**.

---

## 0. Summary

1. **182 phrases** proposed: English 72, Chinese 54 (Simplified + Traditional), Hebrew 24, Korean 22, Japanese 10. Of these, 155 are new (English 47, Hebrew 17, Chinese 54, Korean 22, Japanese 10). 25 English and 7 Hebrew entries are kept, some with new weights. **2 removed**: `"vip"` and `"insider"`. **HYPE_EMOJI**: 5 entries re-weighted and 4 added.
2. **The current lexicon has false positives we measured.** We ran `hype_score()` from the repo on short probe sentences:

   | Probe message | Today | With proposal |
   |---|---|---|
   | `Please download updates before Friday` | 0.70 | 0.50 |
   | `Returns are not guaranteed. Past performance...` | **1.00** | 0.50 |
   | `Insider buying disclosed in Form 4 today` | 0.60 | 0.00 |
   | `Got my vip pass for the concert` | 0.50 | 0.00 |
   | `$GME 🚀🚀🚀` (organic meme post) | **0.94** | 0.73 |
   | `לפי 10 אנליסטים המניה הוגנת` ("according to 10 analysts the stock is fair") | 0.80 | 0.50 |
   | `Fed keeps easy money policy` | 0.90 | 0.60 |

   Every one of these is at or above the S4 cutoff (`hype_min_avg = 0.35`). Changing weights reduces the damage but does not fix it. The real fixes are matching changes (§2), and the CEO decides on those.
3. **The current lexicon misses whole languages.** Today these score 0.00: `跟着老师带单，锁定牛股，稳赚不赔！`, `LINEグループで必ず儲かる銘柄を紹介`, and `我的老师说这只股票要涨`. With the proposal: 0.999, 1.00 and 0.20. That last 0.20 is intended, because 老师 on its own is weak evidence.
4. **A new false-positive risk comes with the new languages: regulator warnings and news about scams.** These now score high, for example `警惕非法荐股骗局，不可能稳赚不赔` → 0.94 and `금감원, 불법 리딩방 수익보장 소비자경보` → 1.00. They use the same words as the scams. §2.4 proposes a "warning context" damper, and the LLM classifier (`llm_classifier_design.md`) has a separate label for them.

---

## 1. How the current matcher behaves (facts from `text.py`)

| Behaviour | Consequence |
|---|---|
| `normalize()` = NFKC + `lower()` + whitespace collapse | Full-width forms fold to ASCII (`１００ｘ` → `100x`, `ＬＩＮＥ` → `line`). So all dict keys **must be lowercase and NFKC-normal**. I checked this programmatically for every key in §7. NFKC does **not** fold `’` (U+2019) to `'`, so `don’t miss` (iOS/Android smart quotes) never matched `don't miss`. Added as separate keys. NFKC also does **not** map Traditional ↔ Simplified Chinese, so both forms are listed. |
| Phrase match is substring `phrase in t` | ASCII short phrases match inside words: `load up` ⊂ "down**load up**dates", `10x` ⊂ "210x"/"10xl", `vip` ⊂ "vipassana". Nested keys **stack**: `guaranteed` + `guaranteed return` both fire. This is intended in 10 places (listed in §7 comments), never by accident. |
| Hebrew | Substring matching *helps* with attached prefixes (ו, ה, ב, ל, ש, כ, מ): `תטוס` matches `שתטוס`, `והמניה תטוס`. But the same mechanism creates collisions: `פי 10` ⊂ `לפי 10` ("according to 10") and `כפי 10`. A naive `\b` word boundary would break prefix handling. See §2.2. |
| Chinese / Japanese / Korean | No spaces, so substring matching is the only option and works. Korean spacing is inconsistent (`수익보장` / `수익 보장`), so both spellings are listed. A cleaner fix is to match Hangul against a whitespace-stripped copy (§2.3). |
| Emoji are counted on the **raw** text, up to 3 each | Three 🚀 alone = 1 − 0.4³ = 0.936. A plain fan post clears the S4 bar with no words at all. |
| `!` is counted on the **raw** text | The full-width `！` used in CJK text is **not** counted, although NFKC would fold it. Fix: count on `normalize(text)` (one-line change). |
| Upper-case cue is ASCII-only (`c.isascii()`) | It never fires for Hebrew/CJK/Korean. These scripts have no case, so this is correct, but they get no "shouting" cue at all. Script-neutral substitutes: repeated punctuation (`!!!`, `！！！`), repeated characters (`冲冲冲`, `가즈아`), digit-heavy "%" claims. **Proposal only.** |
| `CASHTAG` = ASCII `$` + 1–5 letters | Misses most Asian promotion. See §5. |

---

## 2. Matching changes the CEO should consider (not implemented)

These are proposals. They change `text.py` logic, which Team C must not edit.

### 2.1 Word boundaries for Latin-script phrases
Compile ASCII phrases as `(?<![a-z0-9])` + `re.escape(phrase)` + `(?![a-z0-9])`. This kills `download updates`, `210x` and `vipassana`. For CJK/Hangul/Hebrew keep substring matching. **Do not** use `\b`. In Python `re`, `\b` treats CJK and Hebrew letters as word characters, so `\b牛股\b` fails inside `这只牛股要涨`.

### 2.2 Hebrew prefix-aware matching
Proposed pattern for a Hebrew phrase `P`: `(?<![א-ת])(?:[ובהלשכמ]{0,2})P`. This allows up to two attached prefix letters and blocks matches in the middle of a word. For the multiplier phrases (`פי 10`, `פי 100`), also forbid the preceding `ל`/`כ` explicitly, because `לפי`/`כפי` are common words: `(?<![א-ת])(?<!ל)(?<!כ)פי ?10(?!\d)`. Until this ships, `פי 10` is down-weighted to 0.5.

### 2.3 Korean spacing
Match Hangul phrases against `re.sub(r"\s+", "", t)` so `수익 보장`, `수익보장` and `수 익 보 장` (deliberate splitting to evade filters) all hit. Then the duplicate spaced/unspaced keys in §7 can be dropped.

### 2.4 Warning-context damper (most important for the new languages)
Regulators, journalists and victims use exactly the scam vocabulary. Proposed rule: if the message contains a warning cue, multiply the final score by 0.3. Proposed warning cues:
`scam`, `fraud`, `warning`, `beware`, `not guaranteed`, `no guarantee`, `sec charges`, `investor alert`, `הונאה`, `אזהרה`, `רשות ניירות ערך`, `诈骗`, `骗局`, `警惕`, `谨防`, `謹防`, `詐騙`, `證監會`, `证监会`, `사기`, `주의보`, `소비자경보`, `금감원`, `詐欺`, `注意喚起`, `金融庁`.
This damper is *not* the same as negation handling. "不可能稳赚不赔" ("it is impossible to profit without loss") is a warning. "稳赚不赔！" is a pitch. For the long tail, the LLM label `WARNING_OR_VICTIM` (see the classifier design) is the right tool.

### 2.5 Emoji cap
Cap the combined emoji contribution at 0.5, for example `miss *= max(emoji_miss, 0.5)`. Then a post made only of emoji can never pass S4 by itself.

### 2.6 Separate "recruitment" cues from "promotion" cues
Moving a conversation to WhatsApp/Telegram/LINE/VIP rooms is the hallmark of the 2024–2026 ramp-and-dump wave (FBI, FINRA, CSA, FSS, SFC). It is a different behaviour from shouting "to the moon". Today both feed one number. A small structural change would let S5/S7 or a future signal use recruitment separately: a second dict `RECRUIT_PHRASES` with the same saturating sum. **Proposal only.** In §7 the recruitment phrases sit in `HYPE_PHRASES` with comments, so they work today.

---

## 3. Phrase tables with justification, source and false-positive risk

Source keys are in §4. **W** = proposed weight. FP = false-positive risk (L/M/H).

### 3.1 English: existing entries (keep / re-weight / remove)

| Phrase | Old → New W | Reason | Source | FP |
|---|---|---|---|---|
| `to the moon` | 0.8 → 0.6 | Organic retail meme speech (WSB/GME) | [RENAULT], UNVERIFIED for weight | H |
| `10x` | 0.8 → 0.5 | Substring of `210x`, `10xl`, "up 10x since IPO" | measured | H |
| `50x` | 0.9 → 0.7 | Same issue, rarer | measured | M |
| `going parabolic` | 0.9 → 0.8 | Also used descriptively | UNVERIFIED | M |
| `don't miss` / `dont miss` | 0.7 → 0.5 | Generic ad copy; add `don’t miss` (U+2019) | [SEC-RUMORS] urgency | M |
| `last chance` | 0.7 → 0.5 | Generic ad copy | [SEC-RUMORS] urgency | M |
| `load up` | 0.7 → 0.5 | Substring of "download updates" (0.70 measured) | measured | M |
| `buy now` | 0.8 → 0.7 | Pressure cue, also e-commerce spam | [SEC-RUMORS] ("pressure to buy RIGHT NOW") | M |
| `big announcement` | 0.6 → 0.4 | Legit IR/PR language | [FBI-PSA] ("market-moving event") | M |
| `guaranteed` | 1.0 → 0.5 | Disclaimers "not guaranteed" scored 1.0. Specific forms added at 1.0 | measured; [FBI-PSA], [CSA] | H |
| `easy money` | 0.9 → 0.6 | "easy money policy" (macro news) | measured | M |
| `squeeze` | 0.5 → 0.25 | Organic short-squeeze talk | UNVERIFIED for weight | H |
| `target price` / `pt $` | 0.4 → 0.25 | Analyst notes "PT $300 raised by MS"; posting price targets *was* a manipulation device in [SEC-2022-221], so kept at low weight | [SEC-2022-221] | H |
| `vip` | 0.5 → **removed** | "vip pass", "vipassana". Replaced by `vip group/channel/room` | measured | H |
| `insider` | 0.6 → **removed** | "insider buying" (Form 4 news) scored 0.6. Replaced by `inside information`, `insider info` | measured; [FBI-PSA] | H |
| `next tesla`, `next nvidia`, `100x`, `1000%`, `before it explodes`, `about to explode`, `get in now`, `huge news coming`, `undervalued gem`, `hidden gem` | unchanged | Specific to promotion | [RENAULT], [SEC-RUMORS] | L–M |

### 3.2 English: new promotion and pressure cues

| Phrase | W | Justification | Source | FP |
|---|---|---|---|---|
| `guaranteed profit`, `guaranteed return` | 1.0 | Promise of returns, the core red flag (stacks with `guaranteed`) | [FBI-PSA], [CSA] "guaranteed profits" | L |
| `cover your losses`, `cover any losses` | 0.9 | FBI: "guarantees to cover any investor losses" | [FBI-PSA] | L |
| `risk-free`, `risk free` | 0.6 | Promise of no downside | [FBI-PSA] (loss protection) | M ("risk-free rate") |
| `multibagger`, `multi-bagger`, `tenbagger`, `ten bagger` | 0.6 | Promotion slang for 10x stocks | UNVERIFIED (common slang) | M |
| `moonshot` | 0.6 | Promotion slang | UNVERIFIED | M |
| `hot stock` | 0.5 | SEC: "urging investors to buy a hot stock" | [SEC-RUMORS] | M |
| `act fast`, `before it's too late` (+ `’` variant), `get in early` | 0.5–0.6 | Urgency pressure | [SEC-RUMORS], [CSA] "high-pressure tactics" | M |
| `exclusive stock` | 0.6 | "exclusive stock recommendations" | [FBI-PSA] | L |
| `inside information`, `insider info` | 0.8 | "claims access to inside or market-moving information" | [FBI-PSA], [CSA] "non-public information" | M (news about insider-trading cases) |
| `market-moving`, `market moving` | 0.4 | Same | [FBI-PSA] | M |

### 3.3 English: ramp-and-dump / investment-club recruitment (2024–2026)

| Phrase | W | Justification | Source | FP |
|---|---|---|---|---|
| `investment club` | 0.5 | Name used by the schemes | [FBI-PSA] | M (legit clubs, e.g. BetterInvesting) |
| `join our whatsapp`, `join my whatsapp` | 0.85 | Moving the victim to encrypted chat | [FINRA-IGI], [FBI-PSA], [CSA] | L |
| `join our telegram`, `join my telegram` | 0.8 | Same (Telegram is also used by legit communities) | [CSA] | L–M |
| `whatsapp group`, `telegram group` | 0.5 / 0.4 | Weaker form | [FINRA-IGI] | M |
| `vip group`, `vip channel`, `vip room` | 0.7 | Paid/"exclusive" tier | [SZ-CSRC] (加入VIP群), [KB-THINK] (유료 VIP 방); English wording UNVERIFIED | L |
| `trading signals` | 0.4 | "Professor" persona offers "daily trading signals" | [NEWS-WA] (secondary) | M (legit TA/crypto services) |
| `free stock pick` | 0.6 | Free bait before upsell | [KB-THINK] Korean equivalent; English wording UNVERIFIED | M |
| `our analyst` | 0.4 | Impersonated-analyst persona | [FBI-PSA] ("impersonate ... well-known stock analysts" via [WA-DFI]); exact phrase UNVERIFIED | M |
| `professor's assistant` (+ `’`) | 0.6 | "Professor" + "assistant" persona pair | [NEWS-WA], [GMG] (secondary) | L |
| *bare* `teacher`, `assistant`, `professor` | **not added** | Far too common. `teacher's assistant` is a school job title. Leave to the LLM | — | H |
| `institutional account` | 0.5 | Fake "institutional allocation/account" upsell | [NEWS-WA] (secondary) | M |
| `next 3 days`, `next three days` | 0.4 | Short, specific time horizon for the ramp | UNVERIFIED (vocabulary from the brief; consistent with [CSA] "specific date") | M |
| `accumulate before` | 0.7 | "accumulate before [event]" | UNVERIFIED (from the brief) | L |
| `buy together` | 0.6 | Coordinated buying instruction | [CSA] "buy at a specific price and quantity on a specific date"; wording UNVERIFIED | M |
| `don't sell until`, `don’t sell until`, `do not sell until` | 0.8 | "instruct investors not to sell until permission is given" | [FBI-PSA] (via [WA-DFI] summary) | L |
| `send a screenshot`, `send me a screenshot` | 0.5 | Confirmation of purchase | [CSA] "ask for confirmation", [SFC-HK] (screenshots of trading records) | M |

**Deliberately not added** (English): `nfa`/`not financial advice` (organic disclaimer), `i'm adding`/`adding more` (used in [SEC-2022-221] but far too common), `diamond hands` (organic culture), `dyor`.

### 3.4 Hebrew

Context: the ISA warned that self-styled "experts" claim "innovative analysis methods to find safe stocks, including AI" and "authorised information sources", and steer WhatsApp groups into specific stocks [ISA-2023]. Calcalist describes "group managers" posting charts and signals in WhatsApp/Telegram groups [CALCALIST-2024].

| Phrase | W | Justification | Source | FP |
|---|---|---|---|---|
| `תטוס` | 0.9 (unchanged) | "will fly" | existing; UNVERIFIED source | L in ticker-filtered posts |
| `פי 10` | 0.8 → 0.5 | `לפי 10` ("according to 10") collision, measured | measured | H until §2.2 |
| `פי 100` | 1.0 → 0.9 | `לפי 100` collision | measured | M |
| `מובטח` | 1.0 → 0.6 | `לא מובטח` ("not guaranteed"), non-financial "promised". Specific forms below | measured | M |
| `להיכנס עכשיו`, `הזדמנות של פעם בחיים`, `לפני שזה מתפוצץ` | unchanged | Urgency | existing | L |
| `תשואה מובטחת` ("guaranteed return") | 1.0 | Core red flag | [ISA-2023] context; exact ISA wording "תשואה מובטחת" seen only in a search snippet → **UNVERIFIED** | L |
| `רווח מובטח` ("guaranteed profit") | 1.0 | Same | UNVERIFIED | L |
| `מניה בטוחה`, `מניות בטוחות` ("safe stock(s)") | 0.7 | "method to find safe stocks" | [ISA-2023] | M |
| `מידע פנים` ("inside information") | 0.5 | Insider claim. Also the legal term in enforcement news | [ISA-2023] ("authorised information sources"); term UNVERIFIED | M–H |
| `לירח` ("to the moon") | 0.7 | Hebrew calque | UNVERIFIED | L |
| `יטוס` ("will fly", masculine) | 0.4 | Pair to `תטוס`; "he'll fly abroad" FP | UNVERIFIED | M |
| `להתפוצץ` ("to explode") | 0.6 | Pair to `לפני שזה מתפוצץ` | UNVERIFIED | M |
| `ללא סיכון`, `בלי סיכון` ("risk-free") | 0.6 | No-downside promise | UNVERIFIED | M |
| `קבוצת וואטסאפ`, `קבוצת ווטסאפ`, `קבוצת טלגרם` | 0.4 | Recruitment. Two spellings of WhatsApp are common | [ISA-2023], [CALCALIST-2024] | M |
| `קבוצת vip` | 0.7 | Paid tier (normalised lowercase "vip") | UNVERIFIED | L |
| `סיגנלים` ("signals") | 0.4 | Signal groups | [CALCALIST-2024] (topic); Hebrew token UNVERIFIED | M |
| `אל תמכרו` ("don't sell", plural) | 0.6 | Hold instruction (FBI pattern) | UNVERIFIED in Hebrew sources | M |
| `האנליסט שלנו` ("our analyst") | 0.5 | Persona | UNVERIFIED | M |

Hebrew note: the ISA's main framing is *unlicensed advice*. Many legitimate-but-unlicensed Israeli "finfluencer" groups use the same words without any manipulation. Expect lower precision in Hebrew than in Chinese/Korean until we have labelled data.

### 3.5 Chinese (Simplified / Traditional)

Sources: the Shenzhen CSRC bureau (Jun 2025) lists 老师, 专家, 牛股, 内幕消息, "加入VIP群", AI选股, and coded "谐音暗语、唱歌喊票" (homophone code words, "singing out" tickers) [SZ-CSRC]. A CSRC warning (via press) lists personas 股神/大V/老师, "锁定牛股、推荐黑马股", 高中签率, 内幕消息, and "诱导投资者全仓接盘" [CSRC-PRESS]. The HK SFC lists 股票教室, 投資達人, 必賺貼士, 內幕消息 [SFC-HK]. Taiwan police / 165 warn on 穩賺不賠 [TW-CIB], and on ad keywords AI 妖股, 最強黑馬股, 飆股特別通知, 保證獲利 [TW-165].

| Phrase (S / T) | W | Justification | Source | FP |
|---|---|---|---|---|
| 牛股 | 0.5 | "bull stock" pick | [SZ-CSRC] | M (organic forum use) |
| 黑马股 / 黑馬股 | 0.5 | "dark-horse stock" | [CSRC-PRESS], [TW-165] | M |
| 锁定牛股 / 鎖定牛股 | 0.8 | "locked-in bull stock" (stacks with 牛股) | [CSRC-PRESS] | L |
| 内幕消息 / 內幕消息 | 0.8 | Inside-information claim | [SZ-CSRC], [SFC-HK] | M (bare 内幕 *not* added: 内幕交易 enforcement news) |
| 内部消息 / 內部消息 | 0.7 | Variant | UNVERIFIED | M |
| 稳赚 / 穩賺 | 0.9 | Covers 稳赚不赔 | [CSRC-PRESS], [TW-CIB] | M (warnings: needs §2.4) |
| 必赚 / 必賺 | 0.9 | "sure-win" tips | [SFC-HK] (必賺貼士) | M |
| 保证获利 / 保證獲利, 保证收益 / 保證收益 | 1.0 | Guaranteed profit | [TW-165] (保證獲利); 保证收益 UNVERIFIED | L |
| 翻倍 | 0.5 | "double" | UNVERIFIED (brief) | M |
| 拉升 | 0.3 | "pull up" (price). Very common descriptive word ("尾盘拉升") | UNVERIFIED (brief) | H |
| 老师 / 老師 | 0.2 | Persona title, very ambiguous | [SZ-CSRC], [CSRC-PRESS] | H |
| 跟着老师 / 跟著老師 | 0.7 | "follow the teacher" (stacks with 老师) | UNVERIFIED | L |
| 带单 / 帶單 | 0.7 | "leading orders" (group trade calls) | UNVERIFIED (brief). Also used in crypto copy-trading, still promotional | L–M |
| 跟单 / 跟單 | 0.5 | "follow orders" | [CSRC-PRESS] ("集中跟单收割" in a CSRC-cited chain) | M |
| 抄底 | 0.25 | "buy the dip". Extremely common organically | UNVERIFIED (brief) | H |
| 涨停 / 漲停 | 0.3 | "limit-up". Descriptive in A-share talk | UNVERIFIED | H |
| 妖股 | 0.6 | "demon stock" | [TW-165] ("AI 妖股") | M |
| 飙股 / 飆股 | 0.6 | "soaring stock" | [TW-165] ("飆股特別通知") | M |
| 股神 | 0.6 | "stock god" persona | [CSRC-PRESS] | M |
| 炒股大师 / 炒股大師 | 0.6 | "stock master" persona | [CSRC-PRESS] | M |
| 荐股 / 薦股 | 0.4 | "recommending stocks". Also in news about 非法荐股 | [SZ-CSRC] | M–H |
| 股票教室 | 0.7 | "stock classroom" group theme | [SFC-HK] | L |
| 投资达人 / 投資達人 | 0.6 | "investment expert" persona | [SFC-HK] | M |
| vip群 | 0.7 | VIP group | [SZ-CSRC] | L |
| 高中签率 / 高中簽率 | 0.6 | "high IPO allotment rate" bait | [CSRC-PRESS] | M |
| 全仓 / 全倉, 满仓 / 滿倉 | 0.4 | "all-in" | [CSRC-PRESS] (全仓接盘) | M |
| 暴涨 / 暴漲 | 0.4 | "surge" | UNVERIFIED | M (news) |
| 冲冲冲 / 衝衝衝 | 0.4 | Repeated-character "charge!" cheer | UNVERIFIED | M |
| 交割单 / 交割單 | 0.4 | Trade slip shown as "proof" | UNVERIFIED (consistent with [SFC-HK] screenshot red flag) | M |

**Deliberately not added:** 唱高散货 / 唱高散貨 ("pump and dump"). It is the *regulators'* word and appears almost only in warnings. 大V (too generic). 主力 / 庄家 (market-structure talk).
**Evasion warning:** [SZ-CSRC] documents homophone codes and "singing" tickers. A lexicon cannot catch these. They are the strongest case for the LLM classifier and for S5 (copy-paste) and S6 (broker flow).

### 3.6 Korean

Sources: the FSS consumer alert (Apr 2021) on "200% 수익 보장" leading rooms promising to reveal "급등 종목" via "무료 오픈채팅방" [FSS-2021]. FSS "주의" alert (Oct 2025) on illegal overseas-stock leading rooms on Telegram [FSS-2025]. FSS alert (Jan 2026) on "고급 정보", "원금보장", "고수익" bait [FSS-2026]. KB consumer page on "무료로 추천" bait → paid "VIP 방" [KB-THINK].

| Phrase | W | Justification | Source | FP |
|---|---|---|---|---|
| 수익보장, 수익 보장 | 1.0 | Profit guarantee | [FSS-2021], [KB-THINK] | L (warnings → §2.4) |
| 원금보장, 원금 보장 | 0.9 | Principal guarantee | [FSS-2026] | L–M (legit deposit products) |
| 급등주, 급등 종목 | 0.45 | "surging stocks" | [FSS-2021] | M (headlines). *Bare* 급등 not added: "주가 급등" in every market report |
| 리딩방 | 0.6 | "leading room" | [FSS-2021], [FSS-2025] | M (news about 불법 리딩방) |
| 세력주 / 세력 | 0.5 / 0.3 | "operator stock" / "operators". Organic complaint word too | UNVERIFIED (brief) | M / H |
| 작전주 | 0.3 | "manipulated stock". Mostly used by *critics*, so it is a suspicion cue rather than a promotion cue. Better routed to S7-like evidence | UNVERIFIED (brief) | H |
| 무료 추천, 무료로 추천 | 0.5 | Free-pick bait | [KB-THINK] | M |
| 오픈채팅 | 0.4 | Covers 오픈채팅방 | [FSS-2021] | M |
| 텔레그램방 | 0.4 | Telegram room | [FSS-2025] (topic) | M |
| vip방 | 0.7 | Paid VIP room | [KB-THINK] | L |
| 고급 정보, 고급정보 | 0.5 | "premium information" | [FSS-2026] | M |
| 고수익 | 0.4 | "high returns" | [FSS-2026] | M (ads, news) |
| 매수 포착 | 0.4 | From "기관 매수 포착 종목" ("stocks where institutional buying was caught") | search snippet only → **UNVERIFIED** | M |
| 텐배거 | 0.6 | "ten-bagger" | UNVERIFIED | M |
| 떡상 | 0.4 | Slang "skyrocket" | UNVERIFIED | H (organic) |
| 가즈아 | 0.4 | Slang "let's go!" cheer | UNVERIFIED | H (organic, crypto) |

### 3.7 Japanese (added; justified by FSA warnings on SNS→LINE-group investment fraud)

[FSA-JP] describes fake celebrity ads that lead to **LINE groups**, where multiple sock-puppet accounts fake success before specific stock purchases are pushed. Japanese fraud is more often fake-app/deposit fraud than true ramp-and-dumps. Keep weights moderate.

| Phrase | W | Justification | Source | FP |
|---|---|---|---|---|
| 必ず儲かる, 絶対儲かる, 確実に儲かる | 1.0 | "certain to profit" | FSA red-flag words 確実に/必ず/絶対に seen in a search snippet, not on the fetched page → **UNVERIFIED** | L |
| 元本保証 | 0.8 | Principal guarantee | UNVERIFIED | M (legit deposits) |
| lineグループ | 0.5 | Recruitment (NFKC lowercases ＬＩＮＥ) | [FSA-JP] | M |
| 投資グループ | 0.4 | "investment group" | [FSA-JP] (topic) | M |
| 爆上げ, テンバガー, 急騰銘柄 | 0.4–0.6 | Hype slang | UNVERIFIED | M |
| 仕手株 | 0.3 | "manipulated stock", critics' word like 작전주 | UNVERIFIED | H |

**Not added:** 先生 / アシスタント (too generic; same reasoning as English `teacher`/`assistant`).
**Spanish / Portuguese / Russian: not added in this round.** I found no regulator notice in these languages tying a vocabulary to *equity* ramp-and-dumps aimed at our target markets. Russian Telegram "памп" channels are mostly crypto. Revisit once the ingestion layer shows real volume in these languages.

### 3.8 Emoji

| Emoji | Old → New | Reason |
|---|---|---|
| 🚀 | 0.6 → 0.35 | 3 rockets alone = 0.936 today (measured); organic meme use |
| 💎 | 0.3 → 0.15 | "diamond hands" is organic retail culture |
| 🔥 | 0.3 → 0.2 | Generic enthusiasm |
| 💰 | 0.4 → 0.3 | |
| 📈 | 0.2 → 0.15 | Also used by neutral chart posts |
| 🌕 (new) | 0.3 | "moon" |
| 🤑 (new) | 0.4 | Money-face |
| ⏰ (new) | 0.2 | Urgency |
| 📢 (new) | 0.2 | Call-out |

All emoji weights are judgement calls (**UNVERIFIED**) to be re-fitted per §6. Even after this, three 🚀 score 0.73. The emoji cap (§2.5) is the structural fix.

---

## 4. Sources

| Key | Source | Verified how |
|---|---|---|
| [FBI-PSA] | FBI IC3 PSA I-070325-PSA, "Fraudsters Target US Stock Investors through Investment Clubs Accessed on Social Media and Messaging Applications", 3 Jul 2025. https://www.ic3.gov/PSA/2025/PSA250703 | fetched |
| [WA-DFI] | Washington DFI relay of the FBI alert (warning-signs list incl. "not to sell until permission is given"). https://dfi.wa.gov/consumer/alerts/fbi-alert-fraudsters-target-us-stock-investors-through-investment-clubs-accessed | search snippet |
| [FINRA-IGI] | FINRA Investor Insights, "Social Media 'Investment Group' Imposter Scams Continue to Rise" (updated 9 Dec 2025). https://www.finra.org/investors/insights/investment-group-imposter-scams | fetched |
| [CSA] | Canadian Securities Administrators investor alert, "Ramp-and-dump scams surge as fraudulent investment groups target unsuspecting investors". https://www.investright.org/news-and-insights/investor-alerts/csa-investor-alert-ramp-and-dump-scams-surge-as-fraudulent-investment-groups-target-unsuspecting-investors/ (page reported 11 Aug 2026; a Nova Scotia copy is dated 16 Apr 2026: https://nssc.novascotia.ca/sites/default/files/docs/2026-04-16%20CSA%20Investor%20Alert%20Ramp%20and%20Dump%20clean%20cl%20107.pdf. The date discrepancy is UNVERIFIED) | fetched |
| [SEC-RUMORS] | SEC OIEA, "Updated Investor Alert: Social Media and Investing – Stock Rumors". https://www.investor.gov/news-alerts/investor-alerts/updated-investor-alert-social-media-investing-stock-rumors | search snippet (investor.gov returned 403 to our fetcher) |
| [SEC-2022-221] | SEC press release 2022-221, eight social-media influencers, $100M scheme on Twitter/Discord (price targets, "adding" posts). https://www.sec.gov/news/press-release/2022-221 | search snippet |
| [RENAULT] | T. Renault, "Market Manipulation and Suspicious Stock Recommendations on Social Media", EFMA 2017. https://efmaefm.org/0EFMAMEETINGS/EFMA%20ANNUAL%20MEETINGS/2017-Athens/papers/EFMA2017_0387_fullpaper.pdf | search snippet |
| [NEWS-WA] | MalwareTips, "WhatsApp Pump-and-Dump Scam Wipes Out Investors" (professor/assistant/"daily trading signals"/"Wealth Club"). https://malwaretips.com/blogs/?p=410572. Also Herb Greenberg, "Anatomy of a WhatsApp Stock Scam", 8 Jul 2025, https://www.herbgreenberg.com/p/anatomy-of-a-whatsapp-stock-scam. Also The Bear Cave, "Problems in Chinatown", https://thebearcave.substack.com/p/problems-in-chinatown | snippet / fetched (Greenberg) (secondary sources) |
| [GMG] | GoodMoneyGuide forum thread "Professor Vincent (Lisa assistant) WhatsApp Stock Scam". https://goodmoneyguide.com/discussions/topic/stock-scam/ | search snippet (user forum, weak) |
| [ISA-2023] | Bizportal report of the Israel Securities Authority warning (Amir Halmer), 31 Oct 2023. https://www.bizportal.co.il/capitalmarket/news/article/819692 | fetched |
| [CALCALIST-2024] | Calcalist op-ed on unlicensed advice in WhatsApp/Telegram groups, 23 Jan 2024. https://www.calcalist.co.il/local_news/article/b12q01pf6 | fetched |
| [SZ-CSRC] | 深圳证监局 "揭露非法荐股骗局的四大套路", 中证网, 5 Jun 2025. https://cs.com.cn/tj/02/02/202506/t20250605_6494833.html | fetched |
| [CSRC-PRESS] | CSRC warnings as reported by Chinese press (股神/大V/老师, 锁定牛股, 黑马股, 高中签率, 稳赚不赔, 全仓接盘). E.g. https://www.bjnews.com.cn/detail/1787933188189822.html | search snippet; which outlet carries which phrase is **UNVERIFIED** |
| [SFC-HK] | HK SFC leaflet "慎防社交媒體投資詐騙". https://sfc.hk/web/files/gdn/index.html | fetched |
| [TW-165] | Taiwan 165 anti-fraud ad keywords (AI 妖股, 最強黑馬股, 飆股特別通知, 保證獲利, 穩賺不賠) | search snippet only, page not identified → **UNVERIFIED** |
| [TW-CIB] | PTS News, Criminal Investigation Bureau bust of a LINE-account fake-investment ring, 8 Sep 2026 ("穩賺不賠"). https://news.pts.org.tw/article/826031 | fetched |
| [FSS-2021] | 이투데이, "'200% 수익보장' 주식리딩방…소비자경보 '주의' 발령", 5 Apr 2021. https://www.etoday.co.kr/news/view/2012048 | fetched |
| [FSS-2025] | SBS Biz, FSS "주의" alert on illegal overseas-stock leading rooms, 29 Oct 2025. https://biz.sbs.co.kr/amp/article/20000268461 | fetched |
| [FSS-2026] | 한국경제, FSS consumer alert, 26 Jan 2026 (고급 정보, 원금보장, 고수익). https://www.hankyung.com/article/202601263694i | fetched |
| [KB-THINK] | KB Think, "주식 리딩방 사기 유형과 예방법". https://kbthink.com/fraud/stock-tipping-scam.html | search snippet |
| [FSA-JP] | 金融庁 "SNS等を利用した投資詐欺にご注意ください" (updated 17 Apr 2025). https://www.fsa.go.jp/ordinary/chuui/sns.html | fetched |

---

## 5. Tickers without cashtags (proposal, not implemented)

`CASHTAG = (?<![\w$])\$([A-Za-z]{1,5})(?![A-Za-z])` only sees `$ABC`. What it misses:

| Market / habit | Example | Proposed handling |
|---|---|---|
| A-shares: 6-digit codes | `600519`, `000001`, `300750`, `688xxx` | Regex `(?<!\d)(?:60[0135]\|00[0-3]\|30[01]\|68[89])\d{3}(?!\d)`. Accept only if (a) the code is in a reference universe and (b) a stock word (股, 代码, 买入, 板) appears within ±10 characters. Otherwise phone numbers and amounts pollute it. |
| HK: 4–5 digits | `0700`, `00700.HK`, `9988` | `(?<!\d)\d{4,5}(?:\.hk)?(?!\d)` + universe + context words (港股, 號, 股). |
| Korea: 6-digit | `005930` | Same approach. Also a **name dictionary** (삼성전자 → 005930), because Korean chatter mostly uses names. |
| Japan: 4-digit (now alphanumeric too) | `7203`, `285A` | Universe + context words (銘柄, コード, 株). |
| TASE | Hebrew company names, English tickers without `$` | Hebrew name/alias dictionary from TASE listings, matched with the §2.2 prefix rule. |
| US microcaps named in Chinese/Korean/Hebrew posts | "JYD", "杰玉德", "J Y D", "J-Y-D" | (1) bare uppercase ticker with a universe check: `\b[A-Z]{2,5}\b` only when the token is a microcap in the universe *and* a stock-context word is nearby; (2) de-obfuscation: collapse `J Y D`, `J.Y.D`, `J-Y-D`; (3) local-script name aliases from the issuer's prospectus/press. |
| Coded / sung tickers ([SZ-CSRC]) | homophones, images, voice notes | Out of scope for regex. LLM extraction (ask the model for `tickers_mentioned`) on text; OCR/ASR is a separate project. |

Design notes: (a) `Post.tickers` is filled **upstream** at ingestion (`context.py` indexes posts by `p.tickers`), so resolution belongs in a `resolve_tickers(text, universe, market)` step in the adapters, not in the signals. (b) Every resolution should record *how* it matched (cashtag / code / alias / llm) for audit. (c) Keep false matches low by always requiring the universe check. A random 6-digit number is far more often a price or a phone number than a ticker.

---

## 6. Evaluation plan for the lexicon

**Data.** A stratified gold set of **~3,000 messages**: about 600 each for EN, ZH (S+T), KO, HE, and a smaller JA slice (~300) plus mixed-language. Within each language, sample from:
(i) messages on tickers in known ramp-and-dump cases (SEC/DOJ complaints, FINRA/FBI-named issuers, the 2025 China-based Nasdaq microcaps) inside the 30 days before the collapse;
(ii) random ticker-tagged messages from the same sources on normal days;
(iii) **adversarial negatives**: regulator warnings, news about scams, victims' complaints, legitimate analyst notes, WSB/meme posts;
(iv) messages that fire ≥1 lexicon entry (enriches rare phrases).
Record the sampling weights so we can re-weight to population precision.

**Labels.** Use the same taxonomy as the LLM design (PROMOTION_PUMP, SCAM_RECRUITMENT, ORGANIC_BULLISH, ORGANIC_BEARISH_NEUTRAL, NEWS_REPOST, WARNING_OR_VICTIM, UNRELATED). Binary target for the lexicon: *promotional* = PROMOTION_PUMP ∪ SCAM_RECRUITMENT. Two native-speaker annotators per message. Report Cohen's κ per language (target ≥ 0.7 on the binary target) and adjudicate disagreements.

**Metrics.**
1. **Per-phrase firing precision.** For each key: (# promotional among messages where it fires) / (# fires), with a Wilson 95% interval. Rule: a phrase needs ≥ 30 fires to be judged. Drop or down-weight any phrase whose upper CI bound is < 0.3. Flag any phrase with < 30 fires as "unproven".
2. **Message-level PR curve** of `hype_score` per language. Report precision/recall at 0.35 (the S4 cutoff) and the threshold that gives precision ≥ 0.8.
3. **Day-level S4 effect.** Rerun `backtest.py` with old vs new lexicon. Track hits on known cases, S4 hits on clean tickers, and the change in alert-level false positives (the H4 metric in RESEARCH.md).
4. **Weight fitting.** `hype_score` is exactly a *noisy-OR* model: P(promo) = 1 − ∏(1 − wᵢ). So weights can be fitted by maximum likelihood on the gold set (parametrise wᵢ = sigmoid(θᵢ), L2-regularised toward the hand weights). That keeps the deterministic, explainable form. Refit quarterly. Version the dict and record its hash in the audit log (as `engine_version` suffix or config fingerprint).
5. **Slices.** Per language, per source (Telegram/X/StockTwits/Reddit), and adversarial slice (warnings/news). The adversarial slice is where the §2.4 damper must prove itself.

**Source terms (pending lawyer review).** Team B reports that Telegram's API Terms forbid using Telegram data for AI/ML models, and that Reddit and Discord restrict ML use without permission. Human labelling and measuring precision on such messages are probably fine. *Fitting* lexicon weights on them (step 4 above) may count as ML training. Until a lawyer signs off, run step 4 only on messages from cleared sources, and report the Telegram/Reddit/Discord slices as evaluation only. See `llm_classifier_design.md` §1b.

**Acceptance gate for merging.** Overall promotional precision at 0.35 ≥ the current lexicon's on EN. No language has message-level precision < 0.5 at 0.35. Adversarial-slice mean score < 0.35.

---

## 7. Ready-to-paste dict (replace the two dicts in `text.py`)

Checked by script: 182 phrase keys, 9 emoji keys, no duplicate keys, every key equals `normalize(key)`, all weights within [0, 1]. Intentional nested (stacking) pairs: `guaranteed`⊂`guaranteed profit/return`, `פי 10`⊂`פי 100`, `מובטח`⊂`תשואה מובטחת`/`רווח מובטח`, `牛股`⊂`锁定牛股`/`鎖定牛股`, `老师`⊂`跟着老师`, `老師`⊂`跟著老師`, `세력`⊂`세력주`.

```python
# Weighted hype phrases. Keys MUST be lowercase and NFKC-normalised because
# hype_score() matches them as substrings of normalize(text). Chinese is listed
# in both Simplified and Traditional forms (NFKC does not convert between them).
# Recruitment cues (moving victims to WhatsApp/Telegram/LINE/VIP rooms) are
# included here until a separate RECRUIT_PHRASES list exists.
HYPE_PHRASES: dict[str, float] = {
    # ---- English: classic promotion (existing entries, some re-weighted) ----
    "to the moon": 0.6,
    "next tesla": 0.9,
    "next nvidia": 0.9,
    "100x": 1.0,
    "50x": 0.7,
    "10x": 0.5,
    "1000%": 0.9,
    "going parabolic": 0.8,
    "before it explodes": 1.0,
    "about to explode": 1.0,
    "don't miss": 0.5,
    "don’t miss": 0.5,
    "dont miss": 0.5,
    "last chance": 0.5,
    "load up": 0.5,
    "buy now": 0.7,
    "get in now": 0.9,
    "huge news coming": 1.0,
    "big announcement": 0.4,
    "guaranteed": 0.5,
    "easy money": 0.6,
    "squeeze": 0.25,
    "undervalued gem": 0.7,
    "hidden gem": 0.6,
    "target price": 0.25,
    "pt $": 0.25,
    # ---- English: new promotion / pressure cues ----
    "guaranteed profit": 1.0,
    "guaranteed return": 1.0,
    "cover your losses": 0.9,
    "cover any losses": 0.9,
    "risk-free": 0.6,
    "risk free": 0.6,
    "multibagger": 0.6,
    "multi-bagger": 0.6,
    "tenbagger": 0.6,
    "ten bagger": 0.6,
    "moonshot": 0.6,
    "hot stock": 0.5,
    "act fast": 0.5,
    "before it's too late": 0.6,
    "before it’s too late": 0.6,
    "get in early": 0.6,
    "exclusive stock": 0.6,
    "inside information": 0.8,
    "insider info": 0.8,
    "market-moving": 0.4,
    "market moving": 0.4,
    # ---- English: ramp-and-dump / investment-club recruitment ----
    "investment club": 0.5,
    "join our whatsapp": 0.85,
    "join my whatsapp": 0.85,
    "join our telegram": 0.8,
    "join my telegram": 0.8,
    "whatsapp group": 0.5,
    "telegram group": 0.4,
    "vip group": 0.7,
    "vip channel": 0.7,
    "vip room": 0.7,
    "trading signals": 0.4,
    "free stock pick": 0.6,
    "our analyst": 0.4,
    "professor's assistant": 0.6,
    "professor’s assistant": 0.6,
    "institutional account": 0.5,
    "next 3 days": 0.4,
    "next three days": 0.4,
    "accumulate before": 0.7,
    "buy together": 0.6,
    "don't sell until": 0.8,
    "don’t sell until": 0.8,
    "do not sell until": 0.8,
    "send a screenshot": 0.5,
    "send me a screenshot": 0.5,
    # ---- Hebrew (existing entries, some re-weighted) ----
    "תטוס": 0.9,
    "פי 10": 0.5,
    "פי 100": 0.9,
    "להיכנס עכשיו": 0.9,
    "הזדמנות של פעם בחיים": 1.0,
    "מובטח": 0.6,
    "לפני שזה מתפוצץ": 1.0,
    # ---- Hebrew: new ----
    "תשואה מובטחת": 1.0,
    "רווח מובטח": 1.0,
    "מניה בטוחה": 0.7,
    "מניות בטוחות": 0.7,
    "מידע פנים": 0.5,
    "לירח": 0.7,
    "יטוס": 0.4,
    "להתפוצץ": 0.6,
    "ללא סיכון": 0.6,
    "בלי סיכון": 0.6,
    "קבוצת וואטסאפ": 0.4,
    "קבוצת ווטסאפ": 0.4,
    "קבוצת טלגרם": 0.4,
    "קבוצת vip": 0.7,
    "סיגנלים": 0.4,
    "אל תמכרו": 0.6,
    "האנליסט שלנו": 0.5,
    # ---- Chinese (Simplified / Traditional) ----
    "牛股": 0.5,
    "黑马股": 0.5,
    "黑馬股": 0.5,
    "锁定牛股": 0.8,
    "鎖定牛股": 0.8,
    "内幕消息": 0.8,
    "內幕消息": 0.8,
    "内部消息": 0.7,
    "內部消息": 0.7,
    "稳赚": 0.9,
    "穩賺": 0.9,
    "必赚": 0.9,
    "必賺": 0.9,
    "保证获利": 1.0,
    "保證獲利": 1.0,
    "保证收益": 1.0,
    "保證收益": 1.0,
    "翻倍": 0.5,
    "拉升": 0.3,
    "老师": 0.2,
    "老師": 0.2,
    "跟着老师": 0.7,
    "跟著老師": 0.7,
    "带单": 0.7,
    "帶單": 0.7,
    "跟单": 0.5,
    "跟單": 0.5,
    "抄底": 0.25,
    "涨停": 0.3,
    "漲停": 0.3,
    "妖股": 0.6,
    "飙股": 0.6,
    "飆股": 0.6,
    "股神": 0.6,
    "炒股大师": 0.6,
    "炒股大師": 0.6,
    "荐股": 0.4,
    "薦股": 0.4,
    "股票教室": 0.7,
    "投资达人": 0.6,
    "投資達人": 0.6,
    "vip群": 0.7,
    "高中签率": 0.6,
    "高中簽率": 0.6,
    "全仓": 0.4,
    "全倉": 0.4,
    "满仓": 0.4,
    "滿倉": 0.4,
    "暴涨": 0.4,
    "暴漲": 0.4,
    "冲冲冲": 0.4,
    "衝衝衝": 0.4,
    "交割单": 0.4,
    "交割單": 0.4,
    # ---- Korean ----
    "수익보장": 1.0,
    "수익 보장": 1.0,
    "원금보장": 0.9,
    "원금 보장": 0.9,
    "급등주": 0.45,
    "급등 종목": 0.45,
    "리딩방": 0.6,
    "세력주": 0.5,
    "세력": 0.3,
    "작전주": 0.3,
    "무료 추천": 0.5,
    "무료로 추천": 0.5,
    "오픈채팅": 0.4,
    "텔레그램방": 0.4,
    "vip방": 0.7,
    "고급 정보": 0.5,
    "고급정보": 0.5,
    "고수익": 0.4,
    "매수 포착": 0.4,
    "텐배거": 0.6,
    "떡상": 0.4,
    "가즈아": 0.4,
    # ---- Japanese ----
    "必ず儲かる": 1.0,
    "絶対儲かる": 1.0,
    "確実に儲かる": 1.0,
    "元本保証": 0.8,
    "lineグループ": 0.5,
    "投資グループ": 0.4,
    "爆上げ": 0.5,
    "テンバガー": 0.6,
    "急騰銘柄": 0.4,
    "仕手株": 0.3,
}

HYPE_EMOJI: dict[str, float] = {
    "🚀": 0.35,
    "💎": 0.15,
    "🔥": 0.2,
    "💰": 0.3,
    "📈": 0.15,
    "🌕": 0.3,
    "🤑": 0.4,
    "⏰": 0.2,
    "📢": 0.2,
}
```

**Merge checklist for the CEO.**
(1) No current test pins lexicon weights. I pasted this dict into a scratch copy of the repo and the existing suite still passed (`tests/`, 18 passed). Be aware that a message containing only `vip` or `insider` now scores 0.
(2) Re-run `backtest.py`. S4 recall on Asian-language cases should rise. S4 false positives from regulator-warning posts *will* rise until §2.4 lands. Consider merging §2.4 together with this dict.
(3) Record the dict version (e.g. `lexicon=2026-10-04`) in the audit trail.
