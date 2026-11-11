# 25 — Tool Comparison

## Evidence warning

**Every figure below is grade B or C** ([02](02-evidence-ledger.md)) — drawn from secondary
sources and pricing aggregators, not from vendor pricing pages read directly. AI video pricing
and terms change faster than any document can track.

**Before the first paid delivery, the selected vendor's actual Terms of Service and pricing page
must be read and recorded** (verification queue, [42](42-validation-plan.md) V-0). A vendor whose
terms prohibit our use case would invalidate every deliverable made with it.

**Selection principle: we do not choose a tool because it is new, popular, or produces the most
impressive demo.** We choose on commercial terms, failure modes, and switching cost — in that
order.

---

## 1. Generation tools

| Tool | Cost | Commercial rights | Consistency on interiors | Failure modes | Switching cost |
|---|---|---|---|---|---|
| **Kling** | ~$0.09–0.14/s API; ~$6.99/mo consumer plan (E-22, E-23) | Paid plans permit commercial use (E-23, **unverified**) | Reported strong image-to-video | Unknown to us | Low — prompts are portable |
| **Runway Gen-4** | $15 / $35 / $95 per month; ~10–15 credits/s standard, 25–40 credits/s Turbo/4K (E-21) | **Paid plans only. Free tier is personal use, explicitly not for client work (E-21)** | Described as the professional standard for image-to-video (E-22) | Credit burn on retries is the cost risk | Low–medium |
| **Google Veo 3.1** | ~$0.15/s fast; 5s fast clip with audio ≈ $0.75; 5s standard ≈ $2.00. Consumer access via Google One AI Premium from $19.99/mo (E-22, E-23) | Paid plans permit commercial use (E-23, **unverified**) | Native audio generation — **a liability for us, not a feature** (see below) | Higher per-second cost | Low |
| **Sora 2** | ~$0.10/s at 720p standard; Pro $0.30–0.70/s (E-22) | Paid plans (E-23, **unverified**) | Unknown to us | Unknown | Low |

### Recommendation

**Primary: Kling. Secondary: Runway.**

**Why Kling first:** lowest per-second cost (E-22) at a stage where the attempt ratio is unknown
and could be 5:1. When failure rate is the unknown, the cheapest per-attempt option minimises the
cost of discovering it.

**Why Runway second, not first:** it is described as the image-to-video standard (E-22), which
matters for our use case, but at 10–40 credits per second on a 625-credit Standard plan, a single
order consuming ~125 seconds of generation across retries could exhaust a month's allowance. It
is the quality fallback, used when Kling cannot produce an acceptable clip.

**Why not Veo despite quality:** native audio generation is an *accuracy hazard* for us. A model
that invents ambient sound over a property video is generating a sensory claim about the
property. We would be spending more per second for a feature we must then disable.

**Cost of this choice:** two subscriptions instead of one (~$42/mo combined, still inside the
[15](15-financial-model.md) fixed base). Two toolchains to learn.

**Reversal condition:** if measured accepted-clip yield on Kling is worse than 1 in 4 for
interiors (A-03 kill condition), switch primary to Runway and re-run the financial model. If both
fail, the product becomes template-based motion ([24](24-production-workflow.md) §Fallback).

**Privacy note:** customer property photographs are uploaded to a third-party model vendor. This
must be disclosed to customers and covered in the rights agreement
([38](38-rights-and-security.md)). Vendor data-retention and training-use terms must be read —
**this is a customer-confidentiality question, not just a licensing one.**

---

## 2. Editing

| Tool | Cost | Commercial terms | Verdict |
|---|---|---|---|
| **DaVinci Resolve (free)** | $0 | No restriction on commercial use of the free tier; assets you import remain yours | ✅ **Chosen (D-08)** |
| CapCut | Free / ~$10 / ~$20 per month | Paid tiers include a commercial licence for editor-created content. **No rights granted to built-in music at any tier.** ToS grants CapCut a broad licence over uploaded and created content (E-24) | ❌ **Rejected for client work.** Permitted for our own marketing content only |
| Adobe Premiere | ~$23/mo | Standard | ⏸️ Viable, unnecessary spend |

