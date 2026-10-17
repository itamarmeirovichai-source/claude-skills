# T01 paid test · spend ledger (2026-10-08)

Hard cap: **$4.00**. Runner: copies of `hfgen.py` (md5 d7a564e2…) and `elevenlabs.py` (md5 1681ec44…) taken at the start of the run, executed from the session scratchpad. Auth was through the proxy (`HF_AUTH_VIA_PROXY=1`, `ELEVEN_AUTH_VIA_PROXY=1`). Before every paid job, the plan was schema-linted against `llms-full.txt` (unknown keys, enums, ranges) and estimated free with `hfgen batch --dry-run` and the raw `/estimate`.

## Higgsfield (USD)

| # | Job | Model | Request id | Pre-run estimate | Price source | "Actual" (best available) | Running total (est.) | Running total (cap accounting) |
|---|---|---|---|---|---|---|---|---|
| 1 | T1 K1 | `marketing-studio/image/flare` 2k high 9:16, 2 refs | 8a953000-6647-4c9d-b06d-92a322480353 | $0.300 | hfgen fallback (API returns token rates only) | **unknown**, see the note | 0.300 | 0.490 |
| 2 | T1 K2 | same | 5000b6b0-e23e-4e4f-ad2b-54dd0907f00a | $0.300 | same | **unknown** | 0.600 | 0.980 |
| 3 | T2-A | `kling-video/v3.0/pro/image-to-video` 5 s, sound off | 1ba393c3-a852-4662-b7b4-80280b310f9f | $0.476 | `/estimate` usd (7.616 cr, after a 15 % discount; list $0.56) | $0.476 (fixed price) | 1.076 | 1.456 |
| 4 | T2-B | same | 3007599e-d894-4813-b098-bfcc1b1ce27e | $0.476 | same | $0.476 | 1.552 | 1.932 |
| 5 | T3 | same | 5b831900-d76b-4984-87f5-7e8a5b68762b | $0.476 | same | $0.476 | 2.028 | 2.408 |
| 6 | T4 | `alibaba/qwen-image-3/edit` 2k 9:16 | 0cc769ee-9c24-419a-923d-35851286193b | $0.075 | `/estimate` usd (1.2 cr) | $0.075 | 2.103 | 2.483 |
| 7 | T5 | `bytedance/seedance-2.5/image-to-video` 480p 5 s | a35bba51-655b-4a0a-bc59-645a268c5fc9 | $1.028 | hfgen parse of the per-second description | **$1.023** (token formula on the real 480×850 output: ceil(480·850·5·24/1024) = 47,813 tok × $0.0214/1k) | 3.126 | 3.506 |
| — | Reserve retake | Kling | — | $0.476 | — | **not run** (not justified; see results.md) | — | — |

**Total: estimated $3.13, cap-accounting $3.51.** Both are under $4.00, and no job was submitted that could push the cap-accounting total over $4.00.

**Flare reconciliation (T1): not possible through the API.**
- There is no balance endpoint. `GET /balance`, `/v1/balance`, `/account`, `/me`, `/credits`, `/user` and `/usage` (with and without `/v1/`) all return 405. The docs list only `/estimate`, `/requests/{id}/status|cancel`, `/files/generate-upload-url` and the model routes.
- The completed `status` payload carries no cost or credit field.
- Flare's `/estimate` returns only `pricing_description`: text $5/1M in, image in $8/1M, image out $30/1M. "The initial charge is an estimate reconciled on completion."
- The $0.30 per image is therefore still hfgen's hard-coded fallback.
- For cap accounting I assumed **$0.49 per image** [inf]: gpt-image-1's 6,240 output tokens for a high-quality 1024×1536 image, scaled to the 1520×2688 output, ≈16k tokens × $30/1M, plus about 3k input-image tokens × $8/1M.
- To close T1, read the charge for the two request ids above in the Higgsfield console billing/usage page.

## ElevenLabs (credits only, $0)

| # | Job | Credits used (`character_count`) |
|---|---|---|
| E1 | `eleven_v4` TTS, 12 words + `[softly]`, Jenna, plus one `scribe_v2` STT pass | 5,518 → 5,529 = **11** (≈0.14 credits/char over 77 chars; STT may bill separately as STT time) |
| E2 | `POST /v1/music/plan` (free) then `/v1/music` `music_v2_5` 20 s render | 5,529 → 5,804 = **275** |
