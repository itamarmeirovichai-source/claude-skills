# PeakForm nutrition and food data audit (3.0.0)

Audit date: 6 October 2026. This file is public and de-identified: it uses no personal measurements, no food history, and no names. Personal details live only on the phone and in the private plan export.

Scope: `src/content/foods.ts`, `src/content/meals.ts`, `src/content/recipes.ts`, `src/domain/nutrition.ts`, `src/domain/recipeMath.ts`, `src/domain/kosher.ts`, the Eat, Meal prep, Goals, and Review screens, and their tests.

## 1. How the evidence was checked, and what could not be

- **Web pages could not be opened.** Fetching was blocked for every primary site tried (AAP, IOC, PubMed Central, NIH ODS, USDA FoodData Central, NHS, FSIS, Sports Dietitians Australia). Almost every reference below is a **search result snippet**, not the paper or the database page.
- **One exception.** The USDA SR28 nutrient file (public domain) was read as raw data rows through a GitHub mirror, for the green bean and olive oil rows.
- **The search budget ran out** partway through. Food safety, kosher practice, FODMAP content, and the AAP 2016 paper on preventing obesity and eating disorders were **not searched**. What this file says on those topics comes from general knowledge and is marked as unverified (section 10).
- **No FDC ID was supplied from memory.** Where an FDC ID could not be confirmed, the table says so.
- Adult evidence is marked when it is applied to a teenager.

## 2. Findings ranked by importance, and what 3.0 did about them

| # | Severity | Finding in 2.1 | Status in 3.0 |
| --- | --- | --- | --- |
| 1 | High | **The calorie target was the sum of the example meals, not an estimate of need.** Every day was set to about 2,250 kcal (band 2,150 to 2,350). Nothing derived it from an energy requirement. The top of the band worked as a ceiling: the weekly review listed days above it under "Improve". For active boys in their mid teens, the 2023 energy equations give roughly 2,900 to well over 4,000 kcal a day (section 6), so 2,250 was likely a hidden deficit. | **Fixed.** No default calorie target. The Eat screen shows the example meals as examples, "not a target", with a context note. A calorie range appears only when the athlete records one that a professional reviewed, with source, role, date, and status. The review never counts eating more as a problem. |
| 2 | High | **The nutrition check could suggest eating 100 to 150 kcal less** when weight and waist were stable. A stable weight in a growing athlete is not a plateau, and a cut for a minor is outside what the app should decide. | **Fixed.** The check never suggests eating less (a test checks every outcome). Possible results: not enough data, no change, eat more (loss above about 0.45 kg a week), or talk with a parent (energy, mood, sleep, or performance dipped). |
| 3 | High (kashrut) | **Dairy after meat.** The evening milk came 1 h 45 min after the meat dinner on three days. There was no meat, dairy, or pareve data. | **Fixed.** Every food has a kosher category. The meat to dairy interval is a family setting (default 6 hours, the most widespread custom and the cautious choice). When the evening milk would come too soon after meat, a pareve snack is planned instead. Logged meals show the category and when dairy is fine again. The Sabbath note says to choose a pareve dessert after a meat meal. |
| 4 | High (food safety) | **School lunch storage contradicted the shopping list.** The app said nothing needed refrigeration, yet the list bought eggs and tofu to carry. | **Fixed.** Cafeteria food needs nothing from home. Food brought from home goes in an insulated bag with two ice packs, and perishable food should not sit warm for more than two hours (one hour above 32°C). Unverified source, section 10. |
| 5 | Medium | **Lentil yield.** The note said 100 g dry makes 250 g cooked, while the cooked values the app uses imply about 3 times. | **Fixed.** A yield table: lentils 3.0 (range 2.7 to 3.1), rice 2.7 (2.5 to 3.0), chicken breast 0.72 (0.68 to 0.78). Dry and raw entries were added so either weight can be logged. |
| 6 | Medium | **Egg and egg white held raw values but were labelled cooked.** | **Fixed.** Labelled raw, with a note that boiled values are within about 10 percent. |
| 7 | Medium | **Cooked rice and fish could be up to 4 to 5 days old** by Wednesday, depending on the prep day. | **Fixed.** Keep the next day or two in the fridge and freeze the rest as soon as it cools; cooked rice is safest eaten soon or frozen, and reheated only once. |
| 8 | Medium | **Yogurt on the shopping list did not match the food used** (ordinary yogurt instead of high protein). | **Fixed.** The list and the food now say high protein yogurt or skyr. |
| 9 | Medium-low | **Tofu calcium is 350 mg; calcium sulfate tofu is about 680 mg.** | **Noted.** Calcium depends on the coagulant. The food note says so and asks to check the label. |
| 10 | Medium-low | **"Mixed vegetables" (35 kcal) is half a standard frozen mix with corn and peas (about 65 kcal).** | **Fixed.** Renamed "Non starchy vegetables, cooked", with a note on the standard frozen mix. |
| 11 | Low-medium | **Tuna in water matches an older USDA entry; another gives about 86 kcal per 100 g.** | **Noted** in the food entry. |
| 12 | Low | **Tahini existed only as prepared sauce.** | **Fixed.** Raw tahini paste added (595 kcal per 100 g). |
| 13 | Low | **The soup computed 0 kcal in the app** because no ingredient was linked to a food. | **Fixed.** Recipe nutrition is computed from the ingredients and the cooked yield. |
| 14 | Low | **No hidden oil in example dinners.** | **Changed.** Dinners include 5 g olive oil. Restaurant and hosted meals still add an unseen oil range. |

