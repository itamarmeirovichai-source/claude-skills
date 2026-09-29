# PeakForm research notes

Reviewed 2026-09-29 for a private, offline fitness PWA used by one young volleyball player. These notes explain the evidence and platform facts behind PeakForm defaults. They are not medical advice, and anything touching weight, supplements or injury should be reviewed with a parent and a pediatric clinician or sports dietitian.

## How this research was done

The build environment's network proxy blocked direct page access. WebFetch was tried on fsis.usda.gov, ods.od.nih.gov, webkit.org, developer.mozilla.org, pmc.ncbi.nlm.nih.gov, docs.github.com, openfoodfacts.github.io, developers.google.com, aasm.org, bjsm.bmj.com and both TikTok links, and every request was refused. Web search worked and returned titles, URLs and short snippets.

As a result, every source below is marked "search snippet only". No page, PDF or video was opened or watched. Figures were accepted only when snippets agreed with each other or with the named publisher, and conflicts are listed under Uncertainty. No URL, DOI, video ID or finding was invented; where a detail such as a PMID could not be tied to a page, that is stated. The machine readable version of these records is `src/content/sources.ts` and `src/content/media.ts`.

Two PubMed IDs needed checking:

- PMID 37008451 matches "Creatine supplementation in the pediatric and adolescent athlete: A literature review" (Metzger and colleagues, Journal of Orthopaedics, 2023). The title appeared on several publisher and institutional listings, but the PubMed page itself was not opened.
- PMID 42752819 could not be verified. A search tool summary linked it to "Effects of Resistance Training on Muscle Hypertrophy in Children and Adolescents: A Systematic Review and Meta-Analysis" (Sports Medicine, 2026), and that article does exist on link.springer.com, but no PubMed result was shown to confirm the ID. The author name offered by that summary is not recorded.

## Youth training

### [Resistance Training for Children and Adolescents (clinical report)](https://publications.aap.org/pediatrics/article/145/6/e20201011/76942/Resistance-Training-for-Children-and-Adolescents)

American Academy of Pediatrics, Pediatrics 145(6):e20201011 (Stricker, Faigenbaum, McCambridge; Council on Sports Medicine and Fitness). Source date: June 2020. Access: search snippet only.

- Conclusion: Supervised resistance training with good technique is considered safe and beneficial for adolescents. Snippets describe starting with low resistance until technique is solid, sessions of roughly 20 to 30 minutes 2 to 3 times per week with gradual progression, and no added benefit (with more overuse risk) beyond about 4 sessions per week.
- Product decision: PeakForm keeps the prescribed week: four resistance sessions and two volleyball sessions. It asks for a qualified coach for unfamiliar barbell and jump work, never tests a one rep maximum, and adds reps before load. Four resistance days sits at the upper end of the frequencies in these summaries, so it is listed as a question for a parent and coach.
- Uncertainty: The frequency and duration figures came from search snippets that may quote the 2008 AAP statement or secondary summaries rather than the 2020 report itself. The full report was not opened.

### [Effects of Resistance Training on Muscle Hypertrophy in Children and Adolescents: A Systematic Review and Meta-Analysis](https://pubmed.ncbi.nlm.nih.gov/42752819/)

Sports Medicine (Springer Nature), DOI 10.1007/s40279-026-02499-0. Source date: 2026. Access: search snippet only.

- Conclusion: This meta-analysis (searched April 2025, controlled studies in under 18s with imaging or instrumented hypertrophy measures) suggests muscle growth from training is small before and around puberty and larger after puberty in some comparisons. Snippets reported trivial to small effects versus passive controls and a large effect for postpubertal participants versus active controls.
- Product decision: PeakForm never promises a rate of muscle gain or a date based body composition result, and it has no forecast engine.
- Uncertainty: The article itself was seen in search results on link.springer.com. PMID 42752819 could not be verified against a PubMed page: the only link between that PMID and this title was a search tool summary, and no PubMed result was shown. An author name offered by that summary was not confirmed and is not recorded here. Effect sizes are from snippets and were not checked against the paper.

### [Effects of Plyometric Jump Training on Physical Fitness in Amateur and Professional Volleyball: A Meta-Analysis](https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2021.636140/full)

Frontiers in Physiology (Ramirez-Campillo, Garcia-de-Alcaraz, Chaabene, Moran, Negra, Granacher). Source date: 2021. Access: search snippet only.

- Conclusion: Across 18 studies and 746 volleyball players, plyometric jump training produced small to moderate improvements in sprint, several jump tests, and spike jump height, with larger countermovement jump gains in players aged 16 and over. No included study reported training related injuries.
- Product decision: Jump work follows the prescribed quality reps, stops when height, speed, or landing drops, logs landing quality, and never increases volume automatically.
- Uncertainty: Few participants were under 16, and a separate 2026 adolescent team sport review noted in snippets that adverse events are rarely reported in plyometric studies, so safety evidence is thin rather than proven. Full text was not opened.

### [The Preventive Effect of the Nordic Hamstring Exercise on Hamstring Injuries in Amateur Soccer Players: A Randomized Controlled Trial](https://journals.sagepub.com/doi/abs/10.1177/0363546515574057)

The American Journal of Sports Medicine (van der Horst, Smits, Petersen, Goedhart, Backx). Source date: 2015. Access: search snippet only.

- Conclusion: In a trial that randomised 648 amateur male Dutch soccer players and followed them for a season, adding a Nordic hamstring programme reduced hamstring injury incidence, while injury severity among those injured did not differ.
- Product decision: The Nordic hamstring curl stays at the prescribed 2 sets of 4 to 6. Its difficulty never progresses automatically, and the exercise page gives partner or anchor setup cues and an assisted option.
- Uncertainty: The trial population was adult amateur soccer players, not adolescent volleyball players. The exact analysed sample size and effect size were not confirmed because only snippets were available.

