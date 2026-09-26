# Signal 26 Theme Recommendation: Price the Moment, Not the Average — An IPL Win-Probability Engine for a ₹48,390-Crore League

**Pick Theme 1, "The Hidden Scoreboard", and frame it as a pricing problem for IPL franchises. The question: which IPL batters' averages hide how much they actually swing matches, and what does that mispricing cost at auction?** Build it on a single-file, Cricsheet-derived IPL ball-by-ball CSV (2008–2025) inside Anthrena Desk. Of the five themes, this one has the largest money at stake that you can document, the cleanest open-licensed data, the strongest India and Bengaluru hook, and a named, reproducible metric that fits the brief.

## TL;DR
- **Theme and problem:** Theme 1 (cricket/IPL). Business question: *"Traditional batting average and strike rate ignore match situation. How much win probability does each IPL batter actually add, and which players does the auction market mis-price because of it?"* Your named metric is the **Match Swing Index (MSI)**: win-probability points added per 100 balls, built from an empirical chase win-probability table you construct inside Anthrena.
- **Why it wins:** IPL media rights for 2023–27 sold for ₹48,390 crore across 410 matches. Gulf News put that at ₹1,180.2 million (about ₹118 crore) per match, or about ₹49 lakh per ball. Franchises spent ₹639.15 crore on 182 players at the 2025 mega auction. Yet the peer-reviewed literature still says traditional averages "fail to capture a player's comprehensive contribution," and the closest unified impact systems are proprietary. Other teams will chart runs and wickets. You will show the *decision* that costs franchises money.
- **Dataset:** Kaggle "IPL Dataset" by chaitu20 (IPL.csv: one file, ~295,732 deliveries × 64 columns, 2008–2025, derived from Cricsheet).\[1\] Credit Cricsheet (Stephen Rushe) under the Open Data Commons Attribution License 1.0.\[2\] Primary source and 2026 cross-check: Cricsheet's IPL download (1,243 matches, 2008–2026).\[3\] Fallback within the same theme: the Ergast-derived Kaggle Formula 1 World Championship (1950–2024) dataset.\[4\]

## Key Findings

### 1. The five themes, ranked by business stakes × 24-hour feasibility

| Theme | Real business problem (who loses money) | Stakes (sourced) | Why still hard | Feasibility (24h, Anthrena-only) |
|---|---|---|---|---|
| **1. Hidden Scoreboard (IPL)** | Franchises overpay for reputation and average and underpay for match-swinging contribution. Broadcasters and fantasy platforms need credible in-game win probability. | IPL business value US$18.5B and brand value US$3.9B (Houlihan Lokey 2025).\[5\] Media rights ₹48,390 crore for 2023–27.\[6\] 2025 mega auction ₹639.15 crore.\[7\] 2026 mini-auction: Cameron Green ₹25.20 crore\[8\] | Context (phase, wickets, target, venue, era) swamps raw averages. Samples are small. The best impact models are proprietary | **High.** One CSV, ODC-BY licence, India relevance |
| 2. Four Stars (movies) | Studios and OTT platforms green-light and market titles using aggregate scores that hide polarisation | India M&E ₹2.78 trillion in 2025. Filmed entertainment ₹205 billion from over 1,900 releases (FICCI-EY).\[9\] A Piedmont analysis cited by The Ringer (Sept 2020) found the critic–audience correlation declined "from .77 from mid-2012 to the end of 2016 to .61 from the beginning of 2017 to March 2020 (a drop of 21 percent)" | Review-bombing, selection effects in who rates, scraped data | **Medium-High.** Single file available, but the licence is grey (scraped from Rotten Tomatoes) |
| 3. Playlist (music) | Streaming platforms need to separate stable taste from bursts for recommendations and churn | Indian audio streaming reached 178 million users, 92% on free tiers (FICCI-EY 2026)\[10\] | Needs personal longitudinal data, which the team does not have | **Low.** No personal export; the public track-level sets don't answer "your" history |
| 4. Loudest (communities) | Brands and PR teams must separate real consensus from vocal minorities and catch trends early | Social listening market US$9.2B (2024) → US$20.2B (2030) (Grand View Research).\[11\] The SI Lab's State of Social Listening 2025 found "64.6% of social listening professionals cite API restrictions and platform changes as their #1 challenge" | Platform API lockdown (the very reason your data is hard to get), bots, text-heavy analysis that Anthrena doesn't do natively | **Low-Medium.** Available CSVs are old and text-heavy |
| 5. Cracking the Algorithm (YouTube) | Creators and MCNs gamble production budgets on what trends | YouTube CEO Neal Mohan at WAVES 2025: "In the last 3 years alone, we've paid more than INR 21,000 Crores to creators, artists, and media companies across India." Indian digital ad spend ₹94,700 crore (63% of all ads) in 2025\[10\] | Selection bias (trending-only data), with the ranking algorithm hidden behind it | **Medium.** A labelled trending/non-trending set exists but its provenance is thin |