## 3. What the 3.0 nutrition model does and does not do

**Does:**
- Shows example meals with gram amounts, household measures, raw, cooked, dry, frozen, or drained state, kosher category, storage, and options for more food. Every example says: "Example serving. Adjust to appetite and activity; this is not a daily limit."
- Shows a calm context note: teen athletes often need more than the examples, and a pediatric sports dietitian can give a personal number.
- Records targets only when a professional reviewed them, kept apart from the athlete's own aspirations, which are stored word for word and never become targets.
- Reads weight weekly by default (one morning a week). A trend needs 3 of the last 4 weeks, or two full weeks of several mornings in the frequent mode. Weight can be hidden or switched off.

**Does not:**
- Set or lower a calorie target by itself, or treat 2,000 kcal (an adult food label figure) as a floor.
- Suggest eating less, skipping meals, fasting, water cutting, or removing carbohydrate.
- Treat food as earned through exercise, or add exercise to make up for food.
- Call a stable weight over a few days a plateau.
- Use smart scale body fat for targets.

## 4. Food by food

Per 100 g (per 100 ml for liquids): kcal / protein g / carbohydrate g / fat g / fibre g / calcium mg. "Snippet" means the reference value came from a search snippet. "Flag" means a difference above 10 percent, or above 2 g for a macronutrient.

