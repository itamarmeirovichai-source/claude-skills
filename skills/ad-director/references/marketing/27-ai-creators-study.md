# 27 — AI-ad creators study: what the other top creators do (beyond Rourke Heath)

Researched 2026-10-08. A smaller-scale version of the Rourke study (`14-rourke-heath-study.md`) for the other creators who make or teach AI product commercials. Numbers are public TikTok counters on the research date or the creators' own claims. `[inf]` marks my inference.

## Method and coverage

**Pipeline (same as study 14):** profile page → `secUid` → TikTok web `api/creator/item_list` (`count=15`, `type=1`, `cursor`=ms timestamp, paged back) → rank 2025–26 posts by plays and ad relevance → `yt-dlp` per video, 4 s apart → 12-frame timestamped sheet + 0–3 s hook strip (6 frames at 0.5 s) → faster-whisper `small` (auto-language) → sharp full-res grabs wherever a prompt is on screen. Captions were read in full: several creators paste the whole prompt into the caption. Videos were deleted after viewing. Sheets, hook strips and transcripts are in the session scratchpad (`creators/<handle>/`, not committed).

**Processed: 43 TikToks across 8 creators**, listing 2,749 public posts in total. URL pattern: `https://www.tiktok.com/@<handle>/video/<id>`.

| Creator | TikTok handle | Followers | Posts listed | Median plays 2025–26 | Processed |
|---|---|---|---|---|---|
| PJ Accetturo ("PJ Ace", Genre.ai) | pjacefilms | 22k | 25 | 13k | 6 |
| Karen X. Cheng | karenxcheng | 1.02M | 298 | 12.7k | 6 |
| BYRVM (editing / AI tools) | byrvm_contentcreation | 405k | 298 | 8.8k | 6 |
| Cristian Andrade (Crisan) | crisanvisual | 217k | 275 | 18k | 5 |
| Ozan Sihay (TR director) | ozansihay | 190k | 865 | 20k | 5 |
| Jack Vs. AI | jackvsai | 3.6k | 62 | 1.5k | 6 |
| KC "Create Smarter With AI" | billionheirkc | 45k | 404 | 1k | 5 |
| AI Video School | aivideoschool | 11.6k | 200 | 1k | 4 |

**Named in our files but NOT on TikTok (probed 40+ handle variants; HTTP status 10221 = no such user, or empty accounts):** Dan Kieft (YouTube 304k; IG @dan.kieft), Youri van Hofwegen (YouTube 330k), Tao Prompts (YouTube 196k), Rory Flynn (X/IG; `@rory.flynn` on TikTok has 0 videos), Dave Clark (`@diesol` 0 videos), Billy Boman (0 videos), Curious Refuge (TikTok dormant since Feb 2024). For these I used YouTube **listing metadata only** (titles and view counts via `yt-dlp --flat-playlist`), our earlier notes, and web articles.

**Inaccessible:**
- **YouTube video, subtitles and watch pages:** "Sign in to confirm you're not a bot" / HTTP 401. I did not work around it. This blocks Dan Kieft, Youri and Tao content beyond titles.
- **Instagram:** the public `web_profile_info` endpoint returned 401 `require_login`; yt-dlp got 429. Never logged in. That means no IG reels for PJ Ace, Rory Flynn, Dave Clark, Dan Kieft or Karen.
- **TikTok search and discover pages** render client-side (no creator data without a signed request), so I found creators through web search, our files and handle probing instead.
- **Gated prompt PDFs** (all "Comment X" DMs, link-in-bio, Skool/Stan Store) and **X/LinkedIn breakdown threads** (PJ Ace).
- One download hit a 502 and succeeded on retry. No other failures.

---

## 1. PJ Accetturo — the "absurd vignette" commercial (Genre.ai)

**Who:** He runs Genre.ai, an AI ad studio with clients such as Kalshi, Popeyes and Lindy. His TikTok bio reads "315M+ views on X / IG / YT". TikTok is a minor channel for him: 25 posts, most of them repurposed from X.

**Processed:** 7511268853129809183 (Bible influencers, 4.8M), 7613909444975414558 (Red Rising fan trailer, Seedance 2.0, 193k), 7624226546307353886 (AI on the Lot promo, Dreamina CPP, 13k), 7515324663946317087 (the Kalshi NBA Finals ad, 12k), 7538130214031756575 (Lindy ad, 7k), 7515325379071003935 (Kalshi "BTS", 6k).

**Format (frames):** Every post is a **16:9 film letterboxed in a 9:16 frame**, with a fixed 1–2 line white title in the black top bar ("If Bible characters were influencers 😂", "This is the most unhinged AI ad you've ever seen 😂", "Insane Seedance 2.0 film 😂 Prompts in the comments 👇"). There is no talking head, no UI and no captions. The 0–3 s hook is the single most absurd frame of the piece, then a hard cut at about 2 s: a grinning Jesus taking a selfie on the cross, a businessman smashing through a skyscraper window, a skater flipping off the Hollywood sign.