**Verdict:** Theme 1 is the only option where (a) the money is concrete and India-specific, (b) the data is open-licensed and ball-level, (c) your ML background shows naturally (win-probability modelling, confounders, causal era adjustment), and (d) the brief's "name one player/moment with a reproducible metric" maps exactly onto a win-probability worm.

### 2. The business problem behind Theme 1, grounded

- **Money per decision is enormous.** The 2023–27 media-rights cycle is worth ₹48,390.32 crore, nearly 3x the previous cycle's ₹16,347.5 crore, across 410 matches. Gulf News valued each game at ₹1,180.2 million (about ₹118 crore), or about ₹49 lakh per ball. BCCI secretary Jay Shah said the deal made the IPL "the 2nd most valued sporting league in the world in terms of per match value." Disney Star paid ₹23,575 crore for TV and Viacom18 paid ₹23,758 crore for digital, the first time digital outbid TV in Indian sport.\[12\]
- **Talent spending is priced on reputation.** Franchises spent a record ₹639.15 crore on 182 players (62 overseas) at the 2025 mega auction in Jeddah. Rishabh Pant went for ₹27 crore and Shreyas Iyer for ₹26.75 crore.\[13\]\[14\] At the December 2025 mini-auction in Abu Dhabi, KKR paid ₹25.20 crore for Cameron Green, but his salary is capped at ₹18 crore under the new overseas-player rules.\[15\]\[16\] CSK paid ₹14.2 crore each for two uncapped Indians, Prashant Veer and Kartik Sharma.\[17\] When a franchise pays ₹14 crore for an uncapped player, the auction clearly runs on projection under uncertainty, which is exactly where a better metric pays off.
- **The franchise asset base depends on winning.** According to Houlihan Lokey's 2025 IPL Brand Valuation Study (8 July 2025), RCB "replaced Chennai Super Kings to secure No. 1 in both brand and business value rankings, with a staggering brand value of US$269.0 million" after its first title in 2025. Your judges are in Bengaluru, and that is a ready-made hook.
- **Academia agrees the scoreboard lies.** A 2025 systematic review (Chathurangi et al., *International Journal of Sports Science & Coaching*) states that traditional metrics "often fail to capture a player's comprehensive contribution to the game."\[18\] Lemmer (2011, *Journal of Sports Science and Medicine*) showed on IPL 2009 data that "the traditional average is not the most appropriate measure to compare batsmen's performances after conclusion of a short series."\[19\]
- **Why it is still unsolved:** A 2026 arXiv paper, "Context-adjusted Player Evaluation for Twenty20 Cricket" (arXiv:2608.18020), notes that the cricket literature "evaluates players through simulators or opaque models that are hard to reproduce… and the systems that come closest to a unified impact measure are proprietary." It then concedes that its own "REGULUS platform and its constituent metrics are proprietary at this point." A transparent, reproducible impact metric is therefore a real gap, not a student exercise.
- **A confounder almost nobody controls for:** the 2023 Impact Player rule. In "The Impact Player Paradox" (Columbia, 2026), Vishal Misra used 2,355 IPL innings from ESPNcricinfo data and a synthetic control built from five other T20 leagues. He finds "the treatment effect is +12.3 runs per innings (RSC) and +11.2 runs (mRSC)" above global trends, while the raw before/after jump is +25 runs. Averages went from 155.9 runs per innings (2008–22) to 179.6 (2023–26). Toss-winner win rate stayed at 51.8% in both eras, and overs bowled by top-order batters fell 38%. Comparing strike rates across eras without adjustment is therefore wrong, and saying so is your "Google data scientist" moment.