**Why CapCut is rejected (D-08):** it is the fastest editor in this category and it would save
real time. The disqualifier is that its terms take a broad licence over uploaded content — and
what we upload is a *client's* property photography, which we have promised them we hold under
defined terms ([38](38-rights-and-security.md)). We cannot grant a third party rights over assets
that are not ours to grant. The music trap (E-24) is the better-known problem; the content
licence is the more serious one.

**Cost of this choice:** a steeper learning curve and slower simple edits. Accepted.

---

## 3. Music

| Option | Cost | Terms | Verdict |
|---|---|---|---|
| **Epidemic Sound Pro** | ~$16.99/mo annual ($203.88/yr) or $39.99 monthly (E-18) | Freelancer client work, digital ads, commercial online use. **Perpetual right to keep productions made during the subscription available**, and to sublicense to clients under $50M revenue (E-18) | ✅ **Chosen (D-07)** |
| Artlist | ~$299/yr (E-19) | Broad commercial | ⏸️ Alternative |
| Editor-bundled music (CapCut etc.) | $0 | **No commercial rights granted (E-24)** | ❌ **Never** |
| YouTube Audio Library | $0 | Varies by track; attribution requirements | ❌ Too much per-track diligence at volume |

**The decisive term is the perpetual right for work completed during the subscription period**
(E-18). Without it, every video we have ever delivered would become a liability the day we
stopped paying — an unacceptable structure for a client-deliverable business.

**Required before first paid delivery:** read the full licence text. The summary is grade B.

---

## 4. The rest of the stack

| Function | Tool | Cost | Why |
|---|---|---|---|
| Payments | Stripe | 2.9% + $0.30; $15 disputes (E-25) | Standard; hosted checkout avoids handling card data |
| Site | Static site + form | ~$15/mo | Speed and control ([34](34-website-specification.md)) |
| Forms | Any with webhook + file upload | free tier | Feeds the order record |
| Storage | Cloud object storage | ~$10/mo | Delivery + archive ([38](38-rights-and-security.md)) |
| Email | Business email + a lifecycle tool | ~$20/mo | [32](32-search-email-remarketing.md) |
| Time tracking | **Anything, but it must be used on every order** | $0 | **The single most important tool in this list** — it is how A-10 becomes a measurement ([15](15-financial-model.md)) |
| Scheduling | Free tier | $0 | Calls only |
| Accounting | Basic bookkeeping | ~$20/mo | |

---

## 5. Selection principles

1. **Commercial terms before capability.** A tool whose free tier prohibits client work (E-21) is
   not cheaper — it is unusable.
2. **Read what the vendor takes, not just what it gives.** CapCut's content licence (E-24) is the
   clearest example of a term that only matters once you are handling someone else's assets.
3. **Prefer low switching costs** while everything is unvalidated. Prompts are portable; a
   proprietary project format is not.
4. **Free tools where suitable**, per the operating constraints — but never where the licence is
   the reason it is free.
5. **Never select on demo quality.** Demo reels are cherry-picked best-case outputs
   ([11](11-competitor-analysis.md) §F). Our decision variable is *median* output on *interior
   photographs*, which no demo shows.

## 6. What would change these choices

| Trigger | Response |
|---|---|
| Kling yield <1-in-4 on interiors | Promote Runway to primary; re-run the financial model |
| Both generators fail on interiors | Product becomes template-based motion; re-price |
| A vendor's ToS is found to prohibit our use, or claims rights in outputs | **Stop using it immediately**; re-verify every delivered asset made with it |
| A vendor is found to train on uploaded customer content without an opt-out | Stop; this is a customer-confidentiality breach, not a preference |
| Epidemic Sound removes the perpetual term | Switch to Artlist; re-read terms first |
| Measured generation cost exceeds $40/order | Revisit the price floor ([15](15-financial-model.md)) |