**Signature techniques:**
1. **"Crazy people in crazy situations" vignette montage.** The Kalshi spot is a rapid montage of 10+ characters in a vox-pop format (an old man in a flag cape at a game, a pool party, a manatee pool), each giving a one-liner about what they bet on, ending on "Kalshi let you legally trade on anything, anywhere in the US". The brand supplied the lines and PJ invented the characters around them (press coverage: Yahoo/AOL, Marktechpost).
2. **The fake BTS as a second ad.** 7515325379071003935 is an AI-generated "making-of" built from the same assets: an AI film crew on a speedboat ("DAY 1 10:45AM"), lower-third interviews with invented staff ("Matthew MacKay, Florida Fish and Wildlife Commissioner", "Kenneth Bertron, Kalshi CFO"), and deadpan jokes ("Most sets have medics, but we have coroners and priests on standby"; "Nobody knows why we're over budget… Sequoia's gonna kill us"). It is a mockumentary that doubles the ad's lifespan.
3. **Brand as a prop in every shot** [inf from frames]. AI on the Lot: the conference ticket in a bikini girl's hand, the badge on a pit bull's collar, then a logo end card. Lindy: a "LINDY FEVER SWEEPS THE NATION" news chyron, a Times Square billboard, a parachute.
4. **Anachronism selfie-vlog** (Bible influencers): biblical characters vlog in Gen-Z slang ("Day two in the tomb. No Wi-Fi. No snacks. Just kind of waiting for God to respawn me."). This is a format, not a product, and it got 4.8M views.

**Workflow (his caption, verbatim):** "1. Basic Script with ChatGPT (or Gemini/Grok, etc.) 2. Expand to Shot list using my prompt structure 3. Paste into Veo 3 and choose favorites. 4. Edit in Final Cut/Capcut, etc." For Kalshi (press quotes): Gemini pitches ideas, then he asks it to convert every shot into a Veo 3 prompt: "I always tell it to return 5 prompts at a time — any more than that and the quality starts to slip." It took "about 300–400 generations to get 15 usable clips", "one person, 2–3 days", about **$2,000**. The Lindy caption tags Midjourney, Kling and Veo 3.

**Verbatim Veo 3 prompt (caption of 7511268853129809183):**
> "A cinematic handheld selfie-style video shot, showing a soggy, exhausted Middle Eastern man in his 30s with shoulder-length wet hair, a tangled beard, and shredded linen robes clinging to his frame. He's seated awkwardly on a slick, uneven surface deep inside the belly of a massive sea creature. The fleshy, ribbed walls pulse slightly around him, dimly lit by a faint blue-green glow coming from slits in the whale's tissue above. Water drips steadily in the background. He holds the camera close, his face lit softly by the glow, his expression weary and mildly guilty. He talks with a country accent. He says: "Update, still swallowed. I would like to formally apologize to God, the sailors, and this whale, sorry dude, I just took a poop over there." He glances offscreen and winces slightly, then gives the camera a sheepish shrug before shifting uncomfortably. Time of Day: indeterminate interior, faint bioluminescent glow from above Lens: natural wide framing, dim exposure optimized for low light and moisture POV: Selfie camera held close to face, angled upward slightly to capture Jonah and the ribbed organic chamber behind him Audio: (implied) dripping water, faint groaning of the whale's body, distant liquid movement Background: wet, fleshy whale interior with ribbed walls and dim, humid atmosphere"

Structure: a prose paragraph (subject, place, light, action, accent, quoted line, a beat after the line), then labelled tails: `Time of Day / Lens / POV / Audio / Background`.

**Business model:** He uses viral spec and IP work (Bible, Red Rising, "Nexus" hybrid feature) as the funnel for Genre.ai brand deals, gets tool-partner access (Dreamina CPP), and publishes breakdowns on X and his newsletter. He does not sell courses on TikTok.

---

## 2. Karen X. Cheng — tactile hybrid: AI frames printed and animated by hand