| Food id | State | App values | Reference | Reference values | Access | Verdict |
| --- | --- | --- | --- | --- | --- | --- |
| yogurt-hp | as sold | 68/10.5/4.0/1.2/0/120 | SR 170903 Greek yogurt, plain, lowfat; skyr labels | 73/9.9/3.9/1.9; labels about 60/10/4/0.2 | snippet | OK |
| banana | raw | 89/1.1/22.8/0.3/2.6/5 | FDC 173944 | 89/1.09/22.84/0.33/2.6/5 | snippet | Match |
| oats | dry | 379/13.2/67.7/6.5/10.1/52 | FDC 173904 | 379/13.2/67.7/6.5/10.1 | snippet | Match |
| berries-frozen | frozen | 50/0.8/11.5/0.3/3.5/15 | FNDDS 2709272 | 52/0.8/12.5/0.3/4.1 | snippet | OK; state fixed to frozen |
| protein-powder | as sold | 390/78/8/5/0/400 | Typical whey label | about 395/79/10/5 | snippet | Matches a label. Not part of any example by default |
| egg | raw | 143/12.6/0.7/9.5/0/56 | FDC 171287 | 143/12.6/0.7/9.5/56 | snippet | Match; label fixed |
| egg-white | raw | 52/10.9/0.7/0.2/0/7 | FDC 172183 | 52/10.9/0.7/0.2 | snippet | Match; label fixed |
| tofu | as sold | 144/17.3/2.8/8.7/2.3/350 | FDC 172475 (calcium sulfate) | 144/17.3/2.8/8.7/2.3/683 | snippet | Macros match. **Calcium flag**, explained in the note |
| olives | as sold | 130/1.0/5.0/13.0/3.0/60 | FDC 169094 ripe; 169096 green | 116 to 145 kcal | snippet | Average of green and black |
| rice-cooked | cooked | 130/2.7/28.2/0.3/0.4/10 | FDC 168878 | 130/2.7/28.2/0.3/0.4 | snippet | Match |
| rice-dry | dry | 365/7.1/80.0/0.7/1.3/28 | FDC 168877 | 365/7.1/80.0/0.7/1.3 | snippet | New; match |
| potato | cooked (boiled) | 87/1.9/20.1/0.1/1.8/5 | SR 11365 (FDC ID unverified) | 87/1.87/20.13/0.10/1.8 | snippet | Match for boiled. Roasted potatoes are denser per 100 g |
| potato-raw | raw | 77/2.0/17.5/0.1/2.1/12 | FDC 170026 | not re-checked | snippet | New |
| sweet-potato | cooked | 90/2.0/20.7/0.2/3.3/38 | SR 11508 (FDC ID unverified) | about 90/2.0/20.7/0.15/3.3/38 | snippet | Match |
| pasta-cooked | cooked | 158/5.8/30.9/0.9/1.8/7 | FDC 169737 | 158/5.8/30.9/0.9/1.8 | snippet | Match |
| couscous-cooked | cooked | 112/3.8/23.2/0.2/1.4/8 | FDC 169700 | 112/3.8/23.2/0.2 | snippet | Match |
| quinoa-cooked | cooked | 120/4.4/21.3/1.9/2.8/17 | FDC 168917 | 120/4.4/21.3/1.9/2.8 | snippet | Match |
| bread-wholewheat | as sold | 250/12/43/3.5/7.0/100 | FDC 172688 | 252/12.4/42.7/3.5/6.0 | snippet | Match; calcium unverified |
| challah | as sold | 290/8.5/50/6/2/60 | Branded 2534895; aggregator | 279 to 283 kcal | snippet | Within thresholds |
| lentils-cooked | cooked | 116/9.0/20.1/0.4/7.9/19 | Boiled, no salt (FDC ID unverified) | 116/9.02/20.13/0.38/7.9 | snippet | Match; yield fixed |
| lentils-dry | dry | 352/24.6/63.4/1.1/10.7/35 | FDC 172420 | 352/24.6/63.4/1.1 | snippet | New; match |
| chickpeas-cooked | cooked | 164/8.9/27.4/2.6/7.6/49 | FDC 173757 | 164/8.9/27.4/2.6/7.6/49 | snippet | Match |
| chicken-breast | cooked | 165/31.0/0/3.6/0/15 | FDC 171477 | 165/31.02/0/3.57 | snippet | Match |
| chicken-raw | raw | 120/22.5/0/2.6/0/5 | FDC 171077 | about 120/22.4 | snippet | New; match |
| salmon | cooked | 206/22.1/0/12.4/0/15 | FDC 175168 (farmed) | 206/22.1/0/12.3 | snippet | Match for farmed |
| beef-lean | cooked | 200/27.0/0/10.0/0/15 | FDC 174031 (90% lean, broiled) | 217/26.1/0/11.8 | snippet | Within thresholds |
| white-fish | cooked | 105/23.0/0/1.2/0/15 | FDC 171956 (cod) | 105/22.8/0/0.9 | snippet | Match for cod; tilapia is about 20 percent higher |
| turkey-breast | cooked | 147/30.0/0/2.1/0/12 | FDC 174516 | 136/29.5/0/2.0 | snippet | Within thresholds |
| tuna-water | drained | 116/25.5/0/0.8/0/11 | FDC 171986; 173709 | 116/25.5; 86/19.4 | snippet | Matches one entry; note added |
| cottage-cheese | as sold | 95/11.0/1.5/5.0/0/90 | Local 5% label; SR 172179 | 95/11/1.5/5 | snippet | Match |
| veg-mixed | cooked | 35/2.0/7.0/0.3/3.0/35 | FDC 169967 broccoli; 170472 standard frozen mix | 35; 65 | snippet | Correct for non starchy vegetables; renamed |
| green beans (4 states) | see section 7 | see section 7 | SR28 rows 11052, 11053, 11061, 11056 | see section 7 | full data rows (mirror) | Match |
| peas | cooked | 84/5.4/15.6/0.2/5.5/27 | FDC 170420 | 84/5.4/15.6/0.2/5.5 | snippet | Match |
| olive-oil | as sold | 884/0/0/100/0/1 | SR 04053 | 884; teaspoon 4.5 g, tablespoon 13.5 g | full data row (mirror) | Match |
| tahini | prepared sauce | 290/8.0/10.0/25.0/4.0/150 | none verified | about half of paste | none | Unverified |
| tahini-raw | as sold | 595/17.0/21.2/53.8/9.3/426 | FDC 170189 | 595/17.0/21.2/53.8/9.3 | snippet | New; match |
| almonds | as sold | 579/21.2/21.6/49.9/12.5/269 | FDC 170567 | not re-checked this session | snippet | New |
| apple | raw | 52/0.3/13.8/0.2/2.4/6 | FDC 171688 | not re-checked this session | snippet | New |
| milk | as sold (ml) | 50/3.3/4.8/2.0/0/120 | FDC 171267 (2%) | 50/3.3/4.8/2.0 | snippet | Match; grams counted as millilitres, about 3 percent low |
| hummus | prepared | 240/7/14/17/6/40 | FDC 174289 | 237/7.8/15.0/17.8 | snippet | Match |
| pita | as sold | 275/9.1/55.7/1.2/2.2/86 | FDC 174915 | exact | snippet | Match |
| falafel | prepared | 333/13.3/31.8/17.8/5.0/54 | FDC 172455 | 333/13.3/31.8/17.8 | snippet | Match |
| schnitzel, shawarma, sweet portion | prepared | estimates | none found | n/a | none | Unverified; logged with wide ranges |
| fries | prepared | 312/3.4/41/15/3.8/18 | FDC 170698 | 312/3.4/41.4/14.7/3.8 | snippet | Match |
| pizza | prepared | 266/11.4/33/10/2.3/190 | FDC 173292 | 266/11.4/33.3/9.7/2.3; Ca about 170 | snippet | Match; calcium +12 percent |

