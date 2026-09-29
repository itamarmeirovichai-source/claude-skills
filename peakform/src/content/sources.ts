import type { SourceReference } from './types';

/**
 * Research sources behind PeakForm defaults, reviewed 2026-09-29.
 *
 * Access note: the build environment's egress proxy blocked every page fetch that was tried
 * (fsis.usda.gov, ods.od.nih.gov, webkit.org, developer.mozilla.org, pmc.ncbi.nlm.nih.gov,
 * docs.github.com, openfoodfacts.github.io, developers.google.com, aasm.org, bjsm.bmj.com,
 * vt.tiktok.com). Only web search results (titles, URLs, snippets) were available, so no
 * record is marked 'full-text' or 'abstract-or-summary'. Figures below should be re-checked
 * against the live page before they are treated as final.
 */
export const SOURCES: SourceReference[] = [
  // ---------- Youth training ----------
  {
    id: 'aap-resistance-training-2020',
    title: 'Resistance Training for Children and Adolescents (clinical report)',
    publisher: 'American Academy of Pediatrics, Pediatrics 145(6):e20201011 (Stricker, Faigenbaum, McCambridge; Council on Sports Medicine and Fitness)',
    url: 'https://publications.aap.org/pediatrics/article/145/6/e20201011/76942/Resistance-Training-for-Children-and-Adolescents',
    published: 'June 2020',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Supervised resistance training with good technique is considered safe and beneficial for adolescents. Snippets describe starting with low resistance until technique is solid, sessions of roughly 20 to 30 minutes 2 to 3 times per week with gradual progression, and no added benefit (with more overuse risk) beyond about 4 sessions per week.',
    productDecision:
      'PeakForm keeps the prescribed week: four resistance sessions and two volleyball sessions. It asks for a qualified coach for unfamiliar barbell and jump work, never tests a one rep maximum, and adds reps before load. Four resistance days sits at the upper end of the frequencies in these summaries, so it is listed as a question for a parent and coach.',
    uncertainty:
      'The frequency and duration figures came from search snippets that may quote the 2008 AAP statement or secondary summaries rather than the 2020 report itself. The full report was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'youth-hypertrophy-meta-2026',
    title: 'Effects of Resistance Training on Muscle Hypertrophy in Children and Adolescents: A Systematic Review and Meta-Analysis',
    publisher: 'Sports Medicine (Springer Nature), DOI 10.1007/s40279-026-02499-0',
    url: 'https://pubmed.ncbi.nlm.nih.gov/42752819/',
    published: '2026',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'This meta-analysis (searched April 2025, controlled studies in under 18s with imaging or instrumented hypertrophy measures) suggests muscle growth from training is small before and around puberty and larger after puberty in some comparisons. Snippets reported trivial to small effects versus passive controls and a large effect for postpubertal participants versus active controls.',
    productDecision:
      'PeakForm never promises a rate of muscle gain or a date based body composition result, and it has no forecast engine.',
    uncertainty:
      'The article itself was seen in search results on link.springer.com. PMID 42752819 could not be verified against a PubMed page: the only link between that PMID and this title was a search tool summary, and no PubMed result was shown. An author name offered by that summary was not confirmed and is not recorded here. Effect sizes are from snippets and were not checked against the paper.',
    access: 'search-snippet',
  },
  {
    id: 'volleyball-plyometric-meta-2021',
    title: 'Effects of Plyometric Jump Training on Physical Fitness in Amateur and Professional Volleyball: A Meta-Analysis',
    publisher: 'Frontiers in Physiology (Ramirez-Campillo, Garcia-de-Alcaraz, Chaabene, Moran, Negra, Granacher)',
    url: 'https://www.frontiersin.org/journals/physiology/articles/10.3389/fphys.2021.636140/full',
    published: '2021',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Across 18 studies and 746 volleyball players, plyometric jump training produced small to moderate improvements in sprint, several jump tests, and spike jump height, with larger countermovement jump gains in players aged 16 and over. No included study reported training related injuries.',
    productDecision:
      'Jump work follows the prescribed quality reps, stops when height, speed, or landing drops, logs landing quality, and never increases volume automatically.',
    uncertainty:
      'Few participants were under 16, and a separate 2026 adolescent team sport review noted in snippets that adverse events are rarely reported in plyometric studies, so safety evidence is thin rather than proven. Full text was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'nordic-van-der-horst-2015',
    title: 'The Preventive Effect of the Nordic Hamstring Exercise on Hamstring Injuries in Amateur Soccer Players: A Randomized Controlled Trial',
    publisher: 'The American Journal of Sports Medicine (van der Horst, Smits, Petersen, Goedhart, Backx)',
    url: 'https://journals.sagepub.com/doi/abs/10.1177/0363546515574057',
    published: '2015',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'In a trial that randomised 648 amateur male Dutch soccer players and followed them for a season, adding a Nordic hamstring programme reduced hamstring injury incidence, while injury severity among those injured did not differ.',
    productDecision:
      'The Nordic hamstring curl stays at the prescribed 2 sets of 4 to 6. Its difficulty never progresses automatically, and the exercise page gives partner or anchor setup cues and an assisted option.',
    uncertainty:
      'The trial population was adult amateur soccer players, not adolescent volleyball players. The exact analysed sample size and effect size were not confirmed because only snippets were available.',
    access: 'search-snippet',
  },
  {
    id: 'nordic-van-dyk-2019',
    title: 'Including the Nordic hamstring exercise in injury prevention programmes halves the rate of hamstring injuries: a systematic review and meta-analysis of 8459 athletes',
    publisher: 'British Journal of Sports Medicine 53:1362-1370 (van Dyk, Behan, Whiteley)',
    url: 'https://www.researchgate.net/publication/331367089_Including_the_Nordic_hamstring_exercise_in_injury_prevention_programmes_halves_the_rate_of_hamstring_injuries_A_systematic_review_and_meta-analysis_of_8459_athletes',
    published: '2019',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Pooling 15 studies across sports, programmes that included the Nordic hamstring exercise had roughly half the hamstring injury risk of controls (risk ratio about 0.49).',
    productDecision:
      'Supports keeping the Nordic curl in the plan, described as hamstring strengthening rather than a guarantee against injury.',
    uncertainty:
      'A 2021 reappraisal (see nordic-reappraisal-2021) argued the pooled effect is less certain than the title suggests. URL points to a ResearchGate listing seen in search results, not the BJSM page.',
    access: 'search-snippet',
  },
  {
    id: 'nordic-reappraisal-2021',
    title: 'Why methods matter in a meta-analysis: a reappraisal showed inconclusive injury preventive effect of Nordic hamstring exercise',
    publisher: 'Journal of Clinical Epidemiology 140:111-124 (Impellizzeri, McCall, van Smeden)',
    url: 'https://www.sciencedirect.com/science/article/abs/pii/S0895435621002870',
    published: '2021',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Re-analysing earlier meta-analyses with more conservative methods and prediction intervals, the authors judged the injury preventive effect of the Nordic hamstring exercise inconclusive, citing possible publication bias and little evidence outside soccer.',
    productDecision:
      'App copy describes the Nordic curl as eccentric hamstring strengthening and does not quote an injury reduction percentage.',
    uncertainty:
      'The original authors published a response disputing parts of the reappraisal. Neither paper was opened.',
    access: 'search-snippet',
  },
  {
    id: 'refalo-2023-proximity-to-failure',
    title: 'Influence of Resistance Training Proximity-to-Failure on Skeletal Muscle Hypertrophy: A Systematic Review with Meta-analysis',
    publisher: 'Sports Medicine 53(3):649-665 (Refalo, Helms, Trexler, Hamilton, Fyfe)',
    url: 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9935748/',
    published: 'March 2023',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Training to set failure showed only a trivial hypertrophy advantage over stopping short of failure (effect size about 0.19, confidence interval touching zero), so failure is not required for muscle growth.',
    productDecision:
      'PeakForm prescribes sets by reps in reserve (2 to 3 in the seeded plan), never prescribes routine failure, and blocks plan edits or imported recommendations below 1 RIR.',
    uncertainty:
      'Participants were adults. RIR estimates are known to be imprecise, especially in novices, which is why the app also logs form and pain.',
    access: 'search-snippet',
  },
  {
    id: 'grgic-2022-failure',
    title: 'Effects of resistance training performed to repetition failure or non-failure on muscular strength and hypertrophy: A systematic review and meta-analysis',
    publisher: 'Journal of Sport and Health Science 11(2):202-211 (Grgic and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/33497853/',
    published: '2022',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Across 15 studies in young adults, training to failure did not produce significantly more strength or hypertrophy than non-failure training, and non-failure training favoured strength when volume was not equated.',
    productDecision:
      'Reinforces ending sets with reps in reserve. Progression holds or reduces load when logged RIR falls below the prescription.',
    uncertainty: 'Adult participants only. Full text was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'plotkin-2022-rep-progression',
    title: 'Progressive overload without progressing load? The effects of load or repetition progression on muscular adaptations',
    publisher: 'PeerJ (Plotkin and colleagues), DOI 10.7717/peerj.14142',
    url: 'https://peerj.com/articles/14142/',
    published: '2022',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'In 43 trained adults over 8 weeks, progressing repetitions at a fixed load and progressing load in a fixed rep range both produced similar muscle growth, with load progression slightly better for maximal strength.',
    productDecision:
      'Supports adding reps before weight, which matters when the smallest available plate or stack step is large relative to the load.',
    uncertainty: 'Adult, trained, lower body only, short study. Full text was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'double-progression-convention',
    title: 'Double progression (coaching convention, glossary definition)',
    publisher: 'Alpha Progression glossary (commercial training app)',
    url: 'https://alphaprogression.com/en/glossary/double-progression',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'youth-training',
    conclusion:
      'Double progression means working up to the top of a rep range at a fixed load, then increasing load and returning toward the bottom of the range. It is a widely used coaching rule of thumb, not a protocol that has been tested as such in trials.',
    productDecision:
      'PeakForm uses double progression as its default rule and describes it as a coaching convention, not a studied protocol.',
    uncertainty:
      'Source is a commercial glossary used only to define the term. No study was found that tests double progression itself in adolescents.',
    access: 'search-snippet',
  },

  // ---------- Nutrition and energy availability ----------
  {
    id: 'aap-healthy-weight-control-2017',
    title: 'Promotion of Healthy Weight-Control Practices in Young Athletes (clinical report)',
    publisher: 'American Academy of Pediatrics, Pediatrics 140(3):e20171871 (Carl, Johnson, Martin; Council on Sports Medicine and Fitness)',
    url: 'https://publications.aap.org/pediatrics/article/140/3/e20171871/38384/Promotion-of-Healthy-Weight-Control-Practices-in',
    published: 'September 2017',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'The AAP advises that when weight change is appropriate for a young athlete it should be gradual and supervised, and it discourages rapid weight change methods such as restriction, dehydration, and weight cycling.',
    productDecision:
      'No weight targets, no weigh in streaks, and no praise for weight loss. Calorie targets are ranges to review with a parent, never below 2,000 kcal, and they only change through the fourteen day gate with confirmation.',
    uncertainty:
      'The 1 to 2 lb per week ceiling appears on AAP parent material (see healthychildren-safe-weight-loss). Whether that exact phrasing is in this clinical report could not be confirmed.',
    access: 'search-snippet',
  },
  {
    id: 'healthychildren-safe-weight-loss',
    title: 'Safe Weight Loss and Weight Gain for Young Athletes',
    publisher: 'HealthyChildren.org (American Academy of Pediatrics parent site)',
    url: 'https://www.healthychildren.org/English/healthy-living/sports/Pages/Safe-Weight-Loss-and-Weight-Gain-for-Young-Athletes.aspx',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'Young athletes who lose weight should not lose more than about 1 to 2 pounds per week, because faster loss is often muscle or water. Weight cycling should be avoided and large changes discussed with a doctor first.',
    productDecision:
      'If the seven day average falls faster than about 0.7 kg a week after the first week, PeakForm suggests adding 150 to 200 calories and talking with a parent. That threshold sits inside the 1 to 2 lb a week guidance.',
    uncertainty: 'Page date not visible. Content seen only as a search snippet.',
    access: 'search-snippet',
  },
  {
    id: 'aap-nutrition-supplement-use',
    title: 'Nutrition and Supplement Use (Care of the Young Athlete patient education)',
    publisher: 'American Academy of Pediatrics, Pediatric Patient Education (peo_document566)',
    url: 'https://publications.aap.org/patiented/article-pdf/720898/peo_document566_en.pdf',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'Nutrition needs of young athletes are best met with balanced meals rather than supplements. The handout advises steady hydration without waiting for thirst, a carbohydrate rich meal 3 to 4 hours before exercise and a smaller carbohydrate snack about 1 hour before, and warns that supplements have quality and contamination problems.',
    productDecision:
      'Meal templates are food first with a carbohydrate pre training meal. Supplements are a tracker only, and creatine logging needs a one time parent and clinician confirmation.',
    uncertainty: 'Handout date and edition unknown. Read only through search snippets of the AAP page and a hosted copy.',
    access: 'search-snippet',
  },
  {
    id: 'ioc-reds-2023',
    title: "2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs)",
    publisher: 'British Journal of Sports Medicine 57(17):1073-1097 (Mountjoy, Ackerman, Burke, Stellingwerff and others)',
    url: 'https://bjsm.bmj.com/content/57/17/1073.long',
    published: 'September 2023',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'REDs is a syndrome of health and performance harms in male and female athletes caused by low energy availability, which ranges from adaptable to problematic. The statement updates its conceptual models and adds a physiological model of individual risk factors.',
    productDecision:
      'PeakForm treats underfuelling as a safety issue. It flags fast weight loss, fully logged days under 2,000 kcal, falling energy, mood, or concentration, repeated illness, and recorded red flags, and responds by pausing progression and asking to involve a parent and clinician, never with a diagnosis.',
    uncertainty: 'The page was blocked. Specific screening tools and cut offs in the statement were not reviewed.',
    access: 'search-snippet',
  },
  {
    id: 'nasem-carbohydrate-dri',
    title: 'Dietary Reference Intakes for Water, Potassium, Sodium, Chloride, and Sulfate, chapter 25 (National Academies reader page)',
    publisher: 'Institute of Medicine, National Academies Press (DOI 10.17226/10925)',
    url: 'https://www.nationalacademies.org/read/10925/chapter/25',
    published: '2005',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'The carbohydrate RDA is 130 g per day for males aged 14 to 18 (the same value applies from age 1 through adulthood), based on the glucose needs of the brain. Search results from National Academies DRI summary material confirmed the 130 g figure.',
    productDecision:
      'Carbohydrate targets can never be saved below 130 g a day. The seeded targets are 190 to 285 g because training needs more.',
    uncertainty:
      'This URL belongs to the water and electrolytes DRI volume. Chapter 25 could not be opened, so it is not confirmed whether it is a summary table, an index, or other back matter. The primary source for the carbohydrate RDA is the macronutrient DRI report (NAP 10490).',
    access: 'search-snippet',
  },
  {
    id: 'hall-2015-fat-vs-carb-restriction',
    title: 'Calorie for Calorie, Dietary Fat Restriction Results in More Body Fat Loss than Carbohydrate Restriction in People with Obesity',
    publisher: 'Cell Metabolism (Hall and colleagues, NIH)',
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4603544/',
    published: 'August 2015',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'In a metabolic ward, 19 adults with obesity each spent 6 days on equal calorie cuts from fat or from carbohydrate. Cutting carbohydrate increased fat oxidation, but cutting fat produced slightly more body fat loss, so lower carbohydrate intake was not metabolically superior under tight control.',
    productDecision:
      'PeakForm does not promote low carbohydrate eating for fat loss, explains that insulin rising after meals is normal, and keeps measured carbohydrate around training.',
    uncertainty: 'Adults with obesity, very short duration, not athletes or adolescents. Details come from snippets and press summaries.',
    access: 'search-snippet',
  },
  {
    id: 'adolescent-protein-review-2025',
    title: 'Optimizing Performance Nutrition for Adolescent Athletes: A Review of Dietary Needs, Risks, and Practical Strategies',
    publisher: 'Nutrients 17(17):2792 (MDPI)',
    url: 'https://www.mdpi.com/2072-6643/17/17/2792',
    published: '2025',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'Sports nutrition literature suggests adolescent athletes need more protein than the general guideline of about 0.75 to 1.05 g/kg, commonly cited as 1.2 to 2.0 g/kg, with about 1.5 g/kg often mentioned as enough to stay in positive nitrogen balance during growth. Spreading 20 to 40 g across meals is a common practical suggestion.',
    productDecision:
      'Protein targets are the seeded 150 to 175 g a day from food, with protein powder optional. Depending on body weight that can sit above this review\'s range per kilogram, and the default meals supply about 200 g with standard food values. This is flagged for review with a pediatric sports dietitian.',
    uncertainty:
      'The figures came from a search summary that drew on several results (this review, a Brazilian cross sectional study at PMC9520475, and others). Which paper states the 1.5 g/kg nitrogen balance point was not confirmed.',
    access: 'search-snippet',
  },
  {
    id: 'ods-calcium-consumer',
    title: 'Calcium: Fact Sheet for Consumers',
    publisher: 'NIH Office of Dietary Supplements',
    url: 'https://ods.od.nih.gov/factsheets/Calcium-Consumer/',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'nutrition',
    conclusion:
      'Teens aged 14 to 18 need 1,300 mg of calcium per day, and people aged 9 to 18 should not exceed 3,000 mg per day from food and supplements combined.',
    productDecision:
      'The Eat screen adds calcium from food and supplements against about 1,300 mg a day and shows a note if the total passes 2,500 mg, below the 3,000 mg upper limit.',
    uncertainty: 'Page date not visible. Figures confirmed only through search snippets.',
    access: 'search-snippet',
  },
  {
    id: 'ods-omega3-consumer',
    title: 'Omega-3 Fatty Acids: Fact Sheet for Consumers',
    publisher: 'NIH Office of Dietary Supplements',
    url: 'https://ods.od.nih.gov/factsheets/Omega3FattyAcids-Consumer/',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'supplements',
    conclusion:
      'EPA and DHA come mainly from fish and seafood, and children and teens get very little from typical diets. The FDA suggests no more than 3 g per day of EPA plus DHA combined, with up to 2 g from supplements, and supplement labels should not recommend more than 2 g per day.',
    productDecision:
      'The plan includes fish at three dinners a week. The supplement tracker asks for EPA plus DHA from the label, not the total fish oil amount.',
    uncertainty:
      'The label reading tip (total oil versus EPA plus DHA) came from a non government snippet. No adolescent specific omega-3 dose is set by ODS.',
    access: 'search-snippet',
  },

  // ---------- Body composition measurement ----------
  {
    id: 'smart-scales-accuracy-2021',
    title: 'Accuracy of Smart Scales on Weight and Body Composition: Observational Study',
    publisher: "JMIR mHealth and uHealth (Frija-Masson, Mullaert, Vidal-Petiot, Pons-Kerjean, Flamant, d'Ortho)",
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC8122302/',
    published: 'April 2021',
    reviewedOn: '2026-09-29',
    topic: 'body-composition',
    conclusion:
      'This is not a general review of bioelectrical impedance. It compared three consumer smart scales with DEXA in adult patients and found them accurate for total body weight but not reliable enough to use routinely for body composition, especially in severe obesity.',
    productDecision:
      'Smart scale body fat is optional, labelled trend only, shown only as weekly averages when there are at least three readings, and never used for nutrition decisions.',
    uncertainty:
      'Adults in a clinical setting with specific scale models, so results may not transfer to a lean adolescent or newer devices. Findings seen only as snippets.',
    access: 'search-snippet',
  },

  // ---------- Sleep and recovery ----------
  {
    id: 'aasm-teen-sleep-advisory',
    title: 'Health Advisory: Teen Sleep Duration',
    publisher: 'American Academy of Sleep Medicine',
    url: 'https://aasm.org/wp-content/uploads/2017/10/teen-sleep-duration-health-advisory.pdf',
    published: '2017 (URL path); based on the 2016 AASM pediatric consensus (Paruthi and colleagues)',
    reviewedOn: '2026-09-29',
    topic: 'recovery',
    conclusion:
      'Teens aged 13 to 18 should regularly sleep 8 to 10 hours per 24 hours. Regular short sleep is linked to attention, learning and mood problems, more injuries and accidents, and other health risks.',
    productDecision:
      'The sleep target is 8 to 10 hours. The check in shows duration against it, readiness eases off after short nights, and the weekly review flags averages under eight hours.',
    uncertainty: 'PDF was blocked. The advisory publication date is inferred from the URL path.',
    access: 'search-snippet',
  },
  {
    id: 'sleep-injury-adolescents-2019',
    title: 'Chronic Lack of Sleep is Associated With Increased Sports Injury in Adolescents: A Systematic Review and Meta-analysis',
    publisher: 'Orthopaedic Journal of Sports Medicine (meeting abstract; Gao, Dwivedi, Milewski, Cruz)',
    url: 'https://journals.sagepub.com/doi/10.1177/2325967119S00132',
    published: '2019',
    reviewedOn: '2026-09-29',
    topic: 'recovery',
    conclusion:
      'This meta-analysis abstract links chronic short sleep with higher sports injury rates in adolescents. It builds on earlier work by Milewski and colleagues (2014) reporting that adolescent athletes sleeping under 8 hours were about 1.7 times more likely to be injured.',
    productDecision:
      'Sleep feeds the readiness indicator and the weekly review. PeakForm does not change the plan by itself.',
    uncertainty:
      'Observational association, not proof that more sleep prevents injury. This is a conference abstract, and the 1.7 figure came from a secondary review snippet.',
    access: 'search-snippet',
  },
  {
    id: 'sleep-extension-athletes-review',
    title: 'Sleep extension in athletes: what we know so far - A systematic review',
    publisher: 'Sleep Medicine (listed on ScienceDirect and PubMed 33352457)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/33352457/',
    published: '2020 or 2021 (not confirmed)',
    reviewedOn: '2026-09-29',
    topic: 'recovery',
    conclusion:
      'Limited, lower quality evidence suggests that extending sleep may improve some measures of sports performance, with the size of the benefit depending on the outcome measured.',
    productDecision:
      'Sleep advice is framed as supporting recovery, mood and learning, without promising specific performance gains.',
    uncertainty: 'Journal name inferred from the ScienceDirect article code; publication year not confirmed. Evidence quality is low by the authors own account, and the age mix of included athletes was not checked.',
    access: 'search-snippet',
  },

  // ---------- Supplements ----------
  {
    id: 'issn-creatine-2017',
    title: 'International Society of Sports Nutrition position stand: safety and efficacy of creatine supplementation in exercise, sport, and medicine',
    publisher: 'Journal of the International Society of Sports Nutrition 14:18 (Kreider and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/28615996/',
    published: 'June 2017',
    reviewedOn: '2026-09-29',
    topic: 'supplements',
    conclusion:
      'The ISSN considers creatine monohydrate acceptable for adolescent athletes only with proper precautions and supervision: serious supervised training, a good diet, understanding of correct use, and recommended doses. It reported no evidence of harm at recommended doses in under 18s.',
    productDecision:
      'PeakForm never suggests creatine. If a parent and clinician have reviewed it, the tracker can record the product and dose.',
    uncertainty:
      'ISSN is a sports nutrition society with industry ties, and pediatric bodies such as the AAP are more cautious about supplements in minors.',
    access: 'search-snippet',
  },
  {
    id: 'metzger-2023-creatine-pediatric',
    title: 'Creatine supplementation in the pediatric and adolescent athlete: A literature review',
    publisher: 'Journal of Orthopaedics 38:73-78 (Metzger, Minneci, Gehred, Day, Klingele), DOI 10.1016/j.jor.2023.03.010',
    url: 'https://pubmed.ncbi.nlm.nih.gov/37008451/',
    published: '2023',
    reviewedOn: '2026-09-29',
    topic: 'supplements',
    conclusion:
      'The authors found the pediatric creatine literature to be of poor overall quality, with no consistent performance findings and no studies designed to assess safety, and advised clinicians to explain these gaps to young athletes and families.',
    productDecision:
      'Together with the ISSN stand, this is why creatine logging stays locked until a one time parent and clinician confirmation.',
    uncertainty:
      'PMID 37008451 was matched to this title by a search summary and the same title appeared on ScienceDirect, Nemours and jortho.org listings, so the match is likely but the PubMed page itself was not opened.',
    access: 'search-snippet',
  },

  // ---------- Food safety ----------
  {
    id: 'fsis-leftovers',
    title: 'Leftovers and Food Safety',
    publisher: 'USDA Food Safety and Inspection Service',
    url: 'https://www.fsis.usda.gov/food-safety/safe-food-handling-and-preparation/food-safety-basics/leftovers-and-food-safety',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'food-safety',
    conclusion:
      'Refrigerate cooked food within 2 hours (1 hour above 90 F) in shallow containers at 40 F (4 C) or below, use most leftovers within 3 to 4 days, and reheat to 165 F (74 C) or until hot and steaming. Frozen food at 0 F stays safe indefinitely, with storage times given for quality only.',
    productDecision:
      'Meal preparation labels containers by day and meal, lists the two hour rule, the 4 °C fridge, the three to four day limit, and reheating to 74 °C.',
    uncertainty: 'Page could not be opened. The 1 hour above 90 F rule and freezer note came from FSIS snippets on related pages.',
    access: 'search-snippet',
  },
  {
    id: 'foodsafety-gov-min-temps',
    title: 'Safe Minimum Internal Temperatures',
    publisher: 'FoodSafety.gov (US Department of Health and Human Services)',
    url: 'https://www.foodsafety.gov/food-safety-charts/safe-minimum-internal-temperatures',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'food-safety',
    conclusion:
      'Cook poultry to 165 F (74 C), fish to 145 F (63 C), ground beef to 160 F (71 C), and beef steaks and roasts to 145 F (63 C) with a 3 minute rest, checked with a food thermometer.',
    productDecision:
      'Recipes with meat, poultry, or fish state the minimum internal temperature in °C, and the preparation screen lists 74, 63, and 71 °C.',
    uncertainty: 'Page could not be opened; values match snippets from FoodSafety.gov, FSIS and FDA charts.',
    access: 'search-snippet',
  },

  // ---------- iPhone and PWA behaviour ----------
  {
    id: 'webkit-web-push-ios-16-4',
    title: 'Web Push for Web Apps on iOS and iPadOS',
    publisher: 'WebKit blog (Brady Eidson, Jen Simmons)',
    url: 'https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/',
    published: 'February 16, 2023',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'iOS and iPadOS 16.4 added Web Push and the Badging API for web apps added to the Home Screen only, not for pages in a Safari tab. Permission can only be requested in response to a direct user action such as tapping a button.',
    productDecision:
      'PeakForm does not use Web Push, because it needs a push server. Reminders come from the in app timeline and an Apple Calendar export with alarms.',
    uncertainty: 'Blocked page; details from snippets and secondary sources. PeakForm is offline first and would need a push server to send pushes, which conflicts with its private design, so local reminders may be preferable.',
    access: 'search-snippet',
  },
  {
    id: 'apple-web-push-docs',
    title: 'Sending web push notifications in web apps and browsers',
    publisher: 'Apple Developer Documentation',
    url: 'https://developer.apple.com/documentation/usernotifications/sending-web-push-notifications-in-web-apps-and-browsers',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Apple documents standards based Web Push (Push API, Notifications API, service workers). For iOS Home Screen web apps the manifest display member must be standalone or fullscreen and permission must follow a user gesture.',
    productDecision:
      'The manifest uses display standalone. Push is not used.',
    uncertainty: 'Manifest requirement came from a third party summary of Apple guidance; the Apple page was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'webkit-safari-18-4',
    title: 'WebKit Features in Safari 18.4',
    publisher: 'WebKit blog',
    url: 'https://webkit.org/blog/16574/webkit-features-in-safari-18-4/',
    published: '2025',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Safari 18.4 made the Screen Wake Lock API work in Home Screen web apps on iOS and iPadOS 18.4, fixing a gap since 16.4 where it only worked in Safari tabs (WebKit bug 254545). It also added Declarative Web Push for Home Screen web apps, which does not need a service worker to show notifications.',
    productDecision:
      'During workouts PeakForm requests a screen wake lock when the browser supports it and releases it afterwards. Where it is unsupported, nothing breaks.',
    uncertainty: 'Release note seen as snippets. Wake lock is still released when the app goes to the background or the phone locks.',
    access: 'search-snippet',
  },
  {
    id: 'caniuse-wake-lock',
    title: 'Screen Wake Lock API support table',
    publisher: 'Can I use',
    url: 'https://caniuse.com/wake-lock',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Safari on iOS supports Screen Wake Lock from 16.4, recorded as partial from 16.4 until 18.4 because it did not work in standalone Home Screen web apps. All iOS browsers use WebKit, so the same limits apply to them.',
    productDecision:
      'Wake lock is feature detected. The rest timer uses an absolute end time, so it stays correct after the screen locks, but sounds only play while PeakForm is open.',
    uncertainty: 'Snippet level only; current version ranges may have changed.',
    access: 'search-snippet',
  },
  {
    id: 'vibration-api-ios',
    title: 'Navigator API: vibrate support table',
    publisher: 'Can I use (MDN browser compat data)',
    url: 'https://caniuse.com/mdn-api_navigator_vibrate',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Compatibility data lists navigator.vibrate as unsupported in Safari on iOS, and WebKit has not announced support. A March 2026 issue on MDN browser-compat-data (#29166) reported that it works on current iOS Safari, which conflicts with other 2026 reports that it silently does nothing.',
    productDecision:
      'PeakForm does not rely on vibration. The timer end shows a clear visual state and plays a sound while the app is open. The vibrate call is a harmless extra that does nothing on iPhone.',
    uncertainty:
      'Real support status on current iOS is disputed. It should be tested on the actual iPhone before any vibration feature is described to the user.',
    access: 'search-snippet',
  },
  {
    id: 'webkit-safari-18-switch-haptics',
    title: 'WebKit Features in Safari 18.0',
    publisher: 'WebKit blog',
    url: 'https://webkit.org/blog/15865/webkit-features-in-safari-18-0/',
    published: '2024',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Safari on iOS 18 gives haptic feedback when a user toggles an input type checkbox with the switch attribute, the only official web haptic on iPhone found in this review.',
    productDecision:
      'PeakForm does not use hidden switch tricks to fake vibration.',
    uncertainty: 'Details from snippets. Third party libraries exploit this for arbitrary haptics, which may break in future iOS versions.',
    access: 'search-snippet',
  },
  {
    id: 'webkit-storage-policy-2023',
    title: 'Updates to Storage Policy',
    publisher: 'WebKit blog (Sihui Liu)',
    url: 'https://webkit.org/blog/14403/updates-to-storage-policy/',
    published: 'August 10, 2023',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'From Safari 17 and iOS 17, storage quotas are based on disk size (up to 80 percent of disk overall for browser apps, up to 20 percent for other apps), and WebKit evicts data by origin when total usage exceeds the overall quota. An origin in persistent mode, requested with navigator.storage.persist(), is exempt from that eviction.',
    productDecision:
      'PeakForm asks for persistent storage when setup finishes, shows the result in More, Backup, keeps data small, and shows the last backup date on Today.',
    uncertainty: 'Blocked page. How Safari decides whether to grant persist() on iOS, and whether a Home Screen app counts as a browser app for quota, were not confirmed.',
    access: 'search-snippet',
  },
  {
    id: 'webkit-itp-7-day-cap-2020',
    title: 'Full Third-Party Cookie Blocking and More',
    publisher: 'WebKit blog (John Wilander)',
    url: 'https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/',
    published: 'March 24, 2020',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Since iOS 13.4 and Safari 13.1, Intelligent Tracking Prevention deletes all script writable storage (IndexedDB, localStorage, service worker registrations and more) after 7 days of Safari use without user interaction on the site. Home Screen web apps are not part of Safari and keep their own day counter that resets when the app is used.',
    productDecision:
      'The install guide puts Add to Home Screen first, the backup screen explains that data in a plain Safari tab can be cleared after about a week without a visit, and Today shows the last backup date.',
    uncertainty: 'Snippets only. Apple has not documented every edge case, for example a Home Screen app that is not opened for a long time.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-storage-persist',
    title: 'StorageManager: persist() method',
    publisher: 'MDN Web Docs',
    url: 'https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'persist() asks the browser to mark the origin storage as persistent and resolves to true only if granted. By default origins are best effort and can be evicted; persistent data can only be removed by the user. Snippets indicate Safari 17 supports the Storage API including persist().',
    productDecision:
      'Persistence is requested once at setup and on demand, the result is shown, and it is never assumed.',
    uncertainty: 'Blocked page. Support version for Safari came from a WebKit snippet rather than MDN compat tables.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-navigator-share',
    title: 'Navigator: share() method',
    publisher: 'MDN Web Docs',
    url: 'https://developer.mozilla.org/en-US/docs/Web/API/Navigator/share',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'The Web Share API opens the system share sheet. Safari 15 on iOS added level 2 support, which allows sharing files; navigator.canShare can check whether given files are shareable, while share() itself needs a user gesture.',
    productDecision:
      'Exports use navigator.share with files when canShare confirms support, straight from a tap, and fall back to a download otherwise.',
    uncertainty: 'The iOS 15 file sharing detail came from developer blog snippets; some bug reports mention inconsistencies on specific 15.x versions.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-share-data-between-apps',
    title: 'Share data between apps',
    publisher: 'MDN Web Docs (Progressive web apps how to)',
    url: 'https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/How_to/Share_data_between_apps',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'PWAs can share out with the Web Share API and can receive shared content through the share_target manifest member, which requires the PWA to be installed and uses a POST with multipart form data for files.',
    productDecision:
      'PeakForm only shares out. It does not use share_target.',
    uncertainty: 'The statement that share_target does not work on iOS is prior knowledge and was not confirmed in this review.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-pwa-reference',
    title: 'Progressive Web Apps reference',
    publisher: 'MDN Web Docs',
    url: 'https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Reference',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'MDN lists the manifest members (such as name, short_name, scope, shortcuts) and service worker APIs (Cache, Clients, fetch event) that PWAs use for installation and offline behaviour.',
    productDecision:
      'PeakForm precaches the app with a service worker for offline use and ships a manifest with name, short_name, icons, start_url, scope, and display standalone.',
    uncertainty: 'Reference index only; per feature Safari support must be checked separately.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-making-pwas-installable',
    title: 'Making PWAs installable',
    publisher: 'MDN Web Docs',
    url: 'https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Guides/Making_PWAs_installable',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Install prompts use the manifest name and icons, and start_url and display control launch. Chromium requires HTTPS, a service worker and key manifest fields for its prompt, while Safari on iOS installs through the Add to Home Screen option in the share menu.',
    productDecision:
      'The app includes a short Add to Home Screen guide, because iOS has no automatic install prompt.',
    uncertainty: 'Snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'mdn-barcode-detection',
    title: 'Barcode Detection API',
    publisher: 'MDN Web Docs',
    url: 'https://developer.mozilla.org/en-US/docs/Web/API/Barcode_Detection_API',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'BarcodeDetector is not implemented in Safari or any iOS browser. It existed only behind an experimental flag in Safari 17 and reports say that flag broke with iOS 18.',
    productDecision:
      'Barcode lookup uses a typed barcode number with an optional Open Food Facts query. There is no camera scanning, because Safari has no BarcodeDetector. Manual label entry is always available.',
    uncertainty: 'Status from snippets and an Apple developer forum thread title; not tested on device.',
    access: 'search-snippet',
  },
  {
    id: 'apple-eu-home-screen-reversal-2024',
    title: 'Apple reverses decision about blocking web apps on iPhones in the EU',
    publisher: 'TechCrunch',
    url: 'https://techcrunch.com/2024/03/01/apple-reverses-decision-about-blocking-web-apps-on-iphones-in-the-eu/',
    published: 'March 1, 2024',
    reviewedOn: '2026-09-29',
    topic: 'platform',
    conclusion:
      'Apple planned to remove Home Screen web apps in the EU in iOS 17.4 betas, then reversed that and kept the existing capability, so installed web apps in the EU continued to work as before.',
    productDecision:
      'No region specific code. Installation should be checked on the actual phone.',
    uncertainty: 'Some 2026 third party guides still claim push does not work in the EU; that was not verified and may be outdated.',
    access: 'search-snippet',
  },

  // ---------- Hosting ----------
  {
    id: 'github-pages-what-is',
    title: 'What is GitHub Pages?',
    publisher: 'GitHub Docs',
    url: 'https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      'GitHub Pages is available for public repositories on GitHub Free, and for private repositories only on paid plans (Pro, Team, Enterprise). Sites on github.io are served over HTTPS automatically.',
    productDecision:
      'Not used for PeakForm. A GitHub Pages site on the free plan can be opened by anyone with the address, and the user wants nobody else to be able to open or install the app.',
    uncertainty: 'Snippet level; plan terms change.',
    access: 'search-snippet',
  },
  {
    id: 'github-pages-limits',
    title: 'GitHub Pages limits',
    publisher: 'GitHub Docs',
    url: 'https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      'Published sites may be no larger than 1 GB, have a soft bandwidth limit of 100 GB per month, and a soft limit of 10 builds per hour that does not apply when publishing with a custom GitHub Actions workflow.',
    productDecision:
      'Not relevant now that PeakForm is published on Cloudflare Pages.',
    uncertainty: 'Snippet level.',
    access: 'search-snippet',
  },
  {
    id: 'cloudflare-pages-limits',
    title: 'Cloudflare Pages limits',
    publisher: 'Cloudflare Docs',
    url: 'https://developers.cloudflare.com/pages/platform/limits/',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      'The free plan allows 500 builds per month and 20,000 files per site, with a 25 MiB limit per file, and snippets describe bandwidth as unlimited. A January 2026 changelog raised the file limit for paid plans only.',
    productDecision:
      'PeakForm is published on a Cloudflare Pages project owned by the user and built from this repository. It uses a tiny fraction of these limits.',
    uncertainty:
      'Private repository support and the note that Cloudflare now steers new projects toward Workers static assets are from prior knowledge, not confirmed here. Unlimited bandwidth came from third party snippets.',
    access: 'search-snippet',
  },
  {
    id: 'cloudflare-pages-middleware',
    title: 'Middleware',
    publisher: 'Cloudflare Pages Docs',
    url: 'https://developers.cloudflare.com/pages/functions/middleware/',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      'A functions/_middleware file that exports onRequest runs before every request to the project, including static files. The functions folder sits at the project root or the configured root directory, not in the build output.',
    productDecision:
      'functions/_middleware.ts runs the password gate in front of every file, so no part of the app is served without the password.',
    uncertainty: 'Snippet level; the page itself was blocked. The behaviour was checked locally with Wrangler 4.143 in the Cloudflare runtime.',
    access: 'search-snippet',
  },
  {
    id: 'cloudflare-secrets',
    title: 'Secrets',
    publisher: 'Cloudflare Workers Docs',
    url: 'https://developers.cloudflare.com/workers/configuration/secrets/',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      "A Pages project's Settings, Variables and Secrets, Add, with Encrypt selected, stores a value that cannot be viewed again and is available to Functions on context.env. It has to be set before the deployment that uses it.",
    productDecision:
      'The site password is the encrypted PEAKFORM_PASSWORD variable, never in the repository. Without it, the gate serves nothing.',
    uncertainty: 'Snippet level; dashboard labels change over time.',
    access: 'search-snippet',
  },
  {
    id: 'cloudflare-build-image',
    title: 'Build image',
    publisher: 'Cloudflare Pages Docs',
    url: 'https://developers.cloudflare.com/pages/configuration/build-image/',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion: 'The Node.js version for a build can be set with a NODE_VERSION environment variable or a .node-version or .nvmrc file in the project.',
    productDecision: 'peakform/.node-version pins Node 22, which Vite 8 needs.',
    uncertainty: 'Snippet level.',
    access: 'search-snippet',
  },
  {
    id: 'netlify-credit-plans',
    title: 'How credits work (credit-based pricing plans)',
    publisher: 'Netlify Docs',
    url: 'https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/',
    published: 'Credit plans for new accounts from September 4, 2025; rates updated April 14, 2026',
    reviewedOn: '2026-09-29',
    topic: 'hosting',
    conclusion:
      'New Netlify accounts use credit based plans. The Free plan gives 300 credits per month, a production deploy costs 15 credits, bandwidth is metered in credits per GB, and sites pause until the next month when free credits run out.',
    productDecision:
      'Not used. A paused site would block installing or updating the app.',
    uncertainty:
      'Snippets disagreed on bandwidth cost (10 or 20 credits per GB); Netlify docs snippets said 20, and an April 2026 changelog updated rates without the new figure being visible.',
    access: 'search-snippet',
  },

  // ---------- Media and food data ----------
  {
    id: 'youtube-player-parameters',
    title: 'YouTube Embedded Players and Player Parameters',
    publisher: 'Google for Developers (YouTube IFrame Player API)',
    url: 'https://developers.google.com/youtube/player_parameters',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'media',
    conclusion:
      'Since September 25, 2018, rel=0 no longer hides related videos; it limits them to the same channel. The showinfo parameter was deprecated, so title and channel always show. Parameters such as start, end, playsinline and cc_load_policy remain available.',
    productDecision:
      'Videos load only after a tap, never autoplay, and use rel=0 and playsinline=1. PeakForm never downloads or rehosts video.',
    uncertainty: 'The playsinline and cc_load_policy details are prior knowledge; the page itself was blocked.',
    access: 'search-snippet',
  },
  {
    id: 'youtube-privacy-enhanced-mode',
    title: 'Embed videos and playlists (privacy-enhanced mode)',
    publisher: 'YouTube Help',
    url: 'https://support.google.com/youtube/answer/171780',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'media',
    conclusion:
      'Privacy-enhanced mode uses the youtube-nocookie.com domain so that views do not personalise the viewer experience on YouTube and ads are non personalised. Independent 2026 tests reported that no cookies are set on load, but the player still writes local storage and contacts Google before playback and sets cookies after play.',
    productDecision:
      'Embeds use youtube-nocookie.com and load only after a tap on a placeholder, with a note that YouTube may set cookies once playing.',
    uncertainty: 'The storage and telemetry behaviour came from third party blog snippets, not from Google.',
    access: 'search-snippet',
  },
  {
    id: 'open-food-facts-api',
    title: 'Introduction to Open Food Facts API documentation',
    publisher: 'Open Food Facts (Product Opener server docs)',
    url: 'https://openfoodfacts.github.io/openfoodfacts-server/api/',
    published: 'Continuously updated',
    reviewedOn: '2026-09-29',
    topic: 'media',
    conclusion:
      'Reads need no API key. Product lookup is GET https://world.openfoodfacts.org/api/v2/product/{barcode}.json, clients should send a descriptive User-Agent naming the app, and there are per IP rate limits with possible IP bans when exceeded.',
    productDecision:
      'Lookups are optional, one barcode at a time after a tap, and only the barcode number is sent. Browsers cannot set a custom User-Agent, so none is sent. Results are labelled as community data to check against the label.',
    uncertainty:
      'The brief expected 100 requests per minute for product reads, but search snippets quoting the official docs said 15 per minute per IP for product reads and 10 per minute for search; a 100 per minute figure appeared only in a third party project. The live docs must be checked before relying on either number.',
    access: 'search-snippet',
  },
  {
    id: 'open-food-facts-license',
    title: 'Terms of use, contribution and re-use',
    publisher: 'Open Food Facts',
    url: 'https://world.openfoodfacts.org/terms-of-use',
    published: 'Not stated in search result',
    reviewedOn: '2026-09-29',
    topic: 'media',
    conclusion:
      'The database is licensed under the Open Database License (ODbL), individual contents under the Database Contents License, and product images under CC BY-SA. Reuse requires attribution and share alike for adapted databases.',
    productDecision:
      'Food data from a lookup is labelled as coming from Open Food Facts under the ODbL, and no product images are used.',
    uncertainty: 'Snippets only; the implications of ODbL share alike for a private single user cache are low but not reviewed by a lawyer.',
    access: 'search-snippet',
  },
];