**Who:** 1.02M TikTok followers. A director with a small team credited in every caption (producer, typography, SFX). Almost all 2025–26 hits are **paid tool partnerships**: Google Chrome (#sponsored, 147.7M plays, almost certainly boosted [inf]), Adobe Firefly (9.4M, 4.4M, 821k), Higgsfield, LEGO and Southwest.

**Processed:** 7574518094220037407 (Chrome/Gemini, 147.7M), 7566323874392968479 (Firefly horse stop-motion teaser, 9.4M), 7470991309696748830 (Firefly collage stop-motion, 4.4M), 7567079567425359135 (horse tutorial, 821k), 7615785387679550751 (Higgsfield "pendulum effect", 139k), 7572294064066825502 (Southwest ad BTS, 7k).

**Signature techniques:**
1. **Print the AI frames and animate them physically.** Nano Banana makes the still ("put this woman on a horse in the desert, side view"), Veo 3.1 animates it ("the horse gallops across the scene, and out of frame on the right side", both verbatim from the caption), she **prints the frames on paper, cuts them out with an X-Acto knife and shoots stop-motion on a tripod**. The result is AI motion with handmade texture that nobody reads as "AI slop" [inf].
2. **"Roommate POV" lo-fi hook.** The 9.4M teaser opens on a shaky phone shot captioned "what is my roommate doing", with Karen surrounded by printouts. The process is the hook; the payoff comes at 0:07.
3. **Generative fill as prop budget.** Firefly Generative Expand "to stretch the image", Insert for balloon, kite and umbrella "to save money on props", and Remove Background "to generate a new one" behind the real subject, all composited into a collage on a cork board.
4. **"Day N of extremely easy edits" series** (Higgsfield-sponsored). The pendulum effect: one photo, then Higgsfield Create Video, preset **AERIAL PULLBACK**, Kling 2.6, 5 s, audio on, 10 credits. Prompt on screen, verbatim: "the person is standing still. There are no people in the background. Camera movement is a drone shot that pulls upwards." In CapCut: duplicate the clip and reverse the copy.
5. **Hand-drawn storyboard first** (frame 0:05 of 7567079567425359135), then "Step 1 / Step 2 / Step 3" red tags on screen.
6. **Southwest Getaways ad:** a fully handmade paper-collage stop-motion with airline tickets, passport stamps and postcards. The brand assets (boarding pass, logo plane) are physical props.

**On-screen prompt** (Gemini in Chrome, 147.7M video): "i'm debating between these locations for a photoshoot. i'm making a tunnel book, so i need strong foreground, mid ground, and backg[round]".

**Typography:** kinetic single words in mixed serif/sans ("so when i was", "BUT", "Conservatory", "window of time"). No word-by-word captions.

**Business model:** brand-commissioned "tutorial ads" in which the tutorial is the ad. Team credits suggest a small studio [inf].

---

## 3. BYRVM — the "HOW TO MAKE THIS" product-transition tutorial machine

**Who:** 405k followers, about 1.6k videos, a median of 8.8k plays (2025–26). Nearly every post is a **sponsored tool tutorial** (Pollo AI, Kling, CapCut, Creatify, Lovart, TapNow), with a ManyChat "Comment KLING / WORKFLOW / CAN / TAP" CTA.

**Processed:** 7581824072128941344 (Kling O1 v2v, 890k), 7624174222507560224 (floating sneaker, 352k), 7641635356873329952 (PRIME bottle splash, TapNow, 135k), 7587845196348394784 (Coke "Flavorship", CapCut, 19k), 7663083261018557729 (golf → product, Creatify, 16k), 7659734798683917601 (can match-cut, Lovart, 12k).

**Fixed template (hook strips of all 6 posts):** the top half is him reacting ("wait", "okay", hands up) with a big condensed "HOW TO MAKE THIS" title. Below it, an **inset card plays the finished result** for the first 3 s. Then a phone or desktop UI walkthrough with one big kinetic word per beat ("select", "detailed", "duration", "hope"), and the result again at the end.

**Signature techniques:**
1. **Real → AI → real sandwich.** Film a real clip holding the product, **screenshot the frame where the product is fully in frame**, have Nano Banana Pro turn that screenshot into "the next cinematic shot", connect the screenshot (start) to the generated image (end) in Seedance 2.0, repeat scene by scene, and stitch. His caption: "most AI videos are still missing one thing: humanity. So instead of generating everything from scratch, I filmed a real clip first."
2. **Variations → same motion → match-cut** (Lovart): generate several variations "keeping the same person, pose, and composition", animate one with a rotating 3D move, "recreate the exact same motion for every scene", then "combine all generated clips into one fast-paced match-cut sequence while preserving the exact same camera movement throughout."
3. **Flavor-shift** (Coke can): one packshot gives N flavor variants (pomegranate, lemon) with matching ingredient splash, cut on the beat with kinetic text "THIS EFFECT I CALL THE FLAVOR SHIFT".
4. **Product-interior fly-through** (sneaker): floating product still → Kling 3.0, 5–10 s, with a prompt to fly "into the shoe through mesh and lace openings, transitioning into a full interior fly-through with hyper-detailed macro textures. Inside, motion alternates between high-speed bursts and controlled slow[-motion]…" (on-screen fragment).
5. **Text behind the subject** over real footage between AI shots (Creatify golf piece).

**On-screen prompt fragments (verbatim):**
- Nano Banana Pro, floating shot: "A worn grey running sneaker floating mid-air against a clear blue sky, captured outdoors in a sunny backyard with a swimming pool and palm trees below. The … background keeps the same poolside backyard vibe with slight natural variation. The shoe is positioned significantly higher in the frame, clearly shifted upward from its…"
- TapNow NB Pro, PRIME: "…background colors. Premium sports-commercial aesthetic with realistic … layered cinematic depth. Sharp detailed film grain. Subtle chromatic aberration. Natural lens breath[ing] … commercial photography. Product dominant. Ultra cinematic depth separa[tion]…"

**Costs on screen (Pollo):** NB Pro image 18 credits; Kling 3.0, 5 s, Standard 75 credits, Professional 150.

---

## 4. Cristian Andrade (crisanvisual) — Spanish-language tech reviewer turned AI-ad demo

**Who:** 217k followers, LatAm, "CEO @CrisanBrands". A mix of real product reviews (Logitech MX line, XPPen, Autodesk) and AI tool demos (Higgsfield Academy, Topview, Filmora).

**Processed:** 7674257708098391297 (Higgsfield image → editable layers, 358k), 7662901127175736593 (Logitech MX Master 4 review, 139k), 7516961855760289080 (Topview AI UGC, 37k), 7654719297729744145 (Filmora "video de marketing", Chocoramo, 11k), 7626530087046892801 (Oreo spot in 2 minutes, Seedance 2.0 × Higgsfield, 8k).

**Signature techniques:**
1. **"Packshot + product + PROMPT" equation card.** On the Oreo post, three white tiles (pack image + cookie image + "PROMPT") sit over the screen recording. The prompt is a **numbered shot list inside one Seedance generation** (15 s, 16:9, 720p). Verbatim fragments: "Create a hyper-realistic commercial for Oreo [using the] uploaded reference [images]: - Image 1: … - Image 2: … Use both uploaded image[s as the] visual source of truth thr[oughout]…" and "7. Show an extreme macro of the cream and cookie texture after the twist. 8. Show a second person reacting naturally with a subtle smile or look of anticipation. 9. Show the Oreo moving toward or dipping into a glass of milk in a realistic, appetizing way, with believable liqu[id]…". The prompt was written in ChatGPT.
2. **Shock-face hook + "WTF ¿Qué acabo de hacer?"** sticker, then "Y me tomó solo 2 minutos". Speed is the claim.
3. **Local hero product** (Chocoramo, a Colombian snack). Filmora mobile flow: photo of the product, then "video de marketing", then upload a scene, write plain words and let the AI "convert that text into a prompt" (verbatim: "Aquí no hay prompts mágicos, solo escribo con palabras simples lo que quiero").
4. **AI UGC as "the end of influencers?"** framing (Topview Product Avatar: pick an avatar, upload a product photo).
5. The real-product review style (macro b-roll with a yellow condensed title "LOGITECH LO VOLVIÓ A HACER", 1 kinetic word per beat) shows the product-film grammar the AI demos imitate.

**Business model:** sponsored reviews and tool affiliates, plus his own brand agency.

---

## 5. Ozan Sihay — Turkish director: real product, AI world, localized proof

**Who:** 190k followers, "Yönetmen/Fotoğrafçı" (director/photographer). He presents to camera in a studio with a mic, Turkish word-pop captions and an "ozansihay" watermark on outputs.

**Processed:** 7542897195188636948 (Nano Banana, 370k), 7455335462039735559 ("professional product video with AI", 163k), 7586336107638328594 (best AIs of 2025, 111k), 7610904962817674514 (Seedance 2.0 launch night, 78k), 7463867819470507272 ("turn your REAL product into video with an AI model", 41k).

**Signature techniques:**
1. **The real product stays real.** Sneaker: a phone photo on the floor, then Canva background removal and "AI backgrounds" matched to the product's perspective (a mountain top). The handbag ad: ChatGPT writes prompts for an AI model in 3 settings, then he **pastes a photo of his actual bag into the AI image in Photoshop with a perspective transform**, then animates. The thumbnail labels it "YAPAY ZEKA MODEL → GERÇEK ÜRÜN" ("AI model → real product").
2. **The product lands as the END frame.** The composited still went into Kling (1.5) **as the end frame** so the shoe falls from the sky onto the summit through rocks and dust. Then MMAudio for SFX (transcript).
3. **ChatGPT as prompt writer, briefed on the motion idea.** Verbatim (Turkish, on screen): "Görseldeki ayakkabıyı Kling AI'de image to video yöntemini kullanarak, profesyonel bir ürün videosu haline getirmek istiyorum. Bana bunun için bu kaya parçaları ve toz duman ile birlikte ayakkabının gökyüzünden dağın tepesine düşerek geldiği bir video için detaylı prompt yazar mısın?" ("I want to turn the shoe in the image into a professional product video with Kling AI image-to-video. Can you write a detailed prompt for a video where the shoe falls from the sky onto the mountain top, with these rock fragments and dust?")
4. **Localized subjects:** an old Murat 131 car in an Istanbul back street, the Istiklal tram, Ottoman soldiers. The "first in Turkey" launch-night hook ("Şu anda saat gece 11 ve ben kamera karşısına acilen geçtim", "It's 11 pm and I rushed to camera").
5. **Seedance 2.0 in CapCut desktop:** 5–15 s, "15 seconds costs 270 credits; CapCut Pro gives 1,200 credits a month"; the free first video should be 15 s; "if you give a realistic human photo it usually errors", so use non-human refs or text-to-video. On-screen fragment: "…sharp textures on the rusted metal parts of @image1. Constraints: Flawless hand and joint anatomy for the robot, maintain character identity from the car."

Visible ChatGPT model prompt (handbag): "A gorgeous woman walking confidently through a luxurious hotel lobby, holding a black leather [handbag] … wearing a body-hugging red satin dress with a high slit and black stilettos. … elegant background includes marble floors, golden chandeliers, and soft ambient lighting…"

---

## 6. Jack Vs. AI — "animators might be cooked" product workflows

**Who:** Small (3.6k) but has 2 breakout posts (1.2M, 348k). Runs his own "VS" apparel brand and uses it as the demo product. Sponsored by Freepik and Artlist.

**Processed:** 7579390625896893698 (miniature workers, 1.2M), 7539458906364366102 (product-into-film-still, 348k), 7600019725472599318 (knitted hand-made style, 5k), 7534845481969536278 (Carhartt lookbook, 1.5k), 7631915393526942998 (Seedance 2 fashion campaign, Artlist, 0.8k), 7584947850786786582 (AI Christmas ad, 0.7k).

**Format:** **Result card on top, webcam below**, kinetic serif/sans words. Opening lines are either fear ("Okay, we might be cooked…", "animators might be cooked") or a status claim ("I made a better AI commercial than Coca-Cola").

**Signature techniques:**
1. **Miniature workers on a giant product** (1.2M). Freepik Image Generator, Nano Banana Pro (250 credits), product as `@img1`, 9:16, 2K. Prompt start, verbatim: "@img1 A whimsical scene of miniature people in colourful hiking gear…". The scene ideas: painters re-painting a Coke can, climbers on an iPhone, a cap, a Stanley cup and a Sony camera. Then Veo 3.1 or WAN 2.5 "so you get audio added". "You can insert literally any product… perfect for advertising."
2. **Product drop-in to a famous film still** (348k): drag a product tile (camera, Darth Vader helmet, Mountain Dew, a perfume) onto a frame, and the characters "realistically interact with your product as if it was always there". The tool is unnamed in the post [inf: an image-plus-product i2v feature].
3. **Craft-material style lock.** Verbatim style prompt card: "handcrafted knitted wool texture, every element appears made of soft yarn with visible knitting stitches and fuzzy fibres, rounded edges, tactile surfaces, no hard lines". NB Pro starting frames, then Veo 3.1 or Kling 2.6. His claim: "the hand puppeted movement and imperfect art style is exactly what brands are after right now."
4. **Brand lookbook recreation:** Grok describes a reference campaign photo, then a Midjourney prompt plus a pre-written self-description and Omni-reference. He switched to a Higgsfield trained character "because none of them look like me", then Veo.
5. **Mock-news emergency-services Christmas spot** (low-poly 3D look, news-ticker inserts, a tagline card).

---

## 7. KC "Create Smarter With AI" — creator-economy AI for small businesses

**Who:** 45k followers, LA, sells via a Stan Store (faceless AI-character YouTube course). The audience is small-business owners and Black women creators. Her biggest 2026 post is a **real** car-seat food review ("Commercial Break: Ralph's fried fish", 75k).

**Processed:** 7527100694722104590 (Higgsfield Soul realism, 114k), 7597310646811675917 (real "Commercial Break" review, 75k), 7524866881807781133 (Veo 3 frames-to-video, 56k), 7489945463408512302 (ChatGPT brand aesthetic board, 17k), 7509600563751947562 (Veo 3 showcase, 13k).

**Techniques:**
- **Named recurring AI characters** ("Bri", "Robin", "Aura Blues" the AI R&B artist). The Veo prompt uses labelled slots, verbatim on screen: "Scene: A content creator walking through a Love Island villa talking directly to the camera Subject: Robin, A 25-year old young, gorgeous black woman wi[th]…" (Google Flow, Frames to Video).
- **Preset-recreate** in Higgsfield Soul: open a style category ("Y2K", "Hair Clips"), press Recreate to load its prompt, change a couple of descriptors and generate 4.
- **Brand Aesthetic Board** from ChatGPT ("The Wellness Baddie": vibe and mood, colour palette, typography, visual content style, brand voice), then rendered as one board image. This is a fast brand-bible artifact for small clients.
- **Format parody prompts:** "Create a video resembling the Hot Ones intro…" in Gemini/Veo; "A realistic camera surveillance video…" (prison visit phone call).
- Comment-reply videos ("Hey what app did you make these on? Midjourney?") as the hook.

---

## 8. AI Video School — consistency engineering for multi-shot ads

**Who:** 11.6k on TikTok, posts long horizontal tutorials (5–10 min) cross-posted from YouTube. Uses a frog-in-a-tank-top character as a mascot.

**Processed:** 7598724739779071287 (NB character sheets, 178k), 7606046936755457293 (consistent voices, 25k), 7644592043385261326 (consistent locations, OpenArt Worlds + Kling 3 Omni + Seedance 2, 21k), 7673389177836227853 (Seedance 2.5 prompt tip, 19k).

**Techniques and verbatim prompts:**
1. **Character turnaround sheet** (full prompt in the caption): "Create a professional character reference sheet based strictly on the uploaded reference image. Use a clean, neutral plain background and present the sheet as a technical model turnaround while matching the exact visual style of the reference… Top row: four full-body standing views… front view, left profile view (facing left), right profile view (facing right), back view. Bottom row: three highly detailed close-up portraits… Maintain perfect identity consistency across every panel. Keep the subject in a relaxed A-pose… Lighting should be consistent across all panels… Output a crisp, print-ready reference sheet look, sharp details." There is also a no-reference variant with `[PUT YOUR CHARACTER DESCRIPTION HERE]`.
2. **Voice-consistency line format** (caption, verbatim): `He/She says in the voice of a [AGE] [GENDER], [TIMBRE], [TONE], [PACING]: "dialogue"`. It was tested across Veo 3.1, WAN 2.6, LTX 2 Pro, Grok and Kling 3. He uses Claude to fill it in ("Using that format, create a voice for a character who sounds like Audrey Hepburn").
3. **Consistent locations:** build a 3D "World" in OpenArt, place characters, grab camera angles as stills, then use those stills as references in Kling 3 Omni and Seedance.
4. **"Don't let ChatGPT or Claude optimize your Seedance prompts"** (66 s tip): LLMs "categorize and summarize in a way that Seedance doesn't demonstrate". The pushback that worked: "are you sure this is optimized according to the official Seedance 2.5 guidelines?" The LLM itself admitted it was "adding too much explanatory prose and repeating constraints… optimize for **clear reference roles + shot timing + visible action + camera behavior + audio**, not turn it into a production bible." His line: "Seedance 2.5 rewards cinematic language… write more like a screenwriter than a prompt engineer." The example T2V prompt he shows (the style of the official examples [inf]), verbatim: "One-take handheld gimbal tracking shot. The camera slowly pushes in through a gap in a heavy red curtain and enters a warm-toned backstage dressing room. A young female singer, with her back to the camera, is adjusting her earpiece as a staff member reminds her it's time to go on. She turns toward the camera and starts singing citypop. The camera pulls back and tracks her as she passes through the curtain into a dim backstage corridor, interacting naturally with her dancers along the way; one staff member hands her a microphone. She and the dancers then step onto the stage, and the camera arcs around to the back, gradually revealing the red-and-black stage design, LED screens, spotlights, haze, and reflective floor. The camera finally pulls out to a wide shot of the arena, showing the packed audience, light boards, glow sticks, and cheering crowd, capturing the youthful, free-spirited climax of the concert."

---

## 9. YouTube-native educators (metadata and prior notes only)

**Dan Kieft** (304k YT). His top ad titles: "How To Use Google VEO 3 JSON Prompting To Create $100k AI Ads" (356k, afzbZYC6fCM), "Create Cinematic AI Ads With Nano Banana Pro + Kling AI – Full Guide" (259k, P7pH_1zFKbE), "Create Cinematic AI Ads with Seedance 2.5 – Full guide" (147k, kGku3TTiYO8), "Create AI UGC Ads With Nano Banana That ACTUALLY Look REAL" (128k, YbztbmMtDZM), and "Exactly How AI Influencers Like Aitana Lopez Make Crazy Money" (273k). His techniques are already in our notes (`research/ai-video-reels/round2/notes/T1.md`, `V2.md`): a label close-up as "authority for the exact wording", a style block from a lookbook via Claude, the Ad Multiplier via the Higgsfield MCP, human-written ideas ("make me 10 different ads… generic"), and his `/SD25` skill.

**Youri van Hofwegen** (330k YT) leans hard on UGC and money: "How to Make AI UGC Ads in 2026 (Full Course)" (82k, K2yPvRsHT3k), "How to Set Up & Use Higgsfield API in 2026 (Save Money)" (82k), "DO THIS to Make AI UGC Ads with AI Influencers to Get RICH in 2026" (49k), "I Built a Claude Agent that Makes 500 AI UGC Ads per Month" (24k, hgtsG5zfLoY), "Create Realistic AI Ads from One Single Image (Consistent Character + Products)" (25k). [inf] His model is affiliate tools plus agent-scale UGC volume.

**Tao Prompts** (196k YT): mostly technique tutorials. The one ad title is "The NEW Way to Create Cinematic AI Ads (Kling 3.0 + Nano Banana Pro)" (18k, GdazHmK1lro). We already have his NB Pro camera-angle method (T3 P20/P23).

## 10. Rory Flynn and Dave Clark (web sources only)

**Rory Flynn** (Systematiq AI; X/IG). His "Mad Libs for AI" prompt formula of non-negotiables: **shot type, subject + action, environment, color scheme, camera + lens, film stock, mood, lighting** ("Start simple. Add complexity later"). Verbatim example: "Motorsport photography, Red Bull F1 car, racetrack, warm tones, 35mm, shallow depth of field, sunset backlighting, center framing, motion blur" ([MATG](https://marketingagainstthegrain.com/articles/ai-tools-to-replace-your-10k-creative-agency)). His "asset hacking" method: take brand images, run Midjourney Describe, then have ChatGPT apply "Describe the image like an award winning professional photographer in extreme technical detail. Use this formula to structure the prompt: [Insert Prompt Formula]" ([Foreplay](https://foreplay.co/post/midjourney-facebook-ads)). Then batches of about 10 prompts with delimiters run in parallel, and a brand "visual profile" built from about 20 images as the system prompt. He claims about 1,000 images in about 20 minutes "after three weeks of building the system". Business model: teaching teams and done-for-you creative; "I don't run ads".

**Dave Clark** (CCO of Promise, backed by a16z and North Road; ex-commercial director for Coca-Cola, HP and Intel). The studio platform MUSE logs every prompt, setting and approved version as **chain-of-title for rights and insurance**. For the Adobe MAX 2025 short he used text prompts, then Firefly Boards for shot planning, then Firefly partner models, Substance, Photoshop and Premiere ([nofilmschool](https://nofilmschool.com/dave-clark-interview-adobe-max), [Adobe blog](https://blog.adobe.com/en/publish/2025/10/29/how-shorts-for-generative-ai-film-festival-max-2025-were-made), [etcentric](https://www.etcentric.org/?p=189118)).

---

## 11. Cross-creator synthesis

### What all the best ones do

1. **Start from a real artifact, not a prompt.** Ozan photographs the real shoe and pastes the real bag in, BYRVM screenshots his own clip, Karen photographs herself and prints the output, Crisan uses the real packshot, Jack uses his own merch. The real input guarantees product fidelity and reads as human. This agrees with Rourke's 2026 v2v shift (study 14 A3).
2. **The LLM writes the shot prompts; the human writes the idea.** PJ (Gemini, "5 prompts at a time"), Ozan and Crisan (ChatGPT), Jack (Grok describes the reference), Rory (Describe, then the formula), AIVS (Claude for voice lines). But AIVS warns that LLMs over-structure Seedance prompts, so ask for "screenwriter" prose with reference roles, timing, action, camera and audio.
3. **One prompt = one mini-commercial.** A numbered shot list inside a single Seedance generation (Crisan's Oreo, 15 s), a one-take path (AIVS concert), or start/end frames per beat (BYRVM, Ozan).
4. **The result plays in the first 0.5 s.** Every hook strip shows the finished output by 0.5–1.0 s: a full-frame cold open (PJ, Karen), or an inset result card with the creator reacting (BYRVM, Jack, Crisan). Nobody opens on UI.
5. **A big brand as the demo product** (Coke ×3 creators, Oreo, PRIME, Sony, Carhartt, Logitech). Recognizable packaging gets the scroll-stop. Spec work on famous brands is the portfolio [inf].
6. **Low per-video cost, high attempt count.** Kalshi: 300–400 generations for 15 clips (about 4–5% yield) for about $2k. Pollo Kling 3.0 Pro 5 s = 150 credits, CapCut Seedance 15 s = 270 credits, Higgsfield Kling 2.6 5 s = 10 credits.
7. **Money comes from tools, not views.** 5 of the 8 TikTok creators are paid per tool tutorial (Firefly, Chrome, Higgsfield, Pollo, Lovart, TapNow, Creatify, Artlist, Freepik, Filmora, Topview), with a "Comment X" ManyChat CTA. Only PJ and Promise sell **ads to brands** as the main business. Paid posts dominate the top-plays lists (Karen 147.7M; BYRVM 890k).

### Techniques we don't have yet (checked against `creative_matrix.json` and marketing 00–26)

| # | Technique | Source | Gap in our pipeline |
|---|---|---|---|
| T1 | **Fake-BTS mockumentary** as ad #2 from the same assets | PJ Kalshi BTS | no `mock_bts` format in the dice |
| T2 | **Vox-pop "crazy people" montage** with brand-supplied one-liners | PJ Kalshi | `interview_doc` exists; rapid-vignette vox pop does not |
| T3 | **Anachronism selfie-vlog** (historical or fictional figures vlogging) | PJ Bible | no mechanism for anachronism |
| T4 | **Print-and-animate hybrid** (AI frames printed, cut out, stop-motion) | Karen | `stop_motion` exists only as an AI look, not a physical pass |
| T5 | **Pendulum** (AI aerial pull-back + reversed copy) | Karen / Higgsfield preset | not in 16-seamless-flow |
| T6 | **Real → AI → real sandwich** (screenshot the product-in-frame moment, NB next shot, start/end back to the real frame) | BYRVM | we do start/end frames, but not anchored to a real clip |
| T7 | **Flavor/variant match-cut** with the same camera motion re-applied to N variants | BYRVM Lovart/CapCut | no "variant matrix" one-pass |
| T8 | **Product fly-through** ("into the product through openings → interior macro") | BYRVM sneaker | not in the shot list |
| T9 | **Real-product composite** (paste the real product into the AI still with a perspective transform before i2v) | Ozan | we generate the product; no composite-first rule |
| T10 | **Product as END frame** (it lands or arrives into its hero position) | Ozan | we default the hero to the start frame |
| T11 | **Miniature-workers scale shift** prompt template | Jack (1.2M) | `fooh`/`dimension_scale` exist; no ready template |
| T12 | **Craft-material style lock** (knitted, paper, clay, with "no hard lines") | Jack | not in the look bank |
| T13 | **Product drop-in to an existing scene** (characters interact with it) | Jack | partial (Rourke annotated keyframes) |
| T14 | **Labelled-tail Veo prompt** (prose + `Time of Day / Lens / POV / Audio / Background`) | PJ | our templates are block- or JSON-style |
| T15 | **Voice line format** `[AGE] [GENDER], [TIMBRE], [TONE], [PACING]` for in-model dialogue | AIVS | 13-elevenlabs covers EL only |
| T16 | **Anti-over-optimization check** for Seedance prompts (reference roles, timing, action, camera, audio; screenwriter prose) | AIVS | our LLM prompt compiler may over-structure [inf] |
| T17 | **Brand aesthetic board** as a one-image brand bible for small clients | KC | we have art direction (26) but not as a client deliverable |
| T18 | **Chain-of-title log** (every prompt, setting and approved version) | Dave Clark / Promise | partial (hfgen logs?) [inf] |
| T19 | **Batch-of-5 prompt rule** for LLM shot expansion | PJ | none |
| T20 | **Localized-world proof** (local cars, streets, snacks) | Ozan, Crisan | 02-niches has no localization rule |

### Things to copy now, mapped to our pipeline

1. **Add 4 formats to `references/creative_matrix.json`:** `mock_bts` (T1), `vox_pop_montage` (T2), `anachronism_vlog` (T3, under mechanism or format), `print_animate_hybrid` (T4). Add an incompatibility rule: `mock_bts` needs an existing hero ad. Run `director.py dice --lock format=mock_bts` after each delivered spot to plan the free second asset.
2. **Hero-frame rule in the image-direction step (`image-direction.md` / 17-hero-stills):** if the client gives a real product photo, **composite it into the AI plate first** (T9) and decide start vs end placement explicitly. Default to "product arrives as END frame" for reveal spots (T10).
3. **New shot recipes in `16-seamless-flow.md`:** pendulum (T5); real-AI-real sandwich (T6); variant match-cut with "recreate the exact same motion for every scene" (T7); product fly-through (T8).
4. **Prompt-compiler guardrails (`04-ai-craft.md` + the Seedance template in `12-higgsfield-mastery.md`):** (a) expand shots in batches of ≤5 (T19); (b) Seedance: screenwriter prose, then one line each for reference roles, timing, camera and audio; reject "production bible" output (T16); (c) Veo: PJ's labelled tails (T14); (d) keep the numbered in-prompt shot list for 15 s single-gen spots (Crisan).
5. **Template bank (`17-hero-stills-mastery.md`):** miniature-workers (T11), craft-material style lock (T12), AIVS turnaround sheet (cross-check against our current sheet prompt).
6. **Voice lines in in-model dialogue (`13-elevenlabs-mastery.md`, new section):** the AIVS format (T15) for Veo/Kling/Seedance native audio. ElevenLabs stays for VO.
7. **QC gate addition (`qc-rubric.md`):** "Does the result read in frame 0–15 (0.5 s)?" Every top creator's hook shows the finished output by 0.5–1 s.
8. **Client deliverables:** a brand aesthetic board (T17) in the brief stage for SMB clients, and a per-job prompt/setting/approval log (T18) as chain-of-title in the job folder.
9. **Portfolio content (no talking head, to keep the 00-playbook ban):** PJ's letterboxed 16:9 film with a static 1-line top title, and a mock-BTS cut-down. Both are faceless and both are proven formats.
10. **Budget assumption in hfgen cost plans:** plan for about 5% usable takes on comedic multi-character spots (PJ's 300–400 → 15) versus higher yield on single-product shots [inf].

### Caveats

- TikTok under-represents PJ Ace, Rory Flynn, Dave Clark and the YouTube educators, whose main channels (X, IG, YouTube) were blocked. Their sections rely on captions, titles and press.
- Plays on sponsored posts are probably paid-boosted [inf], so they are a weak signal of organic appeal.
- On-screen prompt fragments are partial where the UI was scrolled. Brackets mark my completions.