## 5. Raw, dry, and cooked weights

| Item | Factor used | Range | Cross-check | Verdict |
| --- | --- | --- | --- | --- |
| Rice, dry to cooked | 2.7 | 2.5 to 3.0 | Energy 365 / 130 = 2.81 | Consistent |
| Lentils, dry to cooked | 3.0 | 2.7 to 3.1 | Energy 352 / 116 = 3.03; dry matter 91.7 / 30.4 = 3.02 | Consistent (was 2.5 in 2.1) |
| Chicken breast, raw to cooked | 0.72 | 0.68 to 0.78 | Protein 22.4 raw to 31.0 roasted implies about 0.72 | Consistent |

Example arithmetic: 80 g dry rice × 2.7 = 216 g cooked (range 200 to 240 g). 200 g cooked chicken ÷ 0.72 = about 280 g raw.

## 6. The example day, and why it is not a target

Computed with `exampleDayTotals` and a 3 hour meat to dairy interval, one of the possible family settings. The app default is 6 hours (see below). Midpoint kcal (low to high range from the food variability), with protein, carbohydrate, fat, fibre (g) and calcium (mg).

| Day | Meals (kosher category) | kcal | P / C / F | Fibre | Calcium |
| --- | --- | --- | --- | --- | --- |
| Sunday | Breakfast (dairy), school snack, school lunch, afternoon chicken and rice (meat), salmon dinner, evening milk (dairy, 5 h 25 min after meat) | 2,862 (2,706 to 3,048) | 209 / 316 / 90 | 53 | 1,672 |
| Monday | Same, beef dinner (meat), evening pareve snack instead of milk | 2,910 (2,748 to 3,104) | 213 / 331 / 90 | 60 | 1,376 |
| Tuesday | White fish dinner, evening milk | 2,701 (2,560 to 2,874) | 215 / 316 / 71 | 53 | 1,675 |
| Wednesday | As Sunday | 2,862 | 209 / 316 / 90 | 53 | 1,672 |
| Thursday | As Monday | 2,910 | 213 / 331 / 90 | 60 | 1,376 |
| Friday | Turkey dinner (meat), no evening snack before the Sabbath | 2,606 (2,464 to 2,779) | 214 / 302 / 66 | 53 | 1,306 |
| Saturday | Sabbath plate guide, eaten to appetite | not summed | | | |

