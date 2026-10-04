# PumpWatch: Regulation & Legal Research

Prepared by the Regulation Team (Market & Regulation dept.), 2026-10-04.

> **DISCLAIMER: This is desk research, not legal advice.** It was written by a non-lawyer research team from
> public sources. Terms of service change often (several cited below changed in 2026). Every conclusion here
> must be checked by a qualified lawyer (US securities/privacy + Israeli privacy) before PumpWatch collects
> data commercially or signs a customer. Items not confirmed from an opened/searched source are marked **UNVERIFIED**.

---

## 0. Bottom line (read this first)

1. **X (Twitter) API: the surveillance clause is a real blocker unless X approves in writing.** The Developer
   Agreement (last updated 2026-04-27) bars using X Content "for purpose of conducting or providing surveillance or
   gathering intelligence, including but not limited to investigating or tracking X users or X Content", and bars
   profiling individuals based on "X Content relating to any alleged or actual commission of a crime"
   ([Developer Agreement §User Protection](https://docs.x.com/developer-terms/agreement)). Flagging accounts as pump
   promoters for brokers is very close to that wording. Scraping X instead is also barred, with liquidated damages of
   $15,000 per 1M posts over 1M/day ([X ToS, effective 2026-10-09](https://x.com/en/tos)).
2. **Telegram: the terms now prohibit the core use case.** "Access to user-generated content for any purpose other
   than ordinary, legitimate, and intended use of the Telegram platform as its user is prohibited", and ML
   use of Telegram data is "firmly prohibited" ([Content Licensing ToS](https://telegram.org/tos/content-licensing));
   bot developers may not scrape "public group or channel contents" ([Bot Developer ToS §4.3](https://telegram.org/tos/bot-developers)).
3. **Reddit, StockTwits, Meta, Discord: commercial use needs a separate written deal** (sources in §2). Reddit
   explicitly bans "law enforcement or surveillance purposes" ([Developer Terms](https://redditinc.com/policies/developer-terms)).
   **StockTwits is the bright spot:** its terms say it licenses derived data "to financial institutions and investment
   firms" ([StockTwits Terms, rev. 2026-07-10](https://stocktwits.com/about/legal/terms)).
4. **Case law helps scrapers of logged-off public pages less than it seems.** It limits CFAA and some contract claims, but
   platforms keep winning on breach of contract where the scraper has an account (hiQ paid $500k and was enjoined).
5. **Privacy:** Labelling a named person as a likely manipulator is, in EU terms, "criminal offence" data (GDPR Art. 10),
   which a private company may process only where EU/member-state law authorises it. **Design default: score tickers and
   anonymised clusters, not named people.**
6. **Selling to US brokers is feasible but slow:** expect vendor due diligence (FINRA RN 21-29), a SIG questionnaire,
   and a SOC 2 request. A first SOC 2 typically costs ~$25k-$80k and takes ~4-11 months (vendor-sourced estimates).

**Recommended data strategy (for the lawyer to validate):** start with licensed or clearly allowed sources: EDGAR,
market data, StockTwits (licensed), and X/Reddit **only after written approval of the use case**. Treat Telegram as
out of scope until a lawyer says otherwise.

---

## 1. What a US broker will demand from a vendor

### 1.1 Why they ask
- FINRA RN 21-29: firms "can outsource tasks but cannot outsource responsibility". They must supervise vendors under
  Rule 3110 (supervision) and cover cybersecurity, BCP and records ([FINRA RN 21-29, Aug 2021](https://www.finra.org/rules-guidance/notices/21-29)).
  Stale (>2 yrs) but still the reference notice and cited again in the 2026 report.
- The FINRA 2026 Oversight Report has a "Third-Party Risk Landscape" section. It lists these practices: initial and
  ongoing due diligence on vendors supporting mission-critical systems (explicitly incl. **AML monitoring**); checking
  vendor **GenAI** use; contract language barring firm or customer data from going into open GenAI tools; an inventory of the
  data types vendors hold; involving vendors in incident-response testing; return or destroy data at exit; checking
  **fourth parties** ([FINRA 2026 Report PDF, p.29](https://www.finra.org/sites/default/files/2025-12/2026-annual-regulatory-oversight-report.pdf)).
- The same report has a topic on the **"Increase in Small-Cap Fraud Involving Exchange-Listed Equities"**, which
  describes social-media "investment clubs" that direct victims into small-caps (same PDF). This is a regulatory tailwind for PumpWatch.
- **SEC Reg S-P amendments (adopted 2024-05-16):** covered institutions must oversee service providers. Each provider
  must notify the firm **within 72 hours** of a breach of a customer information system it maintains. Compliance:
  larger entities 2025-12-03, smaller entities 2026-06-03 ([SEC press release 2024-58](https://www.sec.gov/newsroom/press-releases/2024-58);
  [Simpson Thacher summary](https://www.stblaw.com/about-us/publications/view/2024/05/22/sec-adopts-significant-amendments-to-regulation-s-p-requiring-notification-of-sensitive-customer-information-breaches-service-provider-oversight)).
  **Relevance:** applies in full if PumpWatch ever receives broker customer data (signal S6 "new small buyers").
  If PumpWatch only *sends* alerts built from public data, the burden is much lighter. This is a strong reason to keep S6 optional or on-premise.
- **Reg S-ID (identity-theft red flags)** applies to firms with "covered accounts"
  ([Deloitte DART summary](https://dart.deloitte.com/USDART/home/accounting/sec/rules-regulations/248-regulations-s-p-s-am/c-regulation-s-id-identity-theft/c-regulation-s-id-identity-theft)).
  Probably not triggered for PumpWatch unless it touches account data (**UNVERIFIED, lawyer question**).

### 1.2 Vendor checklist (what to have ready)
| # | Item | When needed | Note |
|---|------|-------------|------|
| 1 | Security questionnaire answers: **SIG Lite** (~128 q) or **SIG Core** (~627 q, for vendors holding sensitive data). 2025 edition added an AI domain | First pilot | [Mitratech on SIG 2025](https://mitratech.com/resource-hub/blog/sig-2025-key-updates-and-considerations/); [question counts: Spendflo](https://www.spendflo.com/blog/sig-questionnaire) |
| 2 | Written info-security policy set (access control, encryption, logging, change mgmt, vendor mgmt, incident response, BCP) | First pilot | Basis for SOC 2 later |
| 3 | Incident-response plan with **72h** client notification clause | First contract | Reg S-P (above) |
| 4 | Data inventory + "Data Collection Policy" (what sources, what PII, retention) | First pilot | PLAN §5; FINRA 2026 data-type inventory |
| 5 | Sub-processor / fourth-party list (cloud, LLM API, data vendors) | First pilot | FINRA 2026 |
| 6 | AI/GenAI use statement (models used, no client data in training) | First pilot | FINRA 2026 |
| 7 | BCP / uptime and exit plan (data return/destruction) | Contract | FINRA 2026, Rule 4370 |
| 8 | Data-source licence evidence (proof that X/Reddit/etc. use is permitted) | Contract | Brokers will ask; see §2 |
| 9 | Insurance: Tech E&O + cyber, typically $1M limits | Contract | §1.4 |
| 10 | Pen-test report (annual) | Larger customers | **UNVERIFIED** as a hard requirement; common practice |
| 11 | SOC 2 Type I, then Type II | Enterprise / large broker | §1.3 |

### 1.3 SOC 2: realistic cost and time (vendor-sourced estimates, treat as ranges)
| Item | Estimate | Source |
|------|----------|--------|
| Compliance platform (Vanta/Drata) | ~$7.5k-$15k/yr at start-up size; medians ~$20k-$25k | [costbench Drata vs Vanta](https://www.costbench.com/compare/drata-vs-vanta/); [knowlee Drata 2026](https://www.knowlee.ai/blog/tools/drata-pricing-2026) (third-party estimates, not list prices) |
| Type I audit fee | ~$12k-$25k boutique firm; $50k+ Big 4 | [getagency comparison](https://blog.getagency.com/articles/soc-2-type-i-vs-type-ii-cost-timeline-comparison) |
| Type II audit fee | ~$18k-$40k boutique firm | same |
| First-year total | ~$25k-$50k lean start-up; $45k-$80k Type I then Type II | same; [Drata on audit cost](https://drata.com/blog/soc-2-audit-cost) |
| Time | Type I ~3-4 months from kickoff; Type II needs a 3-12 month observation window, typically report at month ~10-11 | getagency (above) |
| Year 2+ upkeep | ~$15k-$40k/yr | getagency (above) |

**Implication:** a first SOC 2 is close to the founder's whole ~$30k budget. PLAN §8 is right to defer it until 2-3
customers or one large customer demands it. Before that, use SIG Lite answers, policies and a pen test.

### 1.4 Insurance
Tech E&O averages ~$1,094/yr and cyber ~$1,837/yr for SaaS at $1M limits
([Insureon SaaS cost](https://insureon.com/technology-business-insurance/saas-companies/cost)). This is US small-business data;
an Israel-based vendor selling surveillance data to brokers may price higher (**UNVERIFIED**). Media liability /
defamation cover should be asked for explicitly (see §4.1).

---

## 2. Data-source terms

| Source | Commercial use allowed? | Surveillance / tracking restriction? | Cost | Key clause (with URL) |
|--------|------------------------|-------------------------------------|------|-----------------------|
| **X API** | Yes, paid, but **no redistribution** of content: only Post/User IDs, max 1.5M Post IDs per entity per 30 days ([Developer Policy](https://docs.x.com/developer-terms/policy)) | **YES, BLOCKER.** "Unless explicitly approved by X in writing" no use "for purpose of (a) conducting or providing surveillance or gathering intelligence, including but not limited to investigating or tracking X users or X Content … (d) … profiling individuals based on … X Content relating to any alleged or actual commission of a crime". Government end-users need an Enterprise plan; none whose mission is surveillance ([Developer Agreement, updated 2026-04-27](https://docs.x.com/developer-terms/agreement)). The restricted-use page adds "Background checks" ([Restricted uses](https://docs.x.com/developer-terms/more-on-restricted-use-cases)) | Pay-per-use: $0.005 per post read, $0.010 per user read; **capped at 3M post reads/month**, above that Enterprise ([X pricing](https://docs.x.com/x-api/getting-started/pricing)) | ToS: "crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited" + **$15,000 per 1M posts** liquidated damages above 1M posts/24h ([X ToS](https://x.com/en/tos)) |
| **Reddit Data API** | **No** without a separate agreement: may not "access or use … by or on behalf of a business or as part of a service or product that is monetized" ([Developer Terms, rev. 2026-03-24](https://redditinc.com/policies/developer-terms)); "commercial purposes … you will need to enter into a separate agreement" ([Data API Terms, rev. 2026-07-20](https://redditinc.com/policies/data-api-terms)) | **YES.** Prohibits use "for law enforcement or surveillance purposes" (Developer Terms). The Public Content Policy (May 2024) bars partners from background checks, government surveillance or helping law enforcement ([TechCrunch](https://techcrunch.com/2024/05/09/reddit-locks-down-its-public-data-in-new-content-policy-says-use-now-requires-a-contract)) | Free tier 100 QPM non-commercial; $0.24/1k calls (2023, **stale**) ([TechTarget](https://www.techtarget.com/whatis/feature/Reddit-pricing-API-charge-explained)); commercial = negotiated, **UNVERIFIED** price | Data API Terms 3.2: may not "derive revenues from the use or provision of the Data APIs … unless there is express written approval from Reddit" |
| **Telegram (MTProto API / Bot API)** | **Effectively no.** Access to user content "for any purpose other than ordinary, legitimate, and intended use … as its user is prohibited" ([Content Licensing ToS](https://telegram.org/tos/content-licensing)) | **YES, BLOCKER.** Bots may not collect beyond what is needed; "Always prohibited … scraping public group or channel contents" ([Bot Developer ToS §4.3](https://telegram.org/tos/bot-developers)); API apps bound by AI/ML ban ([API ToS §1.5](https://core.telegram.org/api/terms)) | Free | ML ban: "scraping, indexing, harvesting, aggregation or use of data … to … deployment of artificial intelligence, machine learning models" (Content Licensing). PumpWatch's hype-language classifier would fall inside this |
| **StockTwits** | **Yes via licence.** Terms say StockTwits licenses derived data "to third parties, including financial institutions and investment firms" | No surveillance clause found; scraping banned "except as expressly authorized by us in writing or through an approved API" | Negotiated, **UNVERIFIED** | [StockTwits Terms, rev. 2026-07-10](https://stocktwits.com/about/legal/terms). **Best licensed social source to approach first** |
| **Meta (Facebook/Instagram)** | No, except via APIs with permission. The Content Library is for academic/non-profit researchers only ([Meta FAQ](https://developers.facebook.com/docs/content-library-and-api/support/faqs)) | Uses limited to purposes Meta "expressly granted" | n/a | "You may not access or collect data from our Products using automated means (without our prior permission)" ([Automated Data Collection](https://developers.facebook.com/docs/development/terms-and-policies/automated-data-collection/)). Search summaries say the ToS now covers this "regardless of whether … logged-in", i.e. a post-Bright-Data fix (**UNVERIFIED verbatim**; facebook.com/terms is JS-rendered) |
| **Discord** | No scraping; bots only with server-admin consent; self-bots banned | Discord shut down the "Spy.pet" tracking service and threatened legal action ([TechRadar](https://www.techradar.com/pro/security/spypet-data-harvester-taken-down-by-discord)) | Free API | Developer Policy reportedly bans mining/scraping and ML training without permission: **UNVERIFIED** (page returned 403; [policy URL](https://support-dev.discord.com/hc/en-us/articles/8563934450327-Discord-Developer-Policy)) |
| **SEC EDGAR** | Yes (public domain US gov data); fair-access limit and declared User-Agent | None | Free | Rate limit and UA rules: see [SEC webmaster FAQ](https://www.sec.gov/os/webmaster-faq#code-support) (**UNVERIFIED** current 10 req/s figure) |
| **WhatsApp** | Out of scope by red line (PLAN §5) | n/a | n/a | n/a |

### 2.1 Scraping case law (US): what it does and does not protect
| Case | Holding | Lesson for PumpWatch |
|------|---------|----------------------|
| **hiQ v. LinkedIn** (9th Cir. 2022; final 2022-12) | CFAA likely does not cover public pages, **but** hiQ lost on **breach of contract** (scraping + fake accounts), paid **$500k**, and was permanently enjoined and ordered to delete data and code ([Proskauer](https://newmedialaw.proskauer.com/2022/12/08/hiq-and-linkedin-reach-proposed-settlement-in-landmark-scraping-case/)) | Logging in or holding an account = agreeing to ToS. Fake accounts are fatal. The PLAN red line on fake identities is legally sound |
| **Meta v. Bright Data** (N.D. Cal., 2024-01-23) | Summary judgment for Bright Data: Meta's terms did not bar **logged-off** scraping of public data. Meta dropped the case in Feb 2024 ([FBM](https://www.fbm.com/business-litigation/publications/major-decision-affects-law-of-scraping-and-online-data-collection-meta-platforms-v-bright-data/); [TechCrunch](https://techcrunch.com/2024/02/26/meta-drops-lawsuit-against-web-scraping-firm-bright-data-that-sold-millions-of-instagram-records)) | Narrow: depends on contract wording, which Meta and X have since tightened |
| **X Corp v. Bright Data** (N.D. Cal., 2024-05) | Dismissed: X's contract claims pre-empted by copyright law; warning against "information monopolies" ([CNBC](https://www.cnbc.com/2024/05/10/elon-musks-x-loses-lawsuit-against-bright-data-over-data-scraping.html); [Pearl Cohen](https://www.pearlcohen.com/federal-court-dismisses-xs-data-scraping-claims/)) | Helpful, but a district-court ruling. Appeal status and later X ToS changes are **UNVERIFIED** |

**Our reading (for the lawyer):** case law lowers *criminal/CFAA* risk for logged-off public data in the 9th Circuit. It does
**not** make a business built on scraping X/Telegram safe. It also does not fix the **customer problem**: brokers'
vendor due diligence will ask "do you have the right to this data?" (§1.2 item 8), and "we scrape against ToS" fails that test.

---

## 3. Privacy law basics

### 3.1 United States
- **CCPA/CPRA (California):** "publicly available" information is excluded from "personal information". This includes info
  a business reasonably believes the consumer lawfully made available to the general public. Posts restricted to
  friends/specific audiences are **not** covered ([TrueVault explainer](https://safe.truevault.com/learn/ccpa/what-is-publicly-available-information-under-the-ccpa); Cal. Civ. Code §1798.140(v)(2)).
  CCPA business thresholds (e.g., revenue >~$25M adjusted) likely not met early on: **UNVERIFIED current figure**.
- **California Delete Act (data brokers): watch closely.** A "data broker" knowingly collects and **sells** to third parties
  personal information of consumers it has no direct relationship with. It must register, and from **2026-08-01** must
  process DROP deletion requests every 45 days. Penalty **$200/day per request** ([CalPrivacy DROP](https://privacy.ca.gov/drop-for-data-brokers/);
  [Perkins Coie](https://legacy.perkinscoie.com/insights/blog/california-drop-mechanism-15-billion-exposure-and-clock-ticking-key-takeaways-2026)).
  If PumpWatch sells profiles of California-resident promoters, it may be a data broker, even if the data is
  "publicly available" (**lawyer question**; the interaction between the exemption and the Delete Act is UNVERIFIED).
  Vermont, Texas and Oregon also have data-broker registries (**UNVERIFIED** applicability).
- **Other state privacy laws** (≈20 states) mostly exempt publicly available data and have revenue/volume thresholds
  (**UNVERIFIED**, not checked state-by-state).

### 3.2 European Union (GDPR)
- **Reach:** GDPR applies to a non-EU company that **monitors the behaviour** of people in the EU (Art. 3(2)(b)). It would then
  need an EU representative (Art. 27) ([GDPR Art. 3](https://gdpr-info.eu/art-3-gdpr/)). Public Telegram/X promoters can be EU residents.
- **Legal basis Art. 6(1)(f) legitimate interest:** the CJEU (C-621/22 *KNLTB*, 2024-10-04) held commercial interests
  *can* be legitimate interests, overruling the Dutch DPA's "never" stance ([A&O Shearman](https://www.aoshearman.com/en/insights/ao-shearman-on-data/cjeu-commercial-interests-of-controller-can-serve-as-a-legitimate-interest)).
  But the Dutch DPA's 2024 guidance says private scraping is "almost always" unlawful ([Hogan Lovells](https://www.hlc.com/en/publications/dutch-dpa-issues-guidelines-on-data-scraping_1)).
  Fraud prevention is a strong interest, but a balancing test plus a documented LIA is required.
- **Art. 10 (criminal-offence data): biggest EU issue.** Covers suspicion of offences even without proceedings
  ([Bird & Bird on GC v CNIL](https://www.twobirds.com/en/hr-data-essentials/shared/articles/2019/global/are-you-inadvertently-processing-european-criminal-conviction-data);
  [GDPR Art. 10](https://gdpr-info.eu/art-10-gdpr/)). Processing is only allowed under official authority or when Union/member-state
  law authorises it. Tagging an identifiable person as a likely pump promoter is plausibly Art. 10 data.
- **Art. 14 notice:** when data is not collected from the person, they must be informed, unless "disproportionate effort"
  (Art. 14(5)(b)) applies with safeguards such as a public notice ([GDPR Art. 14](https://gdpr-info.eu/art-14-gdpr/)).
- **Art. 22 (automated decisions):** relevant only if a customer makes decisions with legal or similarly significant effect
  (e.g., account closure) solely from PumpWatch scores. Contracts should require human review ([GDPR Art. 22](https://gdpr-info.eu/art-22-gdpr/)).
- **Mitigation by design:** score **tickers** and **message clusters**; pseudonymise handles (hash) by default; reveal an
  identity only on customer request with logged justification; short retention.

### 3.3 Israel (founder's home jurisdiction)
- **Amendment 13** to the Privacy Protection Law in force **2025-08-14** ([Pearl Cohen](https://www.pearlcohen.com/major-amendment-to-israeli-privacy-law-set-to-take-effect/)).
  - **Registration:** mostly abolished, but databases whose **main purpose is collecting personal data to transfer to others
    as a business** (data brokers) must register if >10,000 data subjects. Controllers of "especially sensitive" data on
    ≥100,000 people must notify the PPA ([Pearl Cohen, enacted-law summary](https://www.pearlcohen.com/the-knesset-enacts-a-comprehensive-amendment-to-the-privacy-protection-law/)).
  - **"Especially sensitive data" includes criminal records** and personality assessments (same source).
  - **DPO** required for "extended and systematic monitoring" and data brokering (Pearl Cohen above; the PPA draft guidelines govern).
    PumpWatch's core activity may meet this.
  - **Fines** up to NIS 320k per violation (640k aggravated); statutory damages up to NIS 65k ([Vixio](https://www.vixio.com/insights/pc-regulatory-influencer-israel-modernises-privacy-law-comprehensive)).
- Israel has EU adequacy status, which eases EU→Israel transfers (**UNVERIFIED** current status after the 2024 EC review).

---

## 4. Other legal risks

### 4.1 Defamation / trade libel
- Calling a named person or company a "pump" can be defamatory if false. Example: *Nazerali v. Mitchell* (BC Supreme Court 2016),
  where web posts accused a promoter of pump-and-dumps among other claims; total damages ~C$1.2M plus an injunction
  ([vLex](https://ca.vlex.com/vid/nazerali-v-mitchell-691109661); [canadianmedialawyers](https://canadianmedialawyers.com/nazerali-v-mitchell-2016-bcsc-810/)).
  Issuers also sue short-sellers (e.g., *Grifols v. Gotham*, SDNY 2024; [BNN Bloomberg](https://bnnbloomberg.ca/investing/2024/12/20/short-seller-gotham-asks-judge-to-toss-grifols-defamation-suit)).
  US opinion defences exist (*Silvercorp* dismissed, 2012) but are not guaranteed ([Akin Gump PDF](https://www.akingump.com/a/web/8190/aogRB/121001_new_york_court_dismisses_public.pdf)).
- **Biggest exposure is the public "pumped stocks of the month" report** proposed in PLAN §8. Private alerts to customers
  under contract carry lower (but not zero) risk.
- Mitigation: describe **observable signals** ("volume 12× average with no news; 40 identical posts"), not conclusions
  ("this is fraud"). Add a confidence score and a disclaimer. Keep no named individuals in public content. Get a correction process and media-liability insurance.
- Israel's Prohibition of Defamation Law also applies to the Israel-based founder (**UNVERIFIED** specifics).

### 4.2 Investment adviser status
- The Advisers Act §202(a)(11) covers anyone who for compensation "issues or promulgates analyses or reports concerning
  securities". The publisher exclusion (*Lowe v. SEC*, 472 U.S. 181 (1985)) requires content that is **impersonal, bona fide
  (disinterested), and of general and regular circulation, "not timed to specific market activity"**
  ([Cornell LII](https://www.law.cornell.edu/supremecourt/text/472/181); [GT Law on Seeking Alpha, 2024](https://www.gtlaw.com/en/insights/2024/8/no-need-for-seeking-alpha-to-seek-registration)).
- **Risk:** real-time alerts triggered by market events may fail the "not timed to market activity" test. If a *trading app*
  shows alerts to retail users as "avoid/sell" signals, adviser-status risk rises.
- **Mitigation:** position the product as **compliance/surveillance tooling for institutions** (risk signals, not buy/sell
  recommendations). Use contract terms "not investment advice" and avoid retail-facing distribution without counsel review.
  Whether this is enough is **UNVERIFIED**: lawyer question #3.

### 4.3 Market manipulation / insider trading / front-running
- PumpWatch will hold **non-public, price-sensitive alerts**. Trading on them (by the founder, staff, or a leak) risks
  "scalping"/fraud theories (*SEC v. Capital Gains Research Bureau*, 375 U.S. 180 (1963), [LII](https://www.law.cornell.edu/supremecourt/text/375/180)).
  If customer data (S6) is used, trading also risks the misappropriation theory (*US v. O'Hagan*, 521 U.S. 642 (1997), [LII](https://www.law.cornell.edu/supremecourt/text/521/642)).
- Also: a wrong public alert can itself move a price ("short and distort" claims, cf. *Farmland Partners* settlement
  reported by [Institutional Investor](https://www.institutionalinvestor.com/article/2bswuziii3me2otfve5ts/culture/stunning-confessions-of-a-short-seller)).
- Mitigation: written **personal-trading policy** (no trading small-caps on the watch list; pre-clearance), access logs,
  embargo on publication until customers have had the data, never short or long flagged names. This matches the PLAN red line.
- **CFTC:** relevant only if the signals extend to crypto/commodity derivatives (**UNVERIFIED** scope; flagged for later).

### 4.4 FCRA
- FCRA applies to "consumer reports" used for credit, insurance, employment and similar eligibility decisions. A CFPB rule that would have
  treated many data brokers as CRAs was **withdrawn 2025-05-15** ([CFS Law Monitor](https://www.consumerfinancialserviceslawmonitor.com/2025/05/cfpb-withdraws-proposed-fcra-data-broker-rule/)).
- **Risk:** if a broker uses PumpWatch person-level flags to **deny or close a customer account**, a plaintiff could argue
  the output is a consumer report used for eligibility (**UNVERIFIED** theory). Mitigation: no person-level scores about
  account holders; contract clause prohibiting FCRA-purpose use. X's "background checks" ban (§2) points the same way.

---

## 5. LEGAL RED LINES (consolidated)

PLAN §5 lines (unchanged) plus additions from this research (marked **NEW**):

1. No fake identities or sock-puppets to enter closed groups (hiQ fake-profile liability).
2. No WhatsApp scraping.
3. No hacking, credential use, or buying access to private groups.
4. No trading on alerts by anyone at PumpWatch; written personal-trading policy.
5. Data minimisation: no unnecessary personal data.
6. **NEW** No use of X data for this product until **X approves the use case in writing**; no scraping of X (ToS + $15k/1M posts).
7. **NEW** No Telegram collection (API, bot, or scraping) until a lawyer signs off. Current ToS prohibit it and prohibit ML use.
8. **NEW** No Reddit, Meta or Discord data in a paid product without a signed commercial agreement.
9. **NEW** Never log in to a platform account to scrape; never bypass rate limits, CAPTCHAs or blocks.
10. **NEW** No named-person "fraudster" labels in any public output (monthly report, website, social posts). Describe signals, not guilt.
11. **NEW** Default unit of analysis is **ticker + pseudonymised cluster**; identity only on documented customer request.
12. **NEW** No use of outputs for credit, employment, insurance or account-eligibility decisions (FCRA); stated in contract.
13. **NEW** No buy/sell recommendations; product sold as surveillance/compliance tooling to institutions.
14. **NEW** No ingestion of broker customer data (S6) until a security programme exists and Reg S-P service-provider terms (72h notice) are agreed.
15. **NEW** No customer data into third-party LLM APIs that train on inputs (FINRA 2026 GenAI vendor concern).

---

## 6. "Needs a real lawyer": questions ranked by impact

**Tier 1: decides whether the product is viable (ask before Gate B)**
1. **X:** Does flagging pump-promotion accounts and posts for broker-dealers count as "surveillance or gathering intelligence ...
   investigating or tracking X users or X Content" or "profiling ... alleged commission of a crime"? Is a ticker-level
   aggregate (no handles) outside the clause? How do we get "explicit written approval"; via Enterprise?
2. **Telegram:** Given the Content Licensing ToS, is there *any* lawful path to monitor public channels? E.g., logged-off
   `t.me/s/` web previews (does the *Meta v. Bright Data* logic apply; is Telegram's choice of law relevant?), or
   channel-admin consent? Does using a classifier on Telegram text trigger the AI/ML ban?
3. **Adviser status:** Are real-time, event-driven risk alerts sold to broker-dealers "analyses or reports concerning securities"
   requiring registration (federal or state)? Does the answer change if a trading app shows them to retail users?
4. **GDPR Art. 10 + Israeli "especially sensitive data":** Is a "likely promoter" flag criminal-offence data? Can
   pseudonymisation or ticker-level scoring avoid it? Do we need an EU Art. 27 representative?

**Tier 2: needed before first paid pilot**
5. **Defamation:** safe wording for alerts and for any public report; which jurisdictions' law applies (US, Israel, Canada,
   UK); disclaimers; does insurance cover it?
6. **Data broker status:** Are we a "data broker" under the California Delete Act (DROP from 2026-08-01) or other state
   registries? Are we a registrable "data-broker database" under Amendment 13 (>10,000 people)? Do we need a DPO?
7. **Pilot contract:** liability caps, "not investment advice", no-FCRA-use clause, Reg S-P 72h notice, data ownership,
   indemnity for third-party-platform claims, and what to promise about data-source rights.
8. **Reddit / StockTwits licences:** review commercial licence terms once offered. Can derived signals be redistributed to customers?

**Tier 3: before scaling (Gate D/E)**
9. Corporate structure (Delaware parent + Israeli sub) and where data controllers sit, for GDPR and Israeli law.
10. Personal-trading policy and information barriers: are they adequate against insider-trading/scalping theories?
11. If S6 (broker customer data) is pursued: Reg S-P/S-ID obligations, SOC 2 scope, and on-premise options.
12. CFTC/crypto scope if signals expand beyond equities.

---

### Method note
Sources opened directly: X Developer Agreement/Policy/Restricted-uses/ToS/pricing, Reddit Data API and Developer Terms,
Telegram ToS/API/Bot/Content-Licensing pages, StockTwits Terms, Meta automated-data page, FINRA 2026 report (PDF), SEC
press release 2024-58. Other items are from search-result summaries of law-firm and vendor pages (cited); vendor pricing
pages are marketing estimates. Discord policy page returned 403 (UNVERIFIED). Terms checked 2026-10-04.
