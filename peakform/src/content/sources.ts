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
      'Since 3.0.0 the gym week has four strength sessions, upper and lower body in turn, instead of six. Youth guidance describes two to three sessions a week and no added benefit beyond about four, and the days off leave room for school sport. PeakForm asks for qualified supervision on new exercises, never tests a one rep maximum, and adds reps before load.',
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
      'Since 3.0.0 work sets stop about two reps short of failure. The extra growth from sets taken all the way to failure was trivial in this analysis, while fatigue and recovery time rise, and youth guidance does not prescribe routine failure.',
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
      'Supports the 3.0.0 default of two reps in reserve: no significant difference in growth or strength between failure and non failure training.',
    uncertainty: 'Adult participants only. Full text was not opened.',
    access: 'search-snippet',
  },
  {
    id: 'robinson-2024-proximity-dose-response',
    title: 'Exploring the Dose-Response Relationship Between Estimated Resistance Training Proximity to Failure, Strength Gain, and Muscle Hypertrophy: A Series of Meta-Regressions',
    publisher: 'Sports Medicine 54:2209-2231 (Robinson and colleagues)',
    url: 'https://doi.org/10.1007/s40279-024-02069-2',
    published: '2024',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Muscle growth rose modestly as sets ended closer to failure, while strength barely depended on it.',
    productDecision:
      'Growth rises a little closer to failure, so sets stop about two reps short rather than far from it. Strength barely depends on it. Routine failure is not prescribed for an adolescent (3.0.0).',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text. Proximity was estimated, not measured.',
    access: 'search-snippet',
  },
  {
    id: 'refalo-2024-failure-vs-rir',
    title: 'Similar muscle hypertrophy following eight weeks of resistance training to momentary muscular failure or with repetitions-in-reserve in resistance-trained individuals',
    publisher: 'Journal of Sports Sciences (Refalo and colleagues)',
    url: 'https://doi.org/10.1080/02640414.2024.2321021',
    published: '2024',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Training to momentary failure and stopping one to two reps short produced the same quadriceps growth, about 7 percent in both.',
    productDecision:
      'Same growth with one or two reps in reserve as with failure, so PeakForm keeps two in reserve (3.0.0).',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'hermann-2025-single-set-failure',
    title: 'Without Fail: Muscular Adaptations in Single-Set Resistance Training Performed to Failure or with Repetitions-in-Reserve',
    publisher: 'Medicine and Science in Sports and Exercise 57(9):2021-2031 (Hermann and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/40249908/',
    published: '2025',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'With a single set per exercise, going to failure modestly beat stopping two reps short on some growth measures.',
    productDecision:
      'A small advantage for failure on some measures with single sets; PeakForm uses two or three sets per exercise at two reps in reserve instead, which this study does not cover.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text. Low volume design, so the effect may be smaller with three sets.',
    access: 'search-snippet',
  },
  {
    id: 'halperin-2022-rir-accuracy',
    title: 'Accuracy in Predicting Repetitions to Task Failure in Resistance Exercise: A Scoping Review and Exploratory Meta-analysis',
    publisher: 'Sports Medicine (Halperin and colleagues)',
    url: 'https://doi.org/10.1007/s40279-021-01559-x',
    published: '2022',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'People tend to underestimate how many reps they have left by about one rep, most of all at high rep counts.',
    productDecision:
      'Occasional sets to technical failure on safe exercises help calibrate reps in reserve. New exercises stay two reps short for two sessions.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'pelland-2025-volume-frequency',
    title: 'The Resistance Training Dose Response: Meta-Regressions Exploring the Effects of Weekly Volume and Frequency on Muscle Hypertrophy and Strength Gains',
    publisher: 'Sports Medicine (Pelland and colleagues)',
    url: 'https://doi.org/10.1007/s40279-025-02344-w',
    published: '2025',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Growth rose with weekly sets with diminishing returns, and frequency added little once weekly volume was equal.',
    productDecision:
      'With weekly sets equal, more training days added little or no growth, so the 3.0.0 week trains each muscle twice in four gym days instead of spreading the same work over six. Weekly direct sets land at about 4 to 12 per muscle, plus indirect work. These are adult data.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'nunes-2021-exercise-order',
    title: 'What influence does resistance exercise order have on muscular strength gains and muscle hypertrophy? A systematic review and meta-analysis',
    publisher: 'European Journal of Sport Science 21:149-157 (Nunes and colleagues)',
    url: 'https://doi.org/10.1080/17461391.2020.1733672',
    published: '2021',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Hypertrophy was similar whether multi joint or single joint exercises came first.',
    productDecision:
      'Big and demanding exercises come first in each session, for technique and safety, not because order changes growth.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'singer-2024-rest-intervals',
    title: 'Give it a rest: a systematic review with Bayesian meta-analysis on the effect of inter-set rest interval duration on muscle hypertrophy',
    publisher: 'Frontiers in Sports and Active Living (Singer and colleagues)',
    url: 'https://doi.org/10.3389/fspor.2024.1429789',
    published: '2024',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Resting longer than about 60 seconds gave a small growth benefit, with no clear further benefit past about 90 seconds.',
    productDecision:
      'Rest is 150 to 180 seconds on big exercises and 75 to 90 seconds on small ones.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text. Few studies.',
    access: 'search-snippet',
  },
  {
    id: 'haugen-2023-free-weights-machines',
    title: 'Effect of free-weight vs. machine-based strength training on maximal strength, hypertrophy and jump performance: a systematic review and meta-analysis',
    publisher: 'BMC Sports Science, Medicine and Rehabilitation (Haugen and colleagues)',
    url: 'https://doi.org/10.1186/s13102-023-00713-4',
    published: '2023',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Free weights and machines produced similar muscle growth.',
    productDecision:
      'The program uses machines, cables, the Smith machine, and dumbbells only, because the athlete trains alone, with no expected loss of growth.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'kerr-2010-weight-training-injuries',
    title: 'Epidemiology of weight training-related injuries presenting to United States emergency departments, 1990 to 2007',
    publisher: 'American Journal of Sports Medicine 38(4):765-771 (Kerr and colleagues)',
    url: 'https://doi.org/10.1177/0363546509351560',
    published: '2010',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Most weight training injuries seen in emergency departments involved free weights, and many came from dropped weights.',
    productDecision:
      'No free barbell when training alone. Smith and plate loaded machines always use their safety stops.',
    uncertainty: 'Emergency department data, not a trial. The percentages came from a summary.',
    access: 'search-snippet',
  },
  {
    id: 'chaves-2020-incline-press',
    title: 'Effects of Horizontal and Incline Bench Press on Neuromuscular Adaptations in Untrained Young Men',
    publisher: 'International Journal of Exercise Science 13(6):859-872 (Chaves and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/32922646/',
    published: '2020',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'The incline press grew the upper chest more than the flat press.',
    productDecision:
      'The upper chest has its own slot with three incline presses at 30 to 45 degrees.',
    uncertainty: 'Untrained young men, a small study.',
    access: 'search-snippet',
  },
  {
    id: 'larsen-2025-lateral-raise',
    title: 'Dumbbell versus cable lateral raises for lateral deltoid hypertrophy: an experimental study',
    publisher: 'Frontiers in Physiology (Larsen and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/40692697/',
    published: '2025',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Cable and dumbbell lateral raises grew the side of the shoulder about equally.',
    productDecision:
      'Cable, dumbbell, and machine lateral raises are offered as equal choices.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'maeo-2021-seated-leg-curl',
    title: 'Greater Hamstrings Muscle Hypertrophy but Similar Damage Protection after Training at Long versus Short Muscle Lengths',
    publisher: 'Medicine and Science in Sports and Exercise 53(4):825-837 (Maeo and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/33009197/',
    published: '2021',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Seated leg curls grew the hamstrings more than lying leg curls, about 14 against 9 percent.',
    productDecision:
      'The knee bend slot uses the seated leg curl only.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'maeo-2023-overhead-triceps',
    title: 'Triceps brachii hypertrophy is substantially greater after elbow extension training performed in the overhead versus neutral arm position',
    publisher: 'European Journal of Sport Science (Maeo and colleagues)',
    url: 'https://doi.org/10.1080/17461391.2022.2100279',
    published: '2023',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Overhead extensions grew the triceps about 1.4 times more than pushdowns.',
    productDecision:
      'The long head of the triceps has its own slot, trained twice a week with overhead options.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'kassiano-2025-incline-preacher',
    title: 'Distinct muscle growth and strength adaptations after preacher and incline biceps curls',
    publisher: 'International Journal of Sports Medicine 46(5):334-343 (Kassiano and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/39809454/',
    published: '2025',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Incline curls, with the arm behind the body, grew the upper biceps more than preacher curls, while preacher curls favoured other regions.',
    productDecision:
      'The biceps get two slots: arm behind the body, and arm in front on a preacher pad.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text. Regional results are less certain than whole muscle results.',
    access: 'search-snippet',
  },
  {
    id: 'kubo-2019-squat-depth',
    title: 'Effects of squat training with different depths on lower limb muscle volumes',
    publisher: 'European Journal of Applied Physiology (Kubo and colleagues)',
    url: 'https://doi.org/10.1007/s00421-019-04181-y',
    published: '2019',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Deep squats grew the glutes and adductors more than half squats, and the quads similarly.',
    productDecision:
      'Every squat option is done deep, with safety stops set to that depth.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'plotkin-2023-hip-thrust-squat',
    title: 'Hip thrust and back squat training elicit similar gluteus muscle hypertrophy and transfer similarly to the deadlift',
    publisher: 'Frontiers in Physiology (Plotkin and colleagues)',
    url: 'https://doi.org/10.3389/fphys.2023.1279170',
    published: '2023',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Hip thrusts and squats grew the glutes about equally, and neither grew the side of the hip much.',
    productDecision:
      'Hip thrusts, split squats, and lunges are equal glute choices. The side of the hip has its own slot.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'kassiano-2023-calf-long-length',
    title: 'Greater Gastrocnemius Muscle Hypertrophy After Partial Range of Motion Training Performed at Long Muscle Lengths',
    publisher: 'Journal of Strength and Conditioning Research 37(9):1746-1753 (Kassiano and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/37015016/',
    published: '2023',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Training the stretched half of the calf raise grew the calf more than the full range, about 15 against 7 percent.',
    productDecision:
      'Calf raises use a two second pause in the deep stretch.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'kinoshita-2023-standing-seated-calf',
    title: 'Triceps surae muscle hypertrophy is greater after standing versus seated calf-raise training',
    publisher: 'Frontiers in Physiology 14:1272106 (Kinoshita and colleagues)',
    url: 'https://doi.org/10.3389/fphys.2023.1272106',
    published: '2023',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Standing calf raises grew the gastrocnemius far more than seated raises, and the soleus about equally.',
    productDecision:
      'The calf slot uses straight knee raises only. The seated calf raise stays in the library.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'larsen-2024-leg-extension-hip-angle',
    title: 'The effects of hip flexion angle on quadriceps femoris muscle hypertrophy in the leg extension exercise',
    publisher: 'Journal of Sports Sciences 43(2):210-221 (Larsen and colleagues)',
    url: 'https://pure.solent.ac.uk/en/publications/the-effects-of-hip-flexion-angle-on-quadriceps-femoris-muscle-hyp/',
    published: '2024',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Leg extensions with the hips more extended, leaning back, grew the rectus femoris more.',
    productDecision:
      'Leg extensions are done leaning back in the seat.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'kinoshita-2026-knee-extension-leg-press',
    title: 'Hypertrophic Effects of Single- versus Multi-Joint Exercise: A Direct Comparison between Knee Extension and Leg Press',
    publisher: 'Medicine and Science in Sports and Exercise 58(7) (Kinoshita and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/41630124/',
    published: '2026',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Leg extensions grew the rectus femoris much more than the leg press, which barely grew it.',
    productDecision:
      'The rectus femoris has its own slot, twice a week.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
    access: 'search-snippet',
  },
  {
    id: 'haroy-2019-adductor-programme',
    title: 'The Adductor Strengthening Programme prevents groin problems among male football players: a cluster-randomised controlled trial',
    publisher: 'British Journal of Sports Medicine 53(3):145-152 (Harøy and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/29891614/',
    published: '2019',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'A short adductor programme reduced groin problems in football players.',
    productDecision:
      'The inner thigh has its own slot twice a week.',
    uncertainty: 'Football players, not volleyball players.',
    access: 'search-snippet',
  },
  {
    id: 'andersson-2017-shoulder-warmup',
    title: 'Preventing overuse shoulder injuries among throwing athletes: a cluster-randomised controlled trial in 660 elite handball players',
    publisher: 'British Journal of Sports Medicine 51(14):1073-1080 (Andersson and colleagues)',
    url: 'https://ostrc.no/en/projects/preventing-overuse-shoulder-injuries-among-throwing-athletes-a-cluster-randomised-controlled-trial-in-660-elite-handball-players/',
    published: '2017',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'A shoulder warm up three times a week reduced shoulder problems in overhead athletes, from about 23 to 17 percent.',
    productDecision:
      'Every upper gym day starts with light external rotation work, at three reps in reserve. The spike arm swing is practised at home without a ball until the wrist is cleared.',
    uncertainty: 'Handball players, not volleyball players.',
    access: 'search-snippet',
  },
  {
    id: 'baz-valle-2019-variation',
    title: 'The effects of exercise variation in muscle thickness, maximal strength and motivation in resistance trained men',
    publisher: 'PLoS ONE (Baz-Valle and colleagues)',
    url: 'https://doi.org/10.1371/journal.pone.0226989',
    published: '2019',
    reviewedOn: '2026-09-30',
    topic: 'youth-training',
    conclusion:
      'Varying exercises gave the same muscle and strength gains as a fixed plan and raised motivation.',
    productDecision:
      'The athlete picks a favourite exercise for each muscle head, with an optional second choice for variety, and can change picks later.',
    uncertainty: 'Adult participants. Only search results and abstract level numbers were read, not the full text.',
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
      'PeakForm sets no calorie target and never suggests eating less. If weight falls faster than about 0.45 kg a week, it suggests eating more and talking with a parent. Weight and body fat goals go to a parent and a pediatric professional (3.0.0).',
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
      'If the seven day average falls faster than about 0.5 kg a week after the first week, PeakForm suggests adding 150 to 200 calories and talking with a parent. Since 2.1.0 that threshold sits at the low end of the 1 to 2 lb a week guidance, because a growing athlete training for jump height needs the energy.',
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
      'Low intake on fully logged days, or a slide in energy, mood, sleep, or performance, leads to eating more and a parent, even when weight is stable, because stable weight does not prove that food is enough. The 30 kcal per kg threshold comes mostly from female athletes and is not used as a number.',
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
      'Smart scale body fat and muscle figures are labelled uncertain estimates, are never an input to the nutrition check, and are never turned into kilograms of muscle or fat.',
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
      'Since 3.0.0 there are no early morning sessions. The check in moves to 07:00 and wind down to 21:30, so 8 to 10 hours fit, and training is never planned at the cost of sleep.',
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
      'Sleep feeds the readiness indicator and the weekly review. Since 3.1.0, a night under 8 hours before a home jump day shows advice to do one set of each jump drill. PeakForm does not change the plan by itself.',
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
      'PeakForm never starts, increases, or recommends creatine. It records the product, dose, testing, and who reviewed it, explains early water gain on the scale, and lists an unreviewed supplement as a reason for a professional review.',
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
      'Adolescent evidence is limited, so creatine stays a decision for the athlete, a parent, and a clinician, recorded but never promoted.',
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
      'Recipes refrigerate cooked food within two hours, cool rice quickly and freeze it after a day or two, and school food that is brought from home travels cold with two ice packs.',
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
  // ---------- Jump program and dunk goal (2.1.0), reviewed 2026-10-02 ----------
  {
    id: 'ramirez-campillo-2023-plyo-maturity',
    title: 'Plyometric-Jump Training Effects on Physical Fitness and Sport-Specific Performance According to Maturity: A Systematic Review with Meta-analysis',
    publisher: 'Sports Medicine - Open (Ramirez-Campillo and colleagues)',
    url: 'https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-023-00568-6',
    published: '2023',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Youth before and after peak height velocity gained small to moderate improvements from jump training over 4 to 36 weeks at 1 to 3 sessions a week. The minimal effective dose was about 4 weeks, 8 sessions, and 92 jumps a week.',
    productDecision:
      'Two home jump sessions a week, 72 hours apart, at about 60 landings each to start: within the effective weekly dose in this analysis. Volume changes only after a review, never automatically.',
    uncertainty: 'Search snippets only. Maturity groups were pooled across sports.',
    access: 'search-snippet',
  },
  {
    id: 'moran-2017-youth-cmj-maturity',
    title: "Age-related variation in male youth athletes' countermovement jump after plyometric training: a meta-analysis",
    publisher: 'Journal of Strength and Conditioning Research (Moran and colleagues)',
    url: 'https://pure.hartpury.ac.uk/en/publications/age-related-variation-in-male-youth-athletes-countermovement-jump/',
    published: '2017',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Countermovement jump gains were smaller around the growth spurt (ages about 13 to 16, effect size 0.47) than before or after it (about 0.9 to 1.0).',
    productDecision: 'The dunk estimates in the app are kept modest, and progress is judged by tests every four weeks rather than promised.',
    uncertainty: 'Search snippets only. Maturity was estimated from age bands.',
    access: 'search-snippet',
  },
  {
    id: 'saez-de-villarreal-2009-plyo-dose',
    title: 'Determining variables of plyometric training for improving vertical jump height performance: a meta-analysis',
    publisher: 'Journal of Strength and Conditioning Research 23(2):495-506 (Saez de Villarreal and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/19197203/',
    published: '2009',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Programs longer than 10 weeks with more than 20 sessions gave the largest gains. Mixing jump types beat a single type, and adding external weight to jumps gave no extra benefit.',
    productDecision: 'Each jump session mixes several drills, the program lasts 17 weeks, and no jump is done with added weight.',
    uncertainty: 'Mostly adult studies. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'bedoya-2015-youth-plyo-volume',
    title: 'Plyometric training effects on athletic performance in youth soccer athletes: a systematic review',
    publisher: 'Journal of Strength and Conditioning Research (Bedoya and colleagues)',
    url: 'https://lida.sport-iat.de/ta/Record/4035788?lng=en',
    published: '2015',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'For youth, two sessions a week with about 72 hours between them worked. Sessions should start at 50 to 60 foot contacts and rise to no more than 80 to 120, to prevent overuse injuries.',
    productDecision:
      'The introductory home session starts near 60 landings and the next level stays under about 100, on two days a week with 72 hours between them. No universal safe contact limit exists, so school jumping is counted too and quality decides when to stop.',
    uncertainty: 'Soccer players. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'lloyd-2014-youth-consensus',
    title: 'Position statement on youth resistance training: the 2014 International Consensus',
    publisher: 'British Journal of Sports Medicine 48(7):498-505 (Lloyd and colleagues)',
    url: 'https://bjsm.bmj.com/content/48/7/498',
    published: '2014',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Youth resistance and power training is safe and effective with qualified supervision and sound technique. Rest of 2 to 3 minutes may be needed between sets of high intensity power work.',
    productDecision: 'Jump drills get 60 to 120 seconds of rest and heavy sets 2.5 to 3 minutes. The app asks for technique checks with a coach, because the athlete trains alone.',
    uncertainty: 'Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'ma-2025-vertical-jump-programs',
    title: "Effects of Physical Training Programs on Healthy Athletes' Vertical Jump Height: A Systematic Review and Meta-Analysis",
    publisher: 'Journal of Sports Science and Medicine 24:236-257 (Ma and colleagues)',
    url: 'https://www.jssm.org/jssm-24-236.xml-abst',
    published: '2025',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Combining strength work with jumps improved countermovement jump by about 5 cm, against about 2 cm for jumps or strength training alone.',
    productDecision: 'Monday pairs heavy leg sets with box jumps from block 2, and both jump days are followed by heavy leg work.',
    uncertainty: 'Mixed ages and sports. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'pareja-blanco-2017-velocity-loss',
    title: 'Effects of velocity loss during resistance training on athletic performance, strength gains and muscle adaptations',
    publisher: 'Scandinavian Journal of Medicine and Science in Sports (Pareja-Blanco and colleagues)',
    url: 'https://www.uloyola.es/en/research-transfer/publications/effects-of-velocity-loss-during-resistance-training-on-athletic-performance-strength-gains-and-muscle-adaptations-article',
    published: '2017',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Ending squat sets well short of failure improved countermovement jump by 9.5 percent, against 3.5 percent for sets taken much closer to failure, with similar strength gains and 40 percent fewer reps.',
    productDecision:
      'Leg sets stop well short of failure, so the home jumps on the same day stay fast (3.0.0).',
    uncertainty: 'Adult men. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'moran-navarro-2017-failure-recovery',
    title: 'Time course of recovery following resistance training leading or not to failure',
    publisher: 'European Journal of Applied Physiology (Moran-Navarro and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/28965198/',
    published: '2017',
    reviewedOn: '2026-10-02',
    topic: 'recovery',
    conclusion: 'Sets to failure caused a larger drop in jump height and slowed recovery by up to 24 to 48 hours compared with the same volume stopped short of failure.',
    productDecision:
      'Sets to failure slow recovery by up to a day or two, one reason the 3.0.0 plan keeps two reps in reserve on the days next to jump work.',
    uncertainty: 'Ten trained adult men. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'cmj-vs-drop-jump-2020-volleyball',
    title: 'Countermovement Jump Training Is More Effective Than Drop Jump Training in Enhancing Jump Height in Non-professional Female Volleyball Players',
    publisher: 'Frontiers in Physiology',
    url: 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7091110/',
    published: '2020',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Over 6 weeks, training built mostly on countermovement jumps raised jump height about 17 percent, against about 7 percent for training built mostly on drop jumps.',
    productDecision: 'Countermovement style jumps, broad jumps, and full approach jumps are the core of the home jump sessions. Depth jumps are not planned at the starting and next levels (3.0.1).',
    uncertainty: 'Adult women. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'fuchs-2020-spike-technique',
    title: 'Effect of differential training on female volleyball spike-jump technique and performance',
    publisher: 'Applied Sciences (Fuchs and colleagues)',
    url: 'https://www.mdpi.com/2076-3417/10/17/5921',
    published: '2020',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Six weeks of short approach technique sessions raised spike jump height about 12 percent in elite female players.',
    productDecision: 'Since 3.0.1 the Monday and Thursday home sessions end with approach footwork and then full approach jumps, outdoors or in a hall, with the touch height logged when a wall is marked. Friday keeps the approach rhythm without jumps.',
    uncertainty: 'Elite adult women. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'vint-1996-one-two-foot',
    title: 'Differences between One-Foot and Two-Foot Vertical Jump Performances',
    publisher: 'Journal of Applied Biomechanics (Vint and Hinrichs)',
    url: 'https://researchgate.net/profile/Richard-Hinrichs-2/publication/288544133_Differences_between_One-Foot_and_Two-Foot_Vertical_Jump_Performances/links/591b901c4585153b614fa759/Differences-between-One-Foot-and-Two-Foot-Vertical-Jump-Performances.pdf',
    published: '1996',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'With a four step approach, one foot and two foot takeoffs reached similar overall heights, through different mechanics.',
    productDecision: 'Block 1 alternates both takeoffs so the athlete keeps the one that touches higher.',
    uncertainty: 'Fourteen adults. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'vaverka-2016-arm-swing',
    title: 'Effect of an Arm Swing on Countermovement Vertical Jump Performance in Elite Volleyball Players',
    publisher: 'Journal of Human Kinetics (Vaverka and colleagues)',
    url: 'https://johk.pl/?p=3938',
    published: '2016',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'A full arm swing raised jump height substantially in elite volleyball players; other studies put the gain at about 10 to 15 percent.',
    productDecision: 'Box jumps, broad jumps, and approach jumps all use a hard double arm swing.',
    uncertainty: 'Elite adults. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'dunk-height-calculators',
    title: 'Dunk calculators: how high above the rim the hand must reach',
    publisher: 'Omni Calculator and other coaching tools (not peer reviewed)',
    url: 'https://www.omnicalculator.com/sports/dunk',
    published: 'Not stated in search result',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'A one hand dunk needs the hand about 15 cm above the 305 cm rim when the ball can be palmed, and about 20 cm or more when it cannot.',
    productDecision:
      'Retired in 3.0.0. PeakForm no longer sets a dunk height or deadline. Jump progress comes from repeatable jump and reach tests.',
    uncertainty: 'Not research. Arm length and hand size vary a lot, so the app relies on measured touch heights.',
    access: 'search-snippet',
  },
  {
    id: 'barlow-2007-expert-committee',
    title: 'Expert committee recommendations regarding the prevention, assessment, and treatment of child and adolescent overweight and obesity: summary report',
    publisher: 'Pediatrics (Barlow and the Expert Committee)',
    url: 'https://www.citedrive.com/en/discovery/expert-committee-recommendations-regarding-the-prevention-assessment-and-treatment-of-child-and-adolescent-overweight-and-obesity-summary-report/',
    published: '2007',
    reviewedOn: '2026-10-02',
    topic: 'body-composition',
    conclusion: 'For adolescents in the upper BMI bands the goal is weight maintenance or gradual loss. Even at the highest band, loss should not exceed an average of about 0.9 kg a week.',
    productDecision: 'PeakForm adds food when weight falls faster than about 0.5 kg a week, and does not set a body fat target.',
    uncertainty: 'Replaced in part by the 2023 AAP guideline, whose snippets gave no rate target. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'desbrow-2014-adolescent-athlete',
    title: 'Sports Dietitians Australia position statement: sports nutrition for the adolescent athlete',
    publisher: 'International Journal of Sport Nutrition and Exercise Metabolism (Desbrow and colleagues)',
    url: 'https://sportsdietitians.com.au/wp-content/uploads/2020/07/15432742-International-Journal-of-Sport-Nutrition-and-Exercise-Metabolism-Sports-Dietitians-Australia-Position-Statement_-Sports-Nutrition-for-the-Adolescent-Athlete.pdf',
    published: '2014',
    reviewedOn: '2026-10-02',
    topic: 'nutrition',
    conclusion: 'Severe or prolonged energy restriction is not recommended in developing athletes, and weight maintenance is often more appropriate than loss. Body composition checks are rarely needed and belong with a trained professional.',
    productDecision:
      'Regular meals and snacks with protein spread over the day and carbohydrate around training. Example meals in grams are labelled as examples, never a limit, and personal targets come from a professional (3.0.0).',
    uncertainty: 'Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'murphy-2022-deficit-lean-mass',
    title: 'Energy deficiency impairs resistance training gains in lean mass but not strength: A meta-analysis and meta-regression',
    publisher: 'Scandinavian Journal of Medicine and Science in Sports (Murphy and Koehler)',
    url: 'https://portal.fis.tum.de/en/publications/energy-deficiency-impairs-resistance-training-gains-in-lean-mass-/',
    published: '2022',
    reviewedOn: '2026-10-02',
    topic: 'nutrition',
    conclusion: 'An energy deficit reduced lean mass gains from resistance training, and a deficit of about 500 kcal a day prevented them, while strength still improved.',
    productDecision: 'Calorie reductions stay small, 100 to 150 kcal at a time, so muscle can still be built while fat comes down.',
    uncertainty: 'Adults. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'mountjoy-2023-reds',
    title: "2023 International Olympic Committee's (IOC) consensus statement on Relative Energy Deficiency in Sport (REDs)",
    publisher: 'British Journal of Sports Medicine (Mountjoy and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/37752011/',
    published: '2023',
    reviewedOn: '2026-10-02',
    topic: 'nutrition',
    conclusion: 'Low energy availability harms health and performance in male and female athletes. Warning signs include falling performance, frequent illness or injury, poor sleep and mood, and stalled growth.',
    productDecision:
      'Same decision as the other REDs entry: no automatic cuts, and warning signs lead to more food and a professional review, whatever the scale says.',
    uncertainty: 'Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'smart-scale-accuracy-2021',
    title: 'Accuracy of Smart Scales on Weight and Body Composition: Observational Study',
    publisher: 'JMIR mHealth and uHealth',
    url: 'https://mhealth.jmir.org/2021/4/e22487',
    published: '2021',
    reviewedOn: '2026-10-02',
    topic: 'body-composition',
    conclusion: 'Consumer smart scales measured weight well but were not accurate for body composition, with median fat mass errors of about 2 to 4 kg.',
    productDecision:
      'Smart scale figures are shown at most as a weekly trend, with a note that water, food, timing, and creatine move them.',
    uncertainty: 'Adults. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'bahr-2014-jump-frequency',
    title: "Jump frequency may contribute to risk of jumper's knee: a study of interindividual and sex differences in a total of 11,943 jumps video recorded during training and matches in young elite volleyball players",
    publisher: 'British Journal of Sports Medicine 48(17):1322 (Bahr and Bahr)',
    url: 'https://bjsm.bmj.com/content/48/17/1322',
    published: '2014',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Young elite male volleyball players jumped between about 50 and 666 times a week, and total jump volume may matter more for jumper\'s knee than training hours.',
    productDecision: 'The app asks the athlete to count volleyball jumps with the planned jumps, and to do fewer planned jumps in heavy volleyball weeks.',
    uncertainty: 'Players aged 16 to 18. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'visnes-2013-jumpers-knee',
    title: "Training volume and body composition as risk factors for developing jumper's knee among young elite volleyball players",
    publisher: 'Scandinavian Journal of Medicine and Science in Sports (Visnes and Bahr)',
    url: 'https://lida.sport-iat.de/ta/Record/4030037?lng=en',
    published: '2013',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: "Over four years, the risk of jumper's knee rose with every extra weekly hour of volleyball training and every extra match set.",
    productDecision: 'Since 3.1.0, knee pain above 2 out of 10 the next morning skips the next home jump session, and in a week with many games the home jump session is the first thing to cut. Matches carried the most risk here.',
    uncertainty: 'Elite students aged 16 to 18. Search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'rathleff-2020-osgood-schlatter',
    title: 'Activity Modification and Knee Strengthening for Osgood-Schlatter Disease: A Prospective Cohort Study',
    publisher: 'Orthopaedic Journal of Sports Medicine 8(4) (Rathleff and colleagues)',
    url: 'https://vbn.aau.dk/ws/files/330945567/2325967120911106.pdf',
    published: '2020',
    reviewedOn: '2026-10-02',
    topic: 'youth-training',
    conclusion: 'Managing knee load by pain, with knee strengthening, gave a successful outcome in 80 percent of young athletes with Osgood-Schlatter disease at 12 weeks, though return to full sport took longer.',
    productDecision: 'Since 3.1.0 jumping continues only while knee, heel, shin, or Achilles pain stays at 2 out of 10 or less during the session and the next morning, the threshold of this adolescent protocol. Above that, Today and the Train day say to skip the jumps that day, and the safety page lists signs that need a doctor.',
    uncertainty: 'Ages 10 to 14, 51 participants. Search snippets only.',
    access: 'search-snippet',
  },
  // ---------- Home and gym week, recovery, food data (3.0.0), reviewed 2026-10-06 ----------
  {
    id: 'schoenfeld-2019-frequency',
    title: 'How many times per week should a muscle be trained to maximize muscle hypertrophy? A systematic review and meta-analysis',
    publisher: 'Journal of Sports Sciences (Schoenfeld, Grgic, Krieger)',
    url:
      'https://mennohenselmans.com/training-frequency-2018-meta-analysis-review/',
    published: '2019',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Across 25 studies in adults, training a muscle more often did not increase growth when weekly volume was the same.',
    productDecision:
      'Four gym days that train each muscle twice replace six days. Adult data, applied cautiously.',
    uncertainty:
      'Adult studies only. Seen through a secondary summary page, because the journal page was not captured in the search.',
    access: 'search-snippet',
  },
  {
    id: 'saric-2019-3-vs-6-days',
    title: 'Resistance Training Frequencies of 3 and 6 Times Per Week Produce Similar Muscular Adaptations in Resistance-Trained Men',
    publisher: 'Journal of Strength and Conditioning Research (Saric and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/30363041/',
    published: '2019',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Six weeks of training three or six days a week with equal volume gave similar strength and muscle gains in 27 trained men.',
    productDecision:
      'Supports moving from six to four strength days without losing useful weekly volume.',
    uncertainty:
      'Small, short study in trained adult men.',
    access: 'search-snippet',
  },
  {
    id: 'jayanthi-2015-hours-vs-age',
    title: 'Sports-Specialized Intensive Training and the Risk of Injury in Young Athletes: A Clinical Case-Control Study',
    publisher: 'American Journal of Sports Medicine 43(4) (Jayanthi and colleagues)',
    url: 'https://journals.sagepub.com/doi/10.1177/0363546514567298',
    published: '2015',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'In 1,190 athletes aged 7 to 18, more weekly hours of organised sport than the athlete\'s age in years, and specialised training, went with serious overuse injuries.',
    productDecision:
      'School and club sport is logged and added to the plan\'s minutes; weeks above the athlete\'s age in hours become a recovery concern in the review. A prompt to review, not a limit.',
    uncertainty:
      'Case-control association, not proof of cause.',
    access: 'search-snippet',
  },
  {
    id: 'aap-overuse-2024',
    title: 'Overuse Injuries, Overtraining, and Burnout in Young Athletes',
    publisher: 'Pediatrics 153(2):e2023065129 (Brenner, Watson; AAP Council on Sports Medicine and Fitness)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/38247370/',
    published: '2024',
    reviewedOn: '2026-10-06',
    topic: 'recovery',
    conclusion:
      'Advises one to two days a week off organised sport and training, time off across the year, and attention to growth related injuries.',
    productDecision:
      'Tuesday and Saturday have no structured training, and school sport counts as training.',
    uncertainty:
      'Clinical report seen through search snippets only.',
    access: 'search-snippet',
  },
  {
    id: 'aasm-2016-sleep-consensus',
    title: 'Recommended Amount of Sleep for Pediatric Populations: A Consensus Statement of the American Academy of Sleep Medicine',
    publisher: 'Journal of Clinical Sleep Medicine 12(6) (Paruthi and colleagues)',
    url:
      'https://depts.washington.edu/dbpeds/pediatricsleepdurationconsensus.pdf',
    published: '2016',
    reviewedOn: '2026-10-06',
    topic: 'recovery',
    conclusion:
      'Teenagers aged 13 to 18 should sleep 8 to 10 hours per 24 hours.',
    productDecision:
      'No early morning training; the timeline aims for sleep near 22:15 before a 07:00 check in.',
    uncertainty:
      'Expert consensus.',
    access: 'search-snippet',
  },
  {
    id: 'gudmundsdottir-2020-early-training-sleep',
    title: 'Training Schedule and Sleep in Adolescent Swimmers',
    publisher: 'Pediatric Exercise Science 32(1) (Gudmundsdottir)',
    url: 'https://opinvisindi.is/handle/20.500.11815/2351',
    published: '2020',
    reviewedOn: '2026-10-06',
    topic: 'recovery',
    conclusion:
      'Adolescent swimmers slept only about five to five and a half hours before early morning training sessions.',
    productDecision:
      'Removes the 05:30 home sessions from the default week.',
    uncertainty:
      'Swimmers, actigraphy, one country; applied by analogy.',
    access: 'search-snippet',
  },
  {
    id: 'bhanushali-2023-forearm-fracture-rts',
    title: 'Return to sport after forearm fractures in children: A scoping review and survey',
    publisher: 'Journal of Children\'s Orthopaedics (Bhanushali, Bright, Xu, Cundy, Williams)',
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC10080236/',
    published: '2023',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Return to sport timing varies with the fracture type, roughly four weeks for buckle fractures and longer for others, and recommendations differ between surgeons.',
    productDecision:
      'Wrist status is recorded in the profile. Until a clinician confirms clearance, gripping and pressing loads stay the same, heavy grip exercises are swapped, and there is no ball contact or falling onto the hands.',
    uncertainty:
      'Children, mixed fracture types, survey based; the treating clinician decides.',
    access: 'search-snippet',
  },
  {
    id: 'schoenfeld-2013-soreness',
    title: 'Is Postexercise Muscle Soreness a Valid Indicator of Muscular Adaptations?',
    publisher: 'Strength and Conditioning Journal (Schoenfeld, Contreras)',
    url:
      'https://bretcontreras.com/wp-content/uploads/Is-Postexercise-Muscle-Soreness-a-Valid-Indicator-of-Muscular-Adaptations.pdf',
    published: '2013',
    reviewedOn: '2026-10-06',
    topic: 'recovery',
    conclusion:
      'Soreness is a poor indicator of muscle growth and fades as the body adapts to repeated training.',
    productDecision:
      'The check in explains that soreness does not prove growth and separates it from joint, tendon, heel, and wrist pain.',
    uncertainty:
      'Narrative review.',
    access: 'search-snippet',
  },
  {
    id: 'aap-pes-2016',
    title: 'Use of Performance-Enhancing Substances',
    publisher: 'Pediatrics 138(1):e20161300 (LaBotz, Griesemer; AAP Council on Sports Medicine and Fitness)',
    url: 'https://publications.aap.org/pediatrics/article/138/1/e20161300/52580/',
    published: '2016',
    reviewedOn: '2026-10-06',
    topic: 'supplements',
    conclusion:
      'Strongly discourages performance enhancing substances, including creatine, for young athletes, and notes that product purity cannot be assured.',
    productDecision:
      'PeakForm never recommends or increases a supplement and lists an unreviewed supplement as a reason for a professional review.',
    uncertainty:
      'Search snippets only; other expert bodies accept creatine in supervised adolescents, so experts disagree.',
    access: 'search-snippet',
  },
  {
    id: 'nasem-2023-energy-dri',
    title: 'Dietary Reference Intakes for Energy',
    publisher: 'National Academies of Sciences, Engineering, and Medicine',
    url:
      'https://www.nationalacademies.org/read/26818/chapter/2',
    published: '2023',
    reviewedOn: '2026-10-06',
    topic: 'nutrition',
    conclusion:
      'Estimated energy requirements for boys depend on age, height, weight, and physical activity level, and for active teenage boys often exceed 3,000 kcal a day.',
    productDecision:
      'PeakForm does not calculate a personal target. The Eat screen says that active teens often need more than the example meals and points to a pediatric sports dietitian.',
    uncertainty:
      'Population equations; individual needs differ, and the inputs here (height, activity) are unconfirmed.',
    access: 'search-snippet',
  },
  {
    id: 'chen-2023-plyo-adolescents',
    title: 'Meta-Analysis of the Effects of Plyometric Training on Lower Limb Explosive Strength in Adolescent Athletes',
    publisher: 'International Journal of Environmental Research and Public Health 20(3):1849 (Chen and colleagues)',
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC9915200/',
    published: '2023',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Plyometric programmes improved countermovement jump by about 2.7 cm on average in adolescent athletes.',
    productDecision:
      'Jump progress is measured with repeatable tests every four weeks, and averages are explained as averages, never as a forecast for one person.',
    uncertainty:
      'Wide differences between studies and people.',
    access: 'search-snippet',
  },
  {
    id: 'collins-2018-rt-weight-status-youth',
    title: 'The effect of resistance training interventions on weight status in youth: a meta-analysis',
    publisher: 'Sports Medicine Open (Collins and colleagues)',
    url:
      'https://discovery.dundee.ac.uk/en/publications/the-effect-of-resistance-training-interventions-on-weight-status-/',
    published: '2018',
    reviewedOn: '2026-10-06',
    topic: 'body-composition',
    conclusion:
      'Resistance training had a small effect on body fat percentage in youth, and the change in lean mass was not significant.',
    productDecision:
      'No muscle or body fat forecasts. Aspirations are recorded in the athlete\'s words and reviewed with a professional.',
    uncertainty:
      'Mixed populations and measurement methods.',
    access: 'search-snippet',
  },
  {
    id: 'bia-children-validity',
    title: 'Validity of Four Commercial Bioelectrical Impedance Scales in Measuring Body Fat among Chinese Children and Adolescents',
    publisher:
      'PubMed Central record (journal not shown in the search result)',
    url: 'https://pmc.ncbi.nlm.nih.gov/articles/PMC4475745/',
    published:
      'Not shown in the search result',
    reviewedOn: '2026-10-06',
    topic: 'body-composition',
    conclusion:
      'Consumer impedance scales agreed only poorly to moderately with DXA in children and adolescents.',
    productDecision:
      'Smart scale numbers are labelled uncertain estimates and never drive any suggestion.',
    uncertainty:
      'Different population and devices.',
    access: 'search-snippet',
  },
  {
    id: 'turicchi-2020-weight-fluctuation',
    title:
      'Weekly, seasonal and holiday body weight fluctuation patterns (title shortened in the search result)',
    publisher: 'PLoS ONE (Turicchi and colleagues)',
    url:
      'https://doaj.org/article/d41eea5765d944d8b6e3f5e1cd1d6af4',
    published: '2020',
    reviewedOn: '2026-10-06',
    topic: 'body-composition',
    conclusion:
      'Body weight follows weekly and seasonal rhythms, so short windows mislead.',
    productDecision:
      'Five days of stable weight is never called a plateau; trends need weeks, and weighing once a week is the default.',
    uncertainty:
      'Adults in a weight loss programme.',
    access: 'search-snippet',
  },
  {
    id: 'geyer-2004-supplement-contamination',
    title: 'Analysis of non-hormonal nutritional supplements for anabolic-androgenic steroids: results of an international study',
    publisher: 'International Journal of Sports Medicine 25(2) (Geyer and colleagues)',
    url: 'https://www.thieme-connect.com/products/ejournals/html/10.1055/s-2004-819955',
    published: '2004',
    reviewedOn: '2026-10-06',
    topic: 'supplements',
    conclusion:
      'About 15 percent of 634 supplements contained undeclared anabolic steroids.',
    productDecision:
      'The profile asks whether a supplement is third party tested, such as NSF Certified for Sport or Informed Sport.',
    uncertainty:
      'Older data, not specific to creatine.',
    access: 'search-snippet',
  },
  {
    id: 'usda-sr28-green-beans',
    title: 'USDA National Nutrient Database for Standard Reference, Release 28: snap beans (raw, boiled, frozen, canned) and olive oil',
    publisher: 'USDA Agricultural Research Service',
    url: 'https://fdc.nal.usda.gov/',
    published: '2015 (SR28), in FoodData Central as SR Legacy',
    reviewedOn: '2026-10-06',
    topic: 'nutrition',
    conclusion:
      'Per 100 g: raw 31 kcal, boiled and drained 35 kcal, frozen and boiled 28 kcal, canned and drained 22 kcal; olive oil 884 kcal.',
    productDecision:
      'Separate food entries for each state, and the green bean calculator shows the arithmetic for the amount entered, with any oil.',
    uncertainty:
      'Rows read from a mirror of the SR28 data file; the FDC pages could not be opened.',
    access: 'search-snippet',
  },
  {
    id: 'rossler-2014-youth-injury-prevention',
    title: 'Exercise-Based Injury Prevention in Child and Adolescent Sport: A Systematic Review and Meta-Analysis',
    publisher: 'Sports Medicine (Rössler and colleagues)',
    url: 'https://pubmed.ncbi.nlm.nih.gov/25129698/',
    published: '2014',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Exercise based programmes with landing, balance, and strength work roughly halved injury rates in young athletes.',
    productDecision:
      'Since 3.1.0 every home jump session starts with a 10 minute warm up that includes landing, balance, and trunk control, before any bigger jumps.',
    uncertainty:
      'Mixed sports and programmes.',
    access: 'search-snippet',
  },
  {
    id: 'ioc-2015-youth-development',
    title: 'International Olympic Committee consensus statement on youth athletic development',
    publisher: 'British Journal of Sports Medicine 49:843-851 (Bergeron and colleagues)',
    url: 'https://bjsm.bmj.com/content/49/13/843',
    published: '2015',
    reviewedOn: '2026-10-06',
    topic: 'youth-training',
    conclusion:
      'Youth training should fit growth and maturation, put health first, and avoid excessive load.',
    productDecision:
      'Flexible four month stages with process goals replace dated blocks aimed at a deadline.',
    uncertainty:
      'Expert consensus.',
    access: 'search-snippet',
  },
];