With the default 6 hour interval the evening milk becomes the pareve snack every day (Sunday 2,921 kcal, calcium about 1,380 mg). With a 1 hour interval the milk stays on every day.

**Why these sums are not targets.** They are what one reasonable set of portions adds up to. For comparison, the 2023 National Academies energy equations for boys aged 3 to 18 (coefficients confirmed by two search snippets, not read in the report) give, for an illustrative boy aged 15, 175 cm, 65 kg:

- Low active: 19.12 + 3.68 × 15 + 8.62 × 175 + 20.28 × 65 + 20 = about 2,920 kcal
- Active: −388.19 + 3.68 × 15 + 12.66 × 175 + 20.46 × 65 + 20 = about 3,230 kcal
- Very active: −671.75 + 3.68 × 15 + 15.38 × 175 + 23.25 × 65 + 20 = about 3,610 kcal

These are population equations with individual errors of hundreds of kcal, they rise with height and weight, and training days add more. So the app says teen athletes often need more than the examples and points to a pediatric sports dietitian for a personal number. The examples include options for more food at each meal.

Calcium: the recommended intake for ages 14 to 18 is 1,300 mg a day (IOM 2011, via an NIH fact sheet snippet). Every example day reaches it, Friday only just.

Protein: the example days give more protein than adolescent studies cited by Sports Dietitians Australia found sufficient (about 1.35 to 1.6 g per kg a day, snippet). The app shows no protein target; protein is spread over four or more meals.

## 7. Green beans: arithmetic for a large daily portion

USDA SR28 rows read from the data file through a mirror. Each 500 g value is the per 100 g value × 5. The private plan export shows the same arithmetic for the amount the athlete actually eats.

| State | SR28 row | Per 100 g: kcal / P / C / F / fibre / sodium mg | Per 500 g: kcal / P / C / fibre / sodium mg |
| --- | --- | --- | --- |
| Raw, trimmed | 11052 (FDC 169961, via a third party page) | 31 / 1.83 / 6.97 / 0.22 / 2.7 / 6 | 155 / 9.2 / 34.9 / 13.5 / 30 |
| Boiled, drained, no salt | 11053 (FDC ID not found) | 35 / 1.89 / 7.88 / 0.28 / 3.2 / 1 | 175 / 9.5 / 39.4 / 16.0 / 5 |
| Frozen, boiled, drained | 11061 (FDC 169963, snippet) | 28 / 1.49 / 6.45 / 0.17 / 3.0 / 1 | 140 / 7.5 / 32.3 / 15.0 / 5 |
| Canned, regular, drained | 11056 (FDC 169143, via a third party page) | 22 / 1.12 / 4.32 / 0.46 / 1.9 / 230 | 110 / 5.6 / 21.6 / 9.5 / 1,150 |
| Canned, no salt added, drained | 11729 | 22 / 1.12 / 4.32 / 0.46 / 1.9 / 2 | 110 / 5.6 / 21.6 / 9.5 / 10 |

