# Higgsfield API: endpoints we use (from docs.higgsfield.ai, checked 2026-10-07)

Auth: `Authorization: Key KEY_ID:KEY_SECRET`. Env: `HF_KEY="id:secret"`. Async: POST → request_id → poll `/requests/{id}/status`.
Price before running: `POST /estimate/<endpoint>` with the same body (hfgen does this automatically).
Failed or NSFW requests are **not charged**. Outputs live ≥7 days, so hfgen downloads them right away.
Credits expire 1 year after top-up.

| Use | Endpoint ID | Key params |
|---|---|---|
| Start frame / reference image (GPT-Image-class) | `marketing-studio/image/flare` | prompt*, image_urls[] (refs), aspect_ratio `9:16`, resolution `1k/2k/4k`, quality `low…max` |
| Image (photo-real, styles) | `higgsfield-ai/soul/v2/standard` | prompt*, aspect_ratio, resolution 720p/1080p, seed, batch_size 1/4 |
| Video I2V (hero, multi-modal) | `bytedance/seedance-2.5/image-to-video` | image_url*, prompt, duration 4–30, end_image_url, resolution 480p/720p/1080p, generate_audio |
| Video with refs (up to 30 img / 10 vid / 10 audio) | `bytedance/seedance-2.5/reference-to-video` | image_urls/video_urls/audio_urls, prompt, duration, aspect_ratio `9:16` |
| Video T2V | `bytedance/seedance-2.5/text-to-video` | prompt*, duration, aspect_ratio, resolution, generate_audio |
| Video I2V, label/shape lock, start+end frame | `kling-video/v3.0/pro/image-to-video` | image_url*, last_image_url, prompt, duration ≥3, cfg_scale 0–1, sound on/off, multi_prompt[≤6] |
| Video T2V Kling | `kling-video/v3.0/std/text-to-video` | prompt, duration, aspect_ratio, multi_shots |
| Also documented | Seedance 2.5 video-edit / video-extend, Kling 3.0 4K / Turbo, Kling O3 refs, Wan 2.6/2.7, MiniMax, Genjutsu motion-transfer / object-swap / restyle, Soul Cinema, Recraft V4.1, Qwen Image 3 | see the model page |

Always re-check a model page before a big run. Schemas change, and availability depends on the account (check the console).