### [Including the Nordic hamstring exercise in injury prevention programmes halves the rate of hamstring injuries: a systematic review and meta-analysis of 8459 athletes](https://www.researchgate.net/publication/331367089_Including_the_Nordic_hamstring_exercise_in_injury_prevention_programmes_halves_the_rate_of_hamstring_injuries_A_systematic_review_and_meta-analysis_of_8459_athletes)

British Journal of Sports Medicine 53:1362-1370 (van Dyk, Behan, Whiteley). Source date: 2019. Access: search snippet only.

- Conclusion: Pooling 15 studies across sports, programmes that included the Nordic hamstring exercise had roughly half the hamstring injury risk of controls (risk ratio about 0.49).
- Product decision: Supports keeping the Nordic curl in the plan, described as hamstring strengthening rather than a guarantee against injury.
- Uncertainty: A 2021 reappraisal (see nordic-reappraisal-2021) argued the pooled effect is less certain than the title suggests. URL points to a ResearchGate listing seen in search results, not the BJSM page.

### [Why methods matter in a meta-analysis: a reappraisal showed inconclusive injury preventive effect of Nordic hamstring exercise](https://www.sciencedirect.com/science/article/abs/pii/S0895435621002870)

Journal of Clinical Epidemiology 140:111-124 (Impellizzeri, McCall, van Smeden). Source date: 2021. Access: search snippet only.

- Conclusion: Re-analysing earlier meta-analyses with more conservative methods and prediction intervals, the authors judged the injury preventive effect of the Nordic hamstring exercise inconclusive, citing possible publication bias and little evidence outside soccer.
- Product decision: App copy describes the Nordic curl as eccentric hamstring strengthening and does not quote an injury reduction percentage.
- Uncertainty: The original authors published a response disputing parts of the reappraisal. Neither paper was opened.

### [Influence of Resistance Training Proximity-to-Failure on Skeletal Muscle Hypertrophy: A Systematic Review with Meta-analysis](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9935748/)

Sports Medicine 53(3):649-665 (Refalo, Helms, Trexler, Hamilton, Fyfe). Source date: March 2023. Access: search snippet only.

- Conclusion: Training to set failure showed only a trivial hypertrophy advantage over stopping short of failure (effect size about 0.19, confidence interval touching zero), so failure is not required for muscle growth.
- Product decision: PeakForm prescribes sets by reps in reserve (2 to 3 in the seeded plan), never prescribes routine failure, and blocks plan edits or imported recommendations below 1 RIR.
- Uncertainty: Participants were adults. RIR estimates are known to be imprecise, especially in novices, which is why the app also logs form and pain.

### [Effects of resistance training performed to repetition failure or non-failure on muscular strength and hypertrophy: A systematic review and meta-analysis](https://pubmed.ncbi.nlm.nih.gov/33497853/)

Journal of Sport and Health Science 11(2):202-211 (Grgic and colleagues). Source date: 2022. Access: search snippet only.

- Conclusion: Across 15 studies in young adults, training to failure did not produce significantly more strength or hypertrophy than non-failure training, and non-failure training favoured strength when volume was not equated.
- Product decision: Reinforces ending sets with reps in reserve. Progression holds or reduces load when logged RIR falls below the prescription.
- Uncertainty: Adult participants only. Full text was not opened.

### [Progressive overload without progressing load? The effects of load or repetition progression on muscular adaptations](https://peerj.com/articles/14142/)

PeerJ (Plotkin and colleagues), DOI 10.7717/peerj.14142. Source date: 2022. Access: search snippet only.

- Conclusion: In 43 trained adults over 8 weeks, progressing repetitions at a fixed load and progressing load in a fixed rep range both produced similar muscle growth, with load progression slightly better for maximal strength.
- Product decision: Supports adding reps before weight, which matters when the smallest available plate or stack step is large relative to the load.
- Uncertainty: Adult, trained, lower body only, short study. Full text was not opened.

### [Double progression (coaching convention, glossary definition)](https://alphaprogression.com/en/glossary/double-progression)

Alpha Progression glossary (commercial training app). Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Double progression means working up to the top of a rep range at a fixed load, then increasing load and returning toward the bottom of the range. It is a widely used coaching rule of thumb, not a protocol that has been tested as such in trials.
- Product decision: PeakForm uses double progression as its default rule and describes it as a coaching convention, not a studied protocol.
- Uncertainty: Source is a commercial glossary used only to define the term. No study was found that tests double progression itself in adolescents.

## Nutrition and energy availability

### [Promotion of Healthy Weight-Control Practices in Young Athletes (clinical report)](https://publications.aap.org/pediatrics/article/140/3/e20171871/38384/Promotion-of-Healthy-Weight-Control-Practices-in)

American Academy of Pediatrics, Pediatrics 140(3):e20171871 (Carl, Johnson, Martin; Council on Sports Medicine and Fitness). Source date: September 2017. Access: search snippet only.

- Conclusion: The AAP advises that when weight change is appropriate for a young athlete it should be gradual and supervised, and it discourages rapid weight change methods such as restriction, dehydration, and weight cycling.
- Product decision: No weight targets, no weigh in streaks, and no praise for weight loss. Calorie targets are ranges to review with a parent, never below 2,000 kcal, and they only change through the fourteen day gate with confirmation.
- Uncertainty: The 1 to 2 lb per week ceiling appears on AAP parent material (see healthychildren-safe-weight-loss). Whether that exact phrasing is in this clinical report could not be confirmed.