- Carbohydrate is "by difference" and includes the fibre.
- Raw beans as bought include about 12 percent ends and strings, so 500 g bought is about 440 g eaten.
- Oil changes the total more than the state does: 1 teaspoon of olive oil (4.5 g) is about 40 kcal and 1 tablespoon (13.5 g) about 119 kcal. In the app, oil is a separate field.
- **Fibre:** the adequate intake for boys 14 to 18 is 38 g a day (secondary sources, not the IOM report). A large bean portion supplies a big share. The app shows fibre without a ceiling.
- **Scale effect:** a large portion of beans is mostly water and adds its own weight to a morning reading until it passes. This is why the app reads weekly trends, not single days.
- **Gut comfort:** unverified. Green beans are, from memory, low FODMAP only at a small serving; very large daily portions may cause gas or bloating, especially after a sudden increase. Check with the Monash app or a dietitian.
- **Sodium:** regular canned beans carry a lot of sodium at large portions; no salt added cans carry almost none.
- What the app does: asks the usual amount, the state (raw, boiled, frozen, canned), and the oil, and shows the arithmetic. It never tells the athlete to eat fewer vegetables, and it never counts vegetables as a substitute for meals.

## 8. Meat, dairy, and pareve

| Example | Category | Notes |
| --- | --- | --- |
| Breakfast (yogurt, oats, fruit) | Dairy | Whey, if used, is dairy too |
| School snack (apple, almonds) | Pareve | |
| School lunch (eggs, tofu, salad, olives) | Pareve | Cottage cheese as a swap makes it dairy |
| Afternoon chicken and rice | Meat | Tuna or tofu swaps are pareve |
| Salmon and white fish dinners | Pareve (fish) | Many families do not eat fish together with meat; that is a family setting |
| Beef and turkey dinners | Meat | |
| Evening milk | Dairy | Replaced by the pareve snack when it would come too soon after meat |
| Evening pareve snack (apple, almonds) | Pareve | |
| Sabbath plate guide | Meat | Dessert after it should be pareve |

The interval is the family's decision; the app starts at 6 hours until it is set. The app takes no halachic position; customs differ (about 1, 3, 5 to 5.5, or 6 hours, from general knowledge, unverified). Dairy before meat is not checked.

## 9. Storage

| Item | Guidance in 3.0 |
| --- | --- |
| School lunch | Cafeteria food needs nothing from home. Food from home: insulated bag and two ice packs; no more than two hours warm, one hour above 32°C |
| Chicken and rice boxes | Label by day. Keep the next day or two in the fridge, freeze the rest as soon as cooled. Cooked rice: eat soon or freeze, reheat once |
| Beef bowls | Monday in the fridge, Thursday frozen |
| Turkey plate | Frozen, moved to the fridge on Thursday night |
| Soup | Three servings in the fridge, the rest frozen |
| Overnight oats | Up to two days in the fridge |
| Everything cooked | Refrigerate or freeze within two hours |

These rules are general food safety guidance from memory (FSIS, UK FSA, NHS), not re-read this session.

## 10. What needs a professional, and what is unverified

**Needs a pediatrician or pediatric sports dietitian, with a parent:**
- A personal energy range, especially when a body composition aspiration is recorded.
- Whether a body fat aspiration is appropriate at all at this age, and at what pace. The AAP gives about 0.45 kg (1 lb) a week as the upper rate of loss for a growing athlete (snippet).
- Any supplement already recorded, such as creatine: product, dose, third party testing, and whether to continue. The app records it and does not advise a dose.
- Calcium and vitamin D if dairy is limited on meat days.
- Gut symptoms from large vegetable portions.

**Unverified (not searched or not read):** food safety times and temperatures; kosher customs and the status of whey, creatine, and capsules; FODMAP content of green beans at large portions; the AAP 2016 paper on preventing obesity and eating disorders; the 20 kcal growth term in the energy equations; FDC IDs marked as unverified above; values for tahini sauce, schnitzel, shawarma, and the sweet portion; almond and apple values were taken from the FDC IDs shown but not re-checked this session.