## The Recommendation (lock this at 12:00 PM)

**Theme:** 1, The Hidden Scoreboard (Cricket / IPL).

**Problem statement (business-owned):**
> *"IPL franchises allocate over ₹600 crore per mega auction using batting average and strike rate, statistics that ignore match situation. We build a transparent win-probability engine from 2008–2025 ball-by-ball data and a Match Swing Index (MSI) that measures how many win-probability points each batter adds per 100 balls. We then show which players the market over- and under-values, and recommend how a franchise analytics team should re-rank its auction shortlist."*

**Dataset (primary):** "IPL Dataset" (IPL.csv) by chaitu20 on Kaggle — https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025. One CSV, about 295,732 rows × 64 columns (row count from third-party README, confirm on import), seasons 2008–2025, over 100 MB.\[20\] Key fields: match_id, date, season, batting_team, bowling_team, batter, bowler, over (0-indexed), ball, runs_batter, runs_total, bowler_wicket, wicket_kind, valid_ball, venue, city, toss_decision, match_won_by.\[1\] Built from Cricsheet data.\[21\] **Licence:** the Kaggle licence field could not be verified remotely, so check it on the page before the mentor meeting. Because the data comes from Cricsheet, credit it as *"Data: Cricsheet (cricsheet.org), Stephen Rushe, Open Data Commons Attribution License 1.0."*

**Dataset (source of truth / cross-check):** Cricsheet IPL match data — https://cricsheet.org/downloads/. 1,243 IPL matches covering 2008–2026 (latest match added 17 Sept 2026).\[3\] The "Ashwin" CSV format has two files per match: `<id>.csv` (26 columns: match_id, season, start_date, venue, innings, ball, batting_team, bowling_team, striker, non_striker, bowler, runs_off_bat, extras, wides, noballs, byes, legbyes, penalty, wicket_type, player_dismissed and others) and `<id>_info.csv` (winner, toss, target_runs, method such as D/L).\[22\] Licence: Open Data Commons Attribution License 1.0.\[22\]\[23\] The one-file-per-match layout makes it unsuitable as your main Anthrena import. Use it only to cross-check a hero match.

**Optional small companion file (manually compiled, fully public):** a 25–40 row CSV of auction prices for the players you analyse (player, team, 2025 auction price in ₹ crore, retained or bought), taken from the official IPLT20 2025 auction page and Business Standard's sold-player list. Joining it with XLOOKUP is trivial, and it turns "interesting cricket stat" into "₹ mispricing."

**"Why we chose this theme" pitch (say this to the judges):**
> *"Every ball of the IPL is worth roughly ₹49 lakh in media rights, and franchises spent ₹639 crore at the last mega auction. Those decisions still lean on the batting average, a number that treats a dead-rubber 40 the same as a title-deciding 40. We picked the problem where a better metric has the most direct rupee value. We built a transparent win-probability engine and a Match Swing Index, and we corrected for the Impact Player rule, which inflated scoring by +12.3 runs per innings (Robust Synthetic Control), per Misra's 'The Impact Player Paradox' (2026)."*

## Details: 20-Hour Analysis Plan inside Anthrena Desk