### [Safe Weight Loss and Weight Gain for Young Athletes](https://www.healthychildren.org/English/healthy-living/sports/Pages/Safe-Weight-Loss-and-Weight-Gain-for-Young-Athletes.aspx)

HealthyChildren.org (American Academy of Pediatrics parent site). Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Young athletes who lose weight should not lose more than about 1 to 2 pounds per week, because faster loss is often muscle or water. Weight cycling should be avoided and large changes discussed with a doctor first.
- Product decision: If the seven day average falls faster than about 0.7 kg a week after the first week, PeakForm suggests adding 150 to 200 calories and talking with a parent. That threshold sits inside the 1 to 2 lb a week guidance.
- Uncertainty: Page date not visible. Content seen only as a search snippet.

### [Nutrition and Supplement Use (Care of the Young Athlete patient education)](https://publications.aap.org/patiented/article-pdf/720898/peo_document566_en.pdf)

American Academy of Pediatrics, Pediatric Patient Education (peo_document566). Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Nutrition needs of young athletes are best met with balanced meals rather than supplements. The handout advises steady hydration without waiting for thirst, a carbohydrate rich meal 3 to 4 hours before exercise and a smaller carbohydrate snack about 1 hour before, and warns that supplements have quality and contamination problems.
- Product decision: Meal templates are food first with a carbohydrate pre training meal. Supplements are a tracker only, and creatine logging needs a one time parent and clinician confirmation.
- Uncertainty: Handout date and edition unknown. Read only through search snippets of the AAP page and a hosted copy.

### [2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs)](https://bjsm.bmj.com/content/57/17/1073.long)

British Journal of Sports Medicine 57(17):1073-1097 (Mountjoy, Ackerman, Burke, Stellingwerff and others). Source date: September 2023. Access: search snippet only.

- Conclusion: REDs is a syndrome of health and performance harms in male and female athletes caused by low energy availability, which ranges from adaptable to problematic. The statement updates its conceptual models and adds a physiological model of individual risk factors.
- Product decision: PeakForm treats underfuelling as a safety issue. It flags fast weight loss, fully logged days under 2,000 kcal, falling energy, mood, or concentration, repeated illness, and recorded red flags, and responds by pausing progression and asking to involve a parent and clinician, never with a diagnosis.
- Uncertainty: The page was blocked. Specific screening tools and cut offs in the statement were not reviewed.

### [Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate, chapter 25 (National Academies reader page)](https://www.nationalacademies.org/read/10925/chapter/25)

Institute of Medicine, National Academies Press (DOI 10.17226/10925). Source date: 2005. Access: search snippet only.

- Conclusion: The carbohydrate RDA is 130 g per day for males aged 14 to 18 (the same value applies from age 1 through adulthood), based on the glucose needs of the brain. Search results from National Academies DRI summary material confirmed the 130 g figure.
- Product decision: Carbohydrate targets can never be saved below 130 g a day. The seeded targets are 190 to 285 g because training needs more.
- Uncertainty: This URL belongs to the water and electrolytes DRI volume. Chapter 25 could not be opened, so it is not confirmed whether it is a summary table, an index, or other back matter. The primary source for the carbohydrate RDA is the macronutrient DRI report (NAP 10490).

### [Calorie for Calorie, Dietary Fat Restriction Results in More Body Fat Loss than Carbohydrate Restriction in People with Obesity](https://pmc.ncbi.nlm.nih.gov/articles/PMC4603544/)

Cell Metabolism (Hall and colleagues, NIH). Source date: August 2015. Access: search snippet only.

- Conclusion: In a metabolic ward, 19 adults with obesity each spent 6 days on equal calorie cuts from fat or from carbohydrate. Cutting carbohydrate increased fat oxidation, but cutting fat produced slightly more body fat loss, so lower carbohydrate intake was not metabolically superior under tight control.
- Product decision: PeakForm does not promote low carbohydrate eating for fat loss, explains that insulin rising after meals is normal, and keeps measured carbohydrate around training.
- Uncertainty: Adults with obesity, very short duration, not athletes or adolescents. Details come from snippets and press summaries.

### [Optimizing Performance Nutrition for Adolescent Athletes: A Review of Dietary Needs, Risks, and Practical Strategies](https://www.mdpi.com/2072-6643/17/17/2792)

Nutrients 17(17):2792 (MDPI). Source date: 2025. Access: search snippet only.

- Conclusion: Sports nutrition literature suggests adolescent athletes need more protein than the general guideline of about 0.75 to 1.05 g/kg, commonly cited as 1.2 to 2.0 g/kg, with about 1.5 g/kg often mentioned as enough to stay in positive nitrogen balance during growth. Spreading 20 to 40 g across meals is a common practical suggestion.
- Product decision: Protein targets are the seeded 150 to 175 g a day from food, with protein powder optional. Depending on body weight that can sit above this review's range per kilogram, and the default meals supply about 200 g with standard food values. This is flagged for review with a pediatric sports dietitian.
- Uncertainty: The figures came from a search summary that drew on several results (this review, a Brazilian cross sectional study at PMC9520475, and others). Which paper states the 1.5 g/kg nitrogen balance point was not confirmed.

### [Calcium: Fact Sheet for Consumers](https://ods.od.nih.gov/factsheets/Calcium-Consumer/)

NIH Office of Dietary Supplements. Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Teens aged 14 to 18 need 1,300 mg of calcium per day, and people aged 9 to 18 should not exceed 3,000 mg per day from food and supplements combined.
- Product decision: The Eat screen adds calcium from food and supplements against about 1,300 mg a day and shows a note if the total passes 2,500 mg, below the 3,000 mg upper limit.
- Uncertainty: Page date not visible. Figures confirmed only through search snippets.

## Body composition measurement

### [Accuracy of Smart Scales on Weight and Body Composition: Observational Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8122302/)

JMIR mHealth and uHealth (Frija-Masson, Mullaert, Vidal-Petiot, Pons-Kerjean, Flamant, d'Ortho). Source date: April 2021. Access: search snippet only.

- Conclusion: This is not a general review of bioelectrical impedance. It compared three consumer smart scales with DEXA in adult patients and found them accurate for total body weight but not reliable enough to use routinely for body composition, especially in severe obesity.
- Product decision: Smart scale body fat is optional, labelled trend only, shown only as weekly averages when there are at least three readings, and never used for nutrition decisions.
- Uncertainty: Adults in a clinical setting with specific scale models, so results may not transfer to a lean adolescent or newer devices. Findings seen only as snippets.

## Sleep and recovery

### [Health Advisory: Teen Sleep Duration](https://aasm.org/wp-content/uploads/2017/10/teen-sleep-duration-health-advisory.pdf)

American Academy of Sleep Medicine. Source date: 2017 (URL path); based on the 2016 AASM pediatric consensus (Paruthi and colleagues). Access: search snippet only.

- Conclusion: Teens aged 13 to 18 should regularly sleep 8 to 10 hours per 24 hours. Regular short sleep is linked to attention, learning and mood problems, more injuries and accidents, and other health risks.
- Product decision: The sleep target is 8 to 10 hours. The check in shows duration against it, readiness eases off after short nights, and the weekly review flags averages under eight hours.
- Uncertainty: PDF was blocked. The advisory publication date is inferred from the URL path.

### [Chronic Lack of Sleep is Associated With Increased Sports Injury in Adolescents: A Systematic Review and Meta-analysis](https://journals.sagepub.com/doi/10.1177/2325967119S00132)

Orthopaedic Journal of Sports Medicine (meeting abstract; Gao, Dwivedi, Milewski, Cruz). Source date: 2019. Access: search snippet only.

- Conclusion: This meta-analysis abstract links chronic short sleep with higher sports injury rates in adolescents. It builds on earlier work by Milewski and colleagues (2014) reporting that adolescent athletes sleeping under 8 hours were about 1.7 times more likely to be injured.
- Product decision: Sleep feeds the readiness indicator and the weekly review. PeakForm does not change the plan by itself.
- Uncertainty: Observational association, not proof that more sleep prevents injury. This is a conference abstract, and the 1.7 figure came from a secondary review snippet.

### [Sleep extension in athletes: what we know so far - A systematic review](https://pubmed.ncbi.nlm.nih.gov/33352457/)

Sleep Medicine (listed on ScienceDirect and PubMed 33352457). Source date: 2020 or 2021 (not confirmed). Access: search snippet only.

- Conclusion: Limited, lower quality evidence suggests that extending sleep may improve some measures of sports performance, with the size of the benefit depending on the outcome measured.
- Product decision: Sleep advice is framed as supporting recovery, mood and learning, without promising specific performance gains.
- Uncertainty: Journal name inferred from the ScienceDirect article code; publication year not confirmed. Evidence quality is low by the authors own account, and the age mix of included athletes was not checked.

## Supplements

### [Omega-3 Fatty Acids: Fact Sheet for Consumers](https://ods.od.nih.gov/factsheets/Omega3FattyAcids-Consumer/)

NIH Office of Dietary Supplements. Source date: Not stated in search result. Access: search snippet only.

- Conclusion: EPA and DHA come mainly from fish and seafood, and children and teens get very little from typical diets. The FDA suggests no more than 3 g per day of EPA plus DHA combined, with up to 2 g from supplements, and supplement labels should not recommend more than 2 g per day.
- Product decision: The plan includes fish at three dinners a week. The supplement tracker asks for EPA plus DHA from the label, not the total fish oil amount.
- Uncertainty: The label reading tip (total oil versus EPA plus DHA) came from a non government snippet. No adolescent specific omega-3 dose is set by ODS.

### [International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation in exercise, sport, and medicine](https://pubmed.ncbi.nlm.nih.gov/28615996/)

Journal of the International Society of Sports Nutrition 14:18 (Kreider and colleagues). Source date: June 2017. Access: search snippet only.

- Conclusion: The ISSN considers creatine monohydrate acceptable for adolescent athletes only with proper precautions and supervision: serious supervised training, a good diet, understanding of correct use, and recommended doses. It reported no evidence of harm at recommended doses in under 18s.
- Product decision: PeakForm never suggests creatine. If a parent and clinician have reviewed it, the tracker can record the product and dose.
- Uncertainty: ISSN is a sports nutrition society with industry ties, and pediatric bodies such as the AAP are more cautious about supplements in minors.

### [Creatine supplementation in the pediatric and adolescent athlete: A literature review](https://pubmed.ncbi.nlm.nih.gov/37008451/)

Journal of Orthopaedics 38:73-78 (Metzger, Minneci, Gehred, Day, Klingele), DOI 10.1016/j.jor.2023.03.010. Source date: 2023. Access: search snippet only.

- Conclusion: The authors found the pediatric creatine literature to be of poor overall quality, with no consistent performance findings and no studies designed to assess safety, and advised clinicians to explain these gaps to young athletes and families.
- Product decision: Together with the ISSN stand, this is why creatine logging stays locked until a one time parent and clinician confirmation.
- Uncertainty: PMID 37008451 was matched to this title by a search summary and the same title appeared on ScienceDirect, Nemours and jortho.org listings, so the match is likely but the PubMed page itself was not opened.

## Food safety

### [Leftovers and Food Safety](https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety)

USDA Food Safety and Inspection Service. Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Refrigerate cooked food within 2 hours (1 hour above 90 F) in shallow containers at 40 F (4 C) or below, use most leftovers within 3 to 4 days, and reheat to 165 F (74 C) or until hot and steaming. Frozen food at 0 F stays safe indefinitely, with storage times given for quality only.
- Product decision: Meal preparation labels containers by day and meal, lists the two hour rule, the 4 °C fridge, the three to four day limit, and reheating to 74 °C.
- Uncertainty: Page could not be opened. The 1 hour above 90 F rule and freezer note came from FSIS snippets on related pages.

### [Safe Minimum Internal Temperatures](https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures)

FoodSafety.gov (US Department of Health and Human Services). Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Cook poultry to 165 F (74 C), fish to 145 F (63 C), ground beef to 160 F (71 C), and beef steaks and roasts to 145 F (63 C) with a 3 minute rest, checked with a food thermometer.
- Product decision: Recipes with meat, poultry, or fish state the minimum internal temperature in °C, and the preparation screen lists 74, 63, and 71 °C.
- Uncertainty: Page could not be opened; values match snippets from FoodSafety.gov, FSIS and FDA charts.

## iPhone and PWA behaviour

Summary for iPhone:

- Web Push: iOS and iPadOS 16.4 and later, Home Screen web apps only, permission only from a user tap. Declarative Web Push arrived in 18.4.
- Screen Wake Lock: in Safari tabs since 16.4, and in Home Screen web apps only since iOS 18.4 (WebKit bug 254545 was the earlier gap).
- Vibration: navigator.vibrate is listed as unsupported on iOS. A March 2026 report says it works, but that is disputed, so PeakForm does not depend on it.
- Sharing files: Web Share level 2 (files) since Safari 15 on iOS; check navigator.canShare first and call share() from a tap.
- Storage: since iOS 17, quotas scale with disk size and WebKit may evict whole origins when overall usage is high, unless the origin is persistent (navigator.storage.persist()). Separately, Safari tabs lose script writable storage after 7 days of Safari use without visiting the site; Home Screen web apps keep their own counter based on their own use. Installing the app and exporting backups are the real protections.
- BarcodeDetector: not available in Safari or any iOS browser.

### [Web Push for Web Apps on iOS and iPadOS](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/)

WebKit blog (Brady Eidson, Jen Simmons). Source date: February 16, 2023. Access: search snippet only.

- Conclusion: iOS and iPadOS 16.4 added Web Push and the Badging API for web apps added to the Home Screen only, not for pages in a Safari tab. Permission can only be requested in response to a direct user action such as tapping a button.
- Product decision: PeakForm does not use Web Push, because it needs a push server. Reminders come from the in app timeline and an Apple Calendar export with alarms.
- Uncertainty: Blocked page; details from snippets and secondary sources. PeakForm is offline first and would need a push server to send pushes, which conflicts with its private design, so local reminders may be preferable.

### [Sending web push notifications in web apps and browsers](https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers)

Apple Developer Documentation. Source date: Not stated in search result. Access: search snippet only.

- Conclusion: Apple documents standards based Web Push (Push API, Notifications API, service workers). For iOS Home Screen web apps the manifest display member must be standalone or fullscreen and permission must follow a user gesture.
- Product decision: The manifest uses display standalone. Push is not used.
- Uncertainty: Manifest requirement came from a third party summary of Apple guidance; the Apple page was not opened.

### [WebKit Features in Safari 18.4](https://webkit.org/blog/16574/webkit-features-in-safari-18-4/)

WebKit blog. Source date: 2025. Access: search snippet only.

- Conclusion: Safari 18.4 made the Screen Wake Lock API work in Home Screen web apps on iOS and iPadOS 18.4, fixing a gap since 16.4 where it only worked in Safari tabs (WebKit bug 254545). It also added Declarative Web Push for Home Screen web apps, which does not need a service worker to show notifications.
- Product decision: During workouts PeakForm requests a screen wake lock when the browser supports it and releases it afterwards. Where it is unsupported, nothing breaks.
- Uncertainty: Release note seen as snippets. Wake lock is still released when the app goes to the background or the phone locks.

### [Screen Wake Lock API support table](https://caniuse.com/wake-lock)

Can I use. Source date: Continuously updated. Access: search snippet only.

- Conclusion: Safari on iOS supports Screen Wake Lock from 16.4, recorded as partial from 16.4 until 18.4 because it did not work in standalone Home Screen web apps. All iOS browsers use WebKit, so the same limits apply to them.
- Product decision: Wake lock is feature detected. The rest timer uses an absolute end time, so it stays correct after the screen locks, but sounds only play while PeakForm is open.
- Uncertainty: Snippet level only; current version ranges may have changed.

### [Navigator API: vibrate support table](https://caniuse.com/mdn-api_navigator_vibrate)

Can I use (MDN browser compat data). Source date: Continuously updated. Access: search snippet only.

- Conclusion: Compatibility data lists navigator.vibrate as unsupported in Safari on iOS, and WebKit has not announced support. A March 2026 issue on MDN browser-compat-data (#29166) reported that it works on current iOS Safari, which conflicts with other 2026 reports that it silently does nothing.
- Product decision: PeakForm does not rely on vibration. The timer end shows a clear visual state and plays a sound while the app is open. The vibrate call is a harmless extra that does nothing on iPhone.
- Uncertainty: Real support status on current iOS is disputed. It should be tested on the actual iPhone before any vibration feature is described to the user.

### [WebKit Features in Safari 18.0](https://webkit.org/blog/15865/webkit-features-in-safari-18-0/)

WebKit blog. Source date: 2024. Access: search snippet only.

- Conclusion: Safari on iOS 18 gives haptic feedback when a user toggles an input type checkbox with the switch attribute, the only official web haptic on iPhone found in this review.
- Product decision: PeakForm does not use hidden switch tricks to fake vibration.
- Uncertainty: Details from snippets. Third party libraries exploit this for arbitrary haptics, which may break in future iOS versions.

### [Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/)

WebKit blog (Sihui Liu). Source date: August 10, 2023. Access: search snippet only.

- Conclusion: From Safari 17 and iOS 17, storage quotas are based on disk size (up to 80 percent of disk overall for browser apps, up to 20 percent for other apps), and WebKit evicts data by origin when total usage exceeds the overall quota. An origin in persistent mode, requested with navigator.storage.persist(), is exempt from that eviction.
- Product decision: PeakForm asks for persistent storage when setup finishes, shows the result in More, Backup, keeps data small, and shows the last backup date on Today.
- Uncertainty: Blocked page. How Safari decides whether to grant persist() on iOS, and whether a Home Screen app counts as a browser app for quota, were not confirmed.

### [Full Third-Party Cookie Blocking and More](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/)

WebKit blog (John Wilander). Source date: March 24, 2020. Access: search snippet only.

- Conclusion: Since iOS 13.4 and Safari 13.1, Intelligent Tracking Prevention deletes all script writable storage (IndexedDB, localStorage, service worker registrations and more) after 7 days of Safari use without user interaction on the site. Home Screen web apps are not part of Safari and keep their own day counter that resets when the app is used.
- Product decision: The install guide puts Add to Home Screen first, the backup screen explains that data in a plain Safari tab can be cleared after about a week without a visit, and Today shows the last backup date.
- Uncertainty: Snippets only. Apple has not documented every edge case, for example a Home Screen app that is not opened for a long time.

### [StorageManager: persist() method](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist)

MDN Web Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: persist() asks the browser to mark the origin storage as persistent and resolves to true only if granted. By default origins are best effort and can be evicted; persistent data can only be removed by the user. Snippets indicate Safari 17 supports the Storage API including persist().
- Product decision: Persistence is requested once at setup and on demand, the result is shown, and it is never assumed.
- Uncertainty: Blocked page. Support version for Safari came from a WebKit snippet rather than MDN compat tables.

### [Navigator: share() method](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share)

MDN Web Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: The Web Share API opens the system share sheet. Safari 15 on iOS added level 2 support, which allows sharing files; navigator.canShare can check whether given files are shareable, while share() itself needs a user gesture.
- Product decision: Exports use navigator.share with files when canShare confirms support, straight from a tap, and fall back to a download otherwise.
- Uncertainty: The iOS 15 file sharing detail came from developer blog snippets; some bug reports mention inconsistencies on specific 15.x versions.

### [Share data between apps](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/How_to/Share_data_between_apps)

MDN Web Docs (Progressive web apps how to). Source date: Continuously updated. Access: search snippet only.

- Conclusion: PWAs can share out with the Web Share API and can receive shared content through the share_target manifest member, which requires the PWA to be installed and uses a POST with multipart form data for files.
- Product decision: PeakForm only shares out. It does not use share_target.
- Uncertainty: The statement that share_target does not work on iOS is prior knowledge and was not confirmed in this review.

### [Progressive Web Apps reference](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference)

MDN Web Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: MDN lists the manifest members (such as name, short_name, scope, shortcuts) and service worker APIs (Cache, Clients, fetch event) that PWAs use for installation and offline behaviour.
- Product decision: PeakForm precaches the app with a service worker for offline use and ships a manifest with name, short_name, icons, start_url, scope, and display standalone.
- Uncertainty: Reference index only; per feature Safari support must be checked separately.

### [Making PWAs installable](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable)

MDN Web Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: Install prompts use the manifest name and icons, and start_url and display control launch. Chromium requires HTTPS, a service worker and key manifest fields for its prompt, while Safari on iOS installs through the Add to Home Screen option in the share menu.
- Product decision: The app includes a short Add to Home Screen guide, because iOS has no automatic install prompt.
- Uncertainty: Snippets only.

### [Barcode Detection API](https://developer.mozilla.org/en-US/docs/Web/API/Barcode_Detection_API)

MDN Web Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: BarcodeDetector is not implemented in Safari or any iOS browser. It existed only behind an experimental flag in Safari 17 and reports say that flag broke with iOS 18.
- Product decision: Barcode lookup uses a typed barcode number with an optional Open Food Facts query. There is no camera scanning, because Safari has no BarcodeDetector. Manual label entry is always available.
- Uncertainty: Status from snippets and an Apple developer forum thread title; not tested on device.

### [Apple reverses decision about blocking web apps on iPhones in the EU](https://techcrunch.com/2024/03/01/apple-reverses-decision-about-blocking-web-apps-on-iphones-in-the-eu/)

TechCrunch. Source date: March 1, 2024. Access: search snippet only.

- Conclusion: Apple planned to remove Home Screen web apps in the EU in iOS 17.4 betas, then reversed that and kept the existing capability, so installed web apps in the EU continued to work as before.
- Product decision: No region specific code. Installation should be checked on the actual phone.
- Uncertainty: Some 2026 third party guides still claim push does not work in the EU; that was not verified and may be outdated.

## Hosting

Decision: PeakForm is published on a Cloudflare Pages project that the user owns, behind a same origin password gate, because the user asked that nobody else be able to open or install the app. A GitHub Pages site on the free plan is open to anyone with the address, so it was dropped. Cloudflare Access was considered, but its sign in redirects to another domain, which can loop inside an iPhone Home Screen app, so the gate signs in on the same origin instead. Netlify is not recommended because its credit based free plan pauses sites when 300 monthly credits run out and each production deploy costs 15 credits. None of these hosts ever receives user data, since PeakForm keeps everything on the device.

### [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

GitHub Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: GitHub Pages is available for public repositories on GitHub Free, and for private repositories only on paid plans (Pro, Team, Enterprise). Sites on github.io are served over HTTPS automatically.
- Product decision: Not used for PeakForm. A GitHub Pages site on the free plan can be opened by anyone with the address, and the user wants nobody else to be able to open or install the app.
- Uncertainty: Snippet level; plan terms change.

### [GitHub Pages limits](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits)

GitHub Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: Published sites may be no larger than 1 GB, have a soft bandwidth limit of 100 GB per month, and a soft limit of 10 builds per hour that does not apply when publishing with a custom GitHub Actions workflow.
- Product decision: Not relevant now that PeakForm is published on Cloudflare Pages.
- Uncertainty: Snippet level.

### [Cloudflare Pages limits](https://developers.cloudflare.com/pages/platform/limits/)

Cloudflare Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: The free plan allows 500 builds per month and 20,000 files per site, with a 25 MiB limit per file, and snippets describe bandwidth as unlimited. A January 2026 changelog raised the file limit for paid plans only.
- Product decision: PeakForm is published on a Cloudflare Pages project owned by the user and built from this repository. It uses a tiny fraction of these limits.
- Uncertainty: Private repository support and the note that Cloudflare now steers new projects toward Workers static assets are from prior knowledge, not confirmed here. Unlimited bandwidth came from third party snippets.

### [Middleware](https://developers.cloudflare.com/pages/functions/middleware/)

Cloudflare Pages Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: A functions/_middleware file that exports onRequest runs before every request to the project, including static files. The functions folder sits at the project root or the configured root directory, not in the build output.
- Product decision: functions/_middleware.ts runs the password gate in front of every file, so no part of the app is served without the password.
- Uncertainty: Snippet level; the page itself was blocked. The behaviour was checked locally with Wrangler 4.143 in the Cloudflare runtime.

### [Secrets](https://developers.cloudflare.com/workers/configuration/secrets/)

Cloudflare Workers Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: A Pages project's Settings, Variables and Secrets, Add, with Encrypt selected, stores a value that cannot be viewed again and is available to Functions on context.env. It has to be set before the deployment that uses it.
- Product decision: The site password is the encrypted PEAKFORM_PASSWORD variable, never in the repository. Without it, the gate serves nothing.
- Uncertainty: Snippet level; dashboard labels change over time.

### [Build image](https://developers.cloudflare.com/pages/configuration/build-image/)

Cloudflare Pages Docs. Source date: Continuously updated. Access: search snippet only.

- Conclusion: The Node.js version for a build can be set with a NODE_VERSION environment variable or a .node-version or .nvmrc file in the project.
- Product decision: peakform/.node-version pins Node 22, which Vite 8 needs.
- Uncertainty: Snippet level.

### [How credits work (credit-based pricing plans)](https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/)

Netlify Docs. Source date: Credit plans for new accounts from September 4, 2025; rates updated April 14, 2026. Access: search snippet only.

- Conclusion: New Netlify accounts use credit based plans. The Free plan gives 300 credits per month, a production deploy costs 15 credits, bandwidth is metered in credits per GB, and sites pause until the next month when free credits run out.
- Product decision: Not used. A paused site would block installing or updating the app.
- Uncertainty: Snippets disagreed on bandwidth cost (10 or 20 credits per GB); Netlify docs snippets said 20, and an April 2026 changelog updated rates without the new figure being visible.

## Media and food data

Exercise and recipe videos are recorded in `src/content/media.ts`. youtube.com could not be opened, so every record is a title and channel match from search results, marked `metadata-match`, and none was watched.

- 31 of the 45 requested exercise IDs have a video: 19 from Renaissance Periodization (17 short technique clips filmed at Exile Gym, Baltimore, mostly October 2019, plus two 2012 bench press uploads), 3 from E3 Rehab (Nordic curl, Copenhagen plank, cable external rotation), 2 from Squat University (back squat, Bulgarian split squat), and one each from Children's Hospital Colorado, Bret Contreras, John Meadows (Mountain Dog), USA Volleyball, The Art of Coaching Volleyball, the Olympics channel and Hinge Health.
- No record for: romanian-deadlift (two uploads carry the title of a Jeff Nippard RDL tutorial, and search results did not show which one is on his channel), tibialis-raise, cable-hip-abduction, seated-calf-raise, flat-cable-fly (only a standing cable flye was found), palm-down-wrist-curl, easy-jump-rope, volleyball-approach-jump, countermovement-jump, shuffle-to-sprint, medicine-ball-spike-throw, lateral-block-jump, block-to-spike-transition (an AVCA video exists but its uploading channel was unclear), ten-metre-sprint. These fall back to the written steps and illustrations in each exercise entry.
- Four recipe videos: BBC Good Food overnight oats (toppings add honey and nut butter), America's Test Kitchen one pan salmon with broccoli and red potatoes (oil amount not checked), America's Test Kitchen red lentil soup (onions cooked in butter, so not low oil as filmed), and Downshiftology one pan chicken and rice (chicken thighs and olive oil, not boxed meal prep).
- Embeds should use youtube-nocookie.com, load only on tap, and keep rel=0 and playsinline=1.

### [YouTube Embedded Players and Player Parameters](https://developers.google.com/youtube/player_parameters)

Google for Developers (YouTube IFrame Player API). Source date: Continuously updated. Access: search snippet only.

- Conclusion: Since September 25, 2018, rel=0 no longer hides related videos; it limits them to the same channel. The showinfo parameter was deprecated, so title and channel always show. Parameters such as start, end, playsinline and cc_load_policy remain available.
- Product decision: Videos load only after a tap, never autoplay, and use rel=0 and playsinline=1. PeakForm never downloads or rehosts video.
- Uncertainty: The playsinline and cc_load_policy details are prior knowledge; the page itself was blocked.

### [Embed videos and playlists (privacy-enhanced mode)](https://support.google.com/youtube/answer/171780)

YouTube Help. Source date: Continuously updated. Access: search snippet only.

- Conclusion: Privacy-enhanced mode uses the youtube-nocookie.com domain so that views do not personalise the viewer experience on YouTube and ads are non personalised. Independent 2026 tests reported that no cookies are set on load, but the player still writes local storage and contacts Google before playback and sets cookies after play.
- Product decision: Embeds use youtube-nocookie.com and load only after a tap on a placeholder, with a note that YouTube may set cookies once playing.
- Uncertainty: The storage and telemetry behaviour came from third party blog snippets, not from Google.

### [Introduction to Open Food Facts API documentation](https://openfoodfacts.github.io/openfoodfacts-server/api/)

Open Food Facts (Product Opener server docs). Source date: Continuously updated. Access: search snippet only.

- Conclusion: Reads need no API key. Product lookup is GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json, clients should send a descriptive User-Agent naming the app, and there are per IP rate limits with possible IP bans when exceeded.
- Product decision: Lookups are optional, one barcode at a time after a tap, and only the barcode number is sent. Browsers cannot set a custom User-Agent, so none is sent. Results are labelled as community data to check against the label.
- Uncertainty: The brief expected 100 requests per minute for product reads, but search snippets quoting the official docs said 15 per minute per IP for product reads and 10 per minute for search; a 100 per minute figure appeared only in a third party project. The live docs must be checked before relying on either number.

### [Terms of use, contribution and re-use](https://world.openfoodfacts.org/terms-of-use)

Open Food Facts. Source date: Not stated in search result. Access: search snippet only.

- Conclusion: The database is licensed under the Open Database License (ODbL), individual contents under the Database Contents License, and product images under CC BY-SA. Reuse requires attribution and share alike for adapted databases.
- Product decision: Food data from a lookup is labelled as coming from Open Food Facts under the ODbL, and no product images are used.
- Uncertainty: Snippets only; the implications of ODbL share alike for a private single user cache are low but not reviewed by a lawyer.

## Social media claims

Two TikTok links from the user were reviewed. Both short links were blocked by the proxy, and searches for the short codes returned nothing about the videos. Neither claim could be seen, so neither changes the app. Records are in `CLAIM_REVIEWS` in `src/content/media.ts`.

| Link | Accessible | What was claimed | Verdict |
| --- | --- | --- | --- |
| [vt.tiktok.com/ZSbhYxd9R](https://vt.tiktok.com/ZSbhYxd9R/) | No | Not visible: the video could not be opened from the build environment. | Not reviewed, no change |
| [vt.tiktok.com/ZSbh2L6Fg](https://vt.tiktok.com/ZSbh2L6Fg/) | No | Not visible: the video could not be opened from the build environment. | Not reviewed, no change |

Context only: the user earlier noticed that another app seemed to miss upper back, calves and forearms, so these videos may be about muscle coverage or exercise selection. That was not assumed. The current library does include upper back work (face pull, reverse machine fly, high row, seated cable row), calves (standing and seated calf raise, tibialis raise) and forearms (palm up and palm down wrist curls, hammer curl). To review either video, the next step is the creator name, the caption, and the exact claim, which can then be compared with the sources above. Social media claims are treated as leads, not evidence.

## Open questions for a parent and a pediatric sports dietitian or clinician

1. Is the athlete cleared for supervised barbell squats, bench press and hip thrusts, and who will supervise the heavier sessions?
2. How many total weekly sessions (volleyball practice, matches, gym, jump work) are appropriate right now, and what should be cut first in a heavy tournament week?
3. Is there any history of Osgood-Schlatter, Sever's disease, back pain, shoulder pain or a previous hamstring strain that should change exercise choices?
4. What daily energy intake range is appropriate for the athlete's growth and training, and should the app show calories at all or only meal structure?
5. Is the protein guide of about 1.3 to 1.8 g/kg per day reasonable for the athlete, and should it be adjusted for body weight and growth stage?
6. Should body weight be logged at all, and if so how often? What rate of change should prompt a check in, given AAP guidance against losing more than 1 to 2 lb per week?
7. What early signs of low energy availability (REDs) should the family watch for, and who should the app point to if they appear?
8. Is creatine, fish oil, vitamin D or any other supplement appropriate for the athlete, and if so, which third party tested product and dose?
9. Is the athlete reaching about 1,300 mg of calcium per day from food, and is vitamin D testing needed?
10. Is 8 to 10 hours of sleep realistic with the school and practice schedule, and what should the app suggest on weeks when it is not?
11. Are there any food allergies, intolerances or family food rules the recipes must respect?
12. Which of the matched YouTube videos should an adult watch first and approve before the athlete uses them as technique references?
13. The default meals, as prescribed, calculate to about 2,400 to 2,600 kcal, which matches the calorie targets. With standard food values they supply about 200 to 215 g protein and 60 to 70 g fat, while the targets say about 150 to 155 g protein and 88 to 92 g fat. Should portions change, or should the macro targets be updated?