### A. Cleaning (Milestone 1–2 evidence; show every step on the Data page)
| Required cleaning | What to do on this dataset |
|---|---|
| **Missing values** | Check city, venue, wicket_kind (blank on non-wicket balls, which is structural and should be recoded as "none") and match_won_by (no-result or abandoned matches, which you exclude). Report counts before and after. |
| **Duplicates** | Wides and no-balls legitimately repeat the same over.ball number, so a naive "remove duplicates" would delete real deliveries. Deduplicate on match_id + innings + over + ball + a delivery sequence, and count legal balls only via valid_ball. This is a strong "we thought about it" talking point. |
| **Data types** | Convert date to a date, season to a number (some sources store "2007/08" or "2020/21"), and over and ball to integers. Make sure the runs columns are numeric. |
| **Inconsistent labels** | Unify franchise renames: Delhi Daredevils→Delhi Capitals, Kings XI Punjab→Punjab Kings, Royal Challengers Bangalore→Bengaluru, Deccan Chargers kept separate from SRH, and Rising Pune Supergiant/Supergiants merged.\[24\] Also unify venue spelling variants (e.g., "M Chinnaswamy Stadium" vs "M.Chinnaswamy Stadium, Bengaluru"). Build a small mapping table and apply it with XLOOKUP. |
| **Outliers** | Flag super-over innings (innings > 2), rain-reduced and D/L matches (a target that isn't first-innings total + 1), and extreme totals such as 250+ in the impact era. Keep them but flag them, and use Anthrena outlier detection to justify it. |

### B. Derived columns
1. `phase` = Powerplay (over 0–5), Middle (6–14), Death (15–19).
2. `legal_ball_no` = running count of valid balls within the innings. `balls_left` = 120 − legal_ball_no.
3. `wkts_in_hand` = 10 − cumulative wickets in the innings.
4. `first_inn_total` for each match via SUMIFS, then `target` = first_inn_total + 1 (exclude D/L matches) and `runs_required` = target − cumulative runs in the chase.
5. `rrr` = runs_required ÷ (balls_left/6). `era` = "Pre-Impact (2008–22)" or "Impact (2023–25)".
6. `chase_won` = 1 if batting_team = match_won_by (second innings).
7. **State buckets:** balls_left in bands of 12 (two overs), runs_required in bands of 10, and wkts_in_hand grouped as 0–2, 3–5, 6–7, 8–10.

### C. The named, reproducible metric: Match Swing Index (MSI)
- **Step 1, win-probability table:** From all 2008–2025 second-innings deliveries, compute the empirical chase-win rate for each (balls_left band × runs_required band × wickets band) state using a pivot or matrix. Enforce a minimum sample of about 30 balls per cell and merge sparse cells. This is your transparent WP model, reproducible by anyone with the same CSV.
- **Step 2, ML cross-check (credibility):** Use Anthrena's Pro random forest predict with features balls_left, runs_required, wkts_in_hand, rrr, era and venue to predict chase_won. Report feature importance (you should expect rrr and wickets to dominate) and show that the random forest and the lookup table broadly agree. That agreement is a validation step, which judges reward.
- **Step 3, WPA per ball:** WP_after − WP_before, credited to the striker (and the negative to the bowler).\[25\]
- **Step 4, MSI** = Σ WPA ÷ balls faced × 100 for the player, era-split, with a minimum of 300 balls faced in chases. Pair it with a first-innings companion, **Runs Above Par** = runs scored − expected runs for the same (over, wickets-fallen) state and era, so you cover both innings.

### D. Hypotheses and tests
| Hypothesis | Test in Anthrena |
|---|---|
| H1: Batting average is a weak proxy for match impact | Spearman rank correlation between batting-average rank and MSI rank (a ρ well below 1 is the headline) |
| H2: Scoring context shifted after 2023 | Mann-Whitney or t-test on innings totals and death-over strike rate, pre vs impact era. Compare your estimate with Misra's +12.3 runs per innings synthetic-control result and explain why a raw before/after overstates it\[26\] |
| H3: The toss did not become decisive in the impact era | Chi-square test, toss-winner × match-winner × era (Misra reports 51.8% in both eras, so try to replicate it)\[26\] |
| H4: Phase and wickets, not venue, drive chase WP | OLS regression via AX.REGRESSION of chase_won on rrr, wkts_in_hand, balls_left and a venue dummy (a linear probability model, interpreted with care), plus random forest feature importance |
| H5: Auction price tracks reputation more than MSI | Spearman between 2025 auction price and MSI across your 25–40 player companion table. Label it exploratory because n is small |
| Segmentation (optional) | k-means on player profiles (MSI, Runs Above Par, phase strike rates, dismissal rate) to name archetypes such as "Anchor," "Finisher," and "Empty-calorie accumulator" |

### E. Six-to-eight-page storyline (presentation mode)
| Page | Purpose | Anthrena visuals |
|---|---|---|
| 1. The ₹49-lakh ball | Problem and stakes | KPI cards (₹48,390 cr media rights, ₹639.15 cr auction, US$18.5B IPL value), one-sentence problem statement |
| 2. Data & cleaning | Trust | Funnel or waterfall of rows (raw → deduped → legal balls → analysable chases), a table of cleaning actions, a source and licence callout |
| 3. The scoreboard lies | Obvious metric vs truth | Scatter of batting average vs MSI with quadrant annotations, a ribbon chart of rank change (average rank → MSI rank) |
| 4. The confounder | Era adjustment | Line chart of average innings total by season with a 2023 annotation, and box plots of innings totals by era |
| 5. The win-probability engine | Method | Heatmap of chase-win % (balls_left × runs_required, filtered by wickets via slider), random forest feature-importance bar chart |
| 6. Hero moment | The one named story | Line chart WP worm of the **IPL 2025 final (RCB vs PBKS)**, with callouts on the single biggest-swing over and player, plus a waterfall of WPA by over |
| 7. The mispricing | Business impact | Bubble chart of 2025 auction price vs MSI (bubble = balls faced), a "value per crore" ranking table, a radar comparing two similar-price players |
| 8. Recommendation & sources | Decision | Three recommendations, limitations, full dataset credits and licences |

**Hero-moment rule:** Don't pre-decide the player. Let the data name them, as either (a) the biggest single-over WPA swing in the 2025 final (RCB is the home franchise of your judges) or (b) the player with the largest gap between batting-average rank and MSI rank. Present it as: "Player X averages Y, which ranks N. By MSI they rank M, because Z% of their runs came when chase WP was already below 20% or above 90%."

### F. Recommendations to put on page 8
1. Franchise analytics teams should re-rank auction shortlists by era-adjusted MSI per crore, not by average.
2. Evaluate batters against the state they walked in to (balls left, wickets, required rate), not against league-wide strike rate.
3. Treat pre-2023 and post-2023 numbers as different currencies. Any scouting model that doesn't adjust for the Impact Player rule overrates recent batters.

### G. Hour-by-hour plan (two people)
- **Hours 0–3:** Import, cleaning, label mapping (Person A). Draft the problem slide and source slide (Person B).
- **Hours 3–8:** Derived columns and the WP state table (A). Descriptive era analysis and H2/H3 tests (B).
- **Hours 8–12:** WPA and MSI (A). Random forest, feature importance, regression (B). **Checkpoint:** if MSI doesn't work by hour 12, fall back to Runs Above Par alone, which needs no second-innings target.
- **Hours 12–17:** Hero-match worm, auction companion table, bubble and ribbon charts.
- **Hours 17–20:** Dashboard polish, cross-filters, slider, annotations, presentation-mode rehearsal.

## Differentiators: What Other Teams Will Do vs. You

| Typical student team | Your team (industry framing) |
|---|---|
| "Top 10 run scorers," "Kohli vs Rohit," toss-win pie chart | A decision metric (MSI) tied to a ₹ decision (auction) |
| Compare raw strike rates across 2008–2025 | Adjust for the Impact Player regime shift (+12.3 runs per innings, causal estimate) and explain why raw before/after overstates it\[26\] |
| Correlation = insight | Name the confounders (phase, wickets, target, venue, era) and condition on them via the state table |
| One model, no validation | A transparent lookup-table WP model cross-validated against a random forest |
| Name a famous player | Name a specific ball or over and a player whose average contradicts their swing value, with reproducible steps |
| Generic "more data needed" | Size the impact: "value per crore" and a re-ranked shortlist |

## Datasets for the Other Themes (for the judges' "why not X?" question)

| Theme | Dataset | Publisher/URL | Format and size | Licence | Pitfalls |
|---|---|---|---|---|---|
| 1 (fallback: F1) | Formula 1 World Championship (1950–2024) | rohanrao, Kaggle: https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020 | 14 CSVs (races, results, lap_times, pit_stops, qualifying, drivers, constructors, etc.) | Ergast data, published to the public domain by Chris Newell (per the related jtrotman dataset).\[27\] Kaggle licence unverified | Many joins. Lap times only from 1996.\[28\] Car-vs-driver separation needs teammate comparisons |
| 1 (alt) | IPL Complete Dataset (2008–2024) | patrickb1912, Kaggle | matches.csv (1,095 matches) + deliveries.csv (~260,000 rows) |\[24\] Unverified on Kaggle, credit Cricsheet | Two files need a join. No 2025 |
| 2 | Rotten Tomatoes movies and critic reviews | stefanoleone992, Kaggle | Two CSVs (17k+ movies; critic reviews), scraped 2020-10-31\[29\]\[30\] | Scraped, so the licence is unclear. Flag it | Stale. Audience score definition changed. Review-bombing |
| 2 | Massive Rotten Tomatoes Movies & Reviews | andrezaza, Kaggle | rotten_tomatoes_movies.csv (audienceScore, tomatoMeter, genre, runtime, boxOffice) + reviews CSV\[31\] | Scraped, licence unclear | Heavy missingness in boxOffice |
| 3 | No suitable public personal listening history | — | — | — | Personal Spotify export takes days. Aggregate track datasets don't answer "your" history |
| 4 | 1 million Reddit comments from 40 subreddits | smagnan, Kaggle | 25,000 anonymised comments per subreddit\[32\] | Reddit content, licence unclear | Text-heavy. Temporal momentum is hard to analyse in Anthrena |
| 5 | YouTube Video Trends & Non-Trends | muhammedchreiki, Kaggle (US, labelled, 2025)\[33\] | CSV, row count unverified | Unverified | How "non-trending" videos were sampled is undocumented, so the control group may itself be biased |
| 5 | YouTube Trending Video Dataset (updated daily) | rsrishav, Kaggle (includes India file)\[34\] | Per-country CSVs | Unverified | Trending-only, so it reproduces the selection bias you were warned about |

## Caveats and Risks

- **Kaggle licences and row counts:** The chaitu20 row and column counts (295,732 × 64) come from third-party READMEs, and the Kaggle licence field could not be read remotely. Verify both on the dataset page before 12:00. If the licence is missing or restrictive, cite Cricsheet (ODC-BY 1.0) as the underlying source. If you are still uncomfortable, use the patrickb1912 two-file set and do one XLOOKUP join.
- **File size:** Over 100 MB can slow Anthrena. If it lags, filter to 2015–2025 or to second innings only for the WP table, and document the filter on the Data page.
- **No 2026 season in the single-file set:** Cricsheet has 2026, but only as per-match files.\[35\] Say this openly and use 2026 only as a stretch validation.
- **D/L and no-result matches** distort targets, so exclude them from the WP table and state how many you removed.
- **Sparse WP cells:** Late-chase states with few observations produce noisy probabilities. Merge bands and show the minimum-n rule.
- **Auction-price correlation (H5) is exploratory.** With 25–40 players it is under-powered, and prices also reflect role scarcity, captaincy and marketing value. Present it as "directional" and don't claim causality.
- **Market-size figures conflict:** 2025 sports-analytics market estimates range from US$1.72B (Research and Markets) to US$2.29B (MarketsandMarkets) to US$5.7–5.79B (Grand View, Fortune Business Insights).\[36\]\[37\]\[38\]\[39\] Don't put a single sports-analytics market number on slide 1. Use the IPL-specific figures (media rights, auction, Houlihan Lokey), which are far better sourced.
- **Backup plan:** If the IPL file fails to import or the target calculation breaks, stay in Theme 1 and switch to the F1 Ergast dataset. Problem: "isolating driver pace from car advantage via teammate qualifying gaps" (qualifying.csv + races.csv + drivers.csv, two joins). If you must change theme, go to Theme 2 with the andrezaza Rotten Tomatoes file ("which genre and runtime profiles produce the widest critic–audience split"), and flag the scraped-data licence risk on the sources page.

## Sources

1. [GitHub - HemangiGadhavi/IPL-Data-Analytics-Dashboard: Interactive IPL Data Analytics Dashboard built with Python, Pandas, Streamlit & Plotly. Analyze batting, bowling, teams, venues, toss impact, season trends, and over-wise scoring using ball-by-ball IPL data from 2008–2025.](https://github.com/HemangiGadhavi/IPL-Data-Analytics-Dashboard)
2. [Cricsheet Register - Cricsheet](https://cricsheet.org/register/)
3. [Match data - Cricsheet](https://cricsheet.org/matches/)
4. [Formula 1 World Championship (1950 - 2024)](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020)
5. [Houlihan Lokey Launches IPL Valuation Study 2025 - Passionate In Marketing Houlihan Lokey Launches IPL Valuation Study 2025](https://www.passionateinmarketing.com/houlihan-lokey-launches-ipl-valuation-study-2025/)
6. [IPL Media Rights: BCCI will earn WHOPPING Rs 2.95 crores from EACH OVER bowled in league from 2023 to 2027 | Cricket News | Zee News](https://zeenews.india.com/cricket/ipl-media-rights-bcci-will-earn-whopping-rs-2-95-crores-from-each-over-bowled-in-league-from-2023-to-2027-2474128.html/amp)
7. [IPL 2025 Auction | Live Updates & Overview | IPLT20](https://www.iplt20.com/auction/2025)
8. [IPL auction 2026 - KKR buy Cameron Green for INR 25.20 crore, most expensive overseas player ever | Cricinfo](https://www.cricinfo.com/story/kkr-buy-cameron-green-for-inr-25-20-crore-at-ipl-2026-auction-1515809)
9. [India’s M&E Sector hits Rs 2.78 Trillion mark in 2025, eyes Rs 3.3 trillion by 2028: FICCI-EY](https://beyondbollywood.home.blog/2026/03/24/indias-me-sector-hits-rs-2-78-trillion-mark-in-2025-eyes-rs-3-3-trillion-by-2028-ficci-ey/)
10. [Digital media hits ₹1,00,000 crore, ad revenues surge to ₹94,700 crore: FICCI-EY report - Storyboard18](https://www.storyboard18.com/advertising/digital-media-hits-%E2%82%B9100000-crore-ad-revenues-surge-to-%E2%82%B994700-crore-ficci-ey-report-92987.htm)
11. [Social Media Listening Market Size, Share Report 2025-2030](https://www.grandviewresearch.com/industry-analysis/social-media-listening-market-report)
12. [IPL Broadcasting Rights: ₹48,390 Crore Deal, Digital Beats TV First Time](https://arthnova.com/ipl-broadcasting-rights-48390-crore-disney-viacom18/)
13. [IPL 2025 mega auction: Full list of players sold, teamwise players' salary | IPL 2024 News - Business Standard](https://www.business-standard.com/cricket/ipl/ipl-2025-mega-auction-full-list-of-players-sold-teamwise-players-salary-124112600201_1.html)
14. [IPL 2025 mega auction: Money spent, whopping deals, and more](https://www.newsbytesapp.com/news/sports/major-numbers-from-ipl-2025-mega-auction/story)
15. [List of 2026 Indian Premier League personnel changes](https://en.wikipedia.org/wiki/List_of_2026_Indian_Premier_League_personnel_changes)
16. [IPL 2026 player list - all teams' squads - Olympics.com](https://www.olympics.com/en/news/ipl-2026-teams-squads-list-player-prices)
17. [kkr buy cameron green inr 2520 crore ipl 2026 auction](https://africa.espn.com/cricket/story/_/id/47322426/kkr-buy-cameron-green-inr-2520-crore-ipl-2026-auction)
18. [Impact ranking methodologies in limited-overs cricket: A systematic review of performance metrics - A.K.D.K. Chathurangi, R. M. Silva, N. Withanage, C. L. Jayasinghe, 2025](https://doi.org/10.1177/17479541251321477)
19. [The single match approach to strike rate adjustments in batting performance measures in cricket - Document - Gale Academic OneFile](https://go.gale.com/ps/i.do?id=GALE%7CA274114820&issn=13032968&it=r&linkaccess=abs&p=AONE&sid=googleScholar&sw=w&userGroupName=anon%7E70a64a05&v=2.1)
20. [GitHub - poonamjundre725-dotcom/ibm-bob-project: IPL Cricket Data Analytics Dashboard — End-to-End Data Analytics Project using Python, Pandas, Plotly & Streamlit](https://github.com/poonamjundre725-dotcom/ibm-bob-project)
21. [IPL Dataset](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025)
22. [Cricsheet "Ashwin" CSV format](https://cricsheet.org/format/csv_ashwin/)
23. [How to download and process Cricsheet data (ball-by-ball, CSV, DuckDB) | TIGZIG](https://www.tigzig.com/agents-faq/how-to-download-and-process-cricsheet-data)
24. [GitHub - ankritbaidya/IPL-Cricket-Analytics: IPL Cricket Performance & Strategy Analytics using Python,SQL and Power BI](https://github.com/ankritbaidya/IPL-Cricket-Analytics)
25. [Win probability added](https://en.wikipedia.org/wiki/Win_probability_added)
26. <https://www.cs.columbia.edu/~misra/impact-player-2026.pdf>
27. [Formula 1 Race Data](https://www.kaggle.com/datasets/jtrotman/formula-1-race-data)
28. [archive.linux.duke.edu](https://archive.linux.duke.edu/cran/web/packages/f1dataR/readme/README.html)
29. [Rotten Tomatoes movies and critic reviews dataset](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset)
30. [Rotten Tomatoes movies and critic reviews dataset | Kaggle](https://www.kaggle.com/datasets/stefanoleone992/rotten-tomatoes-movies-and-critic-reviews-dataset/code)
31. [🎬 Massive Rotten Tomatoes Movies & Reviews](https://www.kaggle.com/datasets/andrezaza/clapper-massive-rotten-tomatoes-movies-and-reviews)
32. [1 million Reddit comments from 40 subreddits | Kaggle](https://www.kaggle.com/datasets/smagnan/1-million-reddit-comments-from-40-subreddits)
33. [YouTube Video Trends & Non-Trends Dataset](https://www.kaggle.com/datasets/muhammedchreiki/youtube-video-trends-and-non-trends-dataset)
34. [YouTube Trending Video Dataset (updated daily) | Kaggle](https://www.kaggle.com/datasets/rsrishav/youtube-trending-video-dataset/data?select=US_youtube_trending_data.csv)
35. [2026 Indian Premier League](https://en.wikipedia.org/wiki/2026_Indian_Premier_League)
36. [Sports Analytics Market Report 2025-2030, by Application, Geo, Tech](https://www.marketsandmarkets.com/Market-Reports/sports-analytics-market-35276513.html)
37. [Sports Analytics Market Size, Competitors & Forecast to 2034](https://www.researchandmarkets.com/report/sports-analytics)
38. [Sports Analytics Market Size, Share, Global Growth Report, 2034](https://www.fortunebusinessinsights.com/sports-analytics-market-102217)
39. [Sports Analytics Market Size And Share Report, 2026-2033](https://www.grandviewresearch.com/industry-analysis/sports-analytics-market)
