# Signal 26 · Theme 1 "The Hidden Scoreboard": IPL Data-Collection Dossier and Mentor Q&A Bank

Lock the chaitu20 "IPL Dataset(2008-2025)" single-file IPL.csv as your working dataset, name Cricsheet as the source of truth and licensor (ODC-BY 1.0), and keep patrickb1912 "IPL Complete Dataset (2008-2024)" as the backup. No publicly available dataset we found is clearly better for a CSV-only, one-file, 24-hour Anthrena workflow. The one real gap is that chaitu20's Kaggle licence field could not be verified directly. The fix is to screenshot the licence field when you download and to credit Cricsheet under ODC-BY on the dashboard, which covers you whatever chaitu20 declares.

## TL;DR

- **Dataset decision:** Use the primary file chaitu20 IPL.csv, reported as 295,732 deliveries × 64 columns covering 2008–2025, "compiled and organized from Cricsheet data". It is one CSV, so it imports straight into Anthrena with no format conversion and no multi-file joins before cleaning. The backup is patrickb1912 (2008–2024; matches.csv plus deliveries.csv; cited in Bhatnagar & Bhatnagar, Journal of Quantitative Analysis in Sports 2025;21(3):253–267, doi:10.1515/jqas-2025-0006). The ground truth for spot-checks is Cricsheet's 1,243 IPL matches, for which Cricsheet provides only per-match CSV files, not one combined file.
- **Legal status:** Cricsheet data is published under the Open Data Commons Attribution License (ODC-BY) 1.0, whose only condition is attribution. chaitu20's own Kaggle licence could not be confirmed; one third-party mirror reports "CC0 (Public Domain)". Crediting both Cricsheet (ODC-BY) and the Kaggle uploader makes the use defensible either way.
- **Is there anything better?** Not for this setup. Newer "2008–2026" Kaggle uploads either stop before the 2026 season finished (vedantbhavsar43, last updated about 2 May 2026 against a 31 May final) or mix in manually compiled ESPNcricinfo and IPL-website data with unclear rights (krishd123, maratheabhishek). Cricsheet's own files are the most authoritative, but they come as JSON (which Anthrena can't import) or as roughly 2 × 1,243 per-match CSVs, which you can't merge inside the rules. Show players' names, because the brief requires naming a player and these are public professional records. Hide all registry, match and person IDs.

## Key Findings

1. **Cricsheet is the provenance behind every serious candidate.** It was started in 2009 by Stephen Rushe, who "has written all of the code which extracts and validates the data".\[1\] As of September 2026 it holds 22,983 matches, including 1,243 IPL matches.\[2\] The IPL downloads are 5.2 MB as JSON and 4.6 MB as YAML.\[2\]
2. **Cricsheet's own CSV options are per-match only.** The "Ashwin" CSV format has two files per match, `<id>.csv` (ball-by-ball) and `<id>_info.csv` (match info).\[3\] Cricsheet calls it "probably the most straightforward data format to use",\[4\] but also describes its CSVs as "experimental" and JSON as "the most complete".\[5\] We found no official single combined IPL CSV.
3. **chaitu20 is the most practical legal-looking single file.** It has one file (IPL.csv, 64 columns), a Cricsheet-derived description, a card image dated 6 June 2025 (which suggests the last update included the 2025 final), and about 64.8K views and 18K downloads. The licence field is unverified.\[6\]
4. **The data supports a win-probability (WP) engine.** Confirmed chaitu20 columns include `match_id, date, season, batting_team, bowling_team, batter, bowler, over, ball, runs_batter, runs_total, bowler_wicket, wicket_kind, valid_ball, venue, city, toss_winner, toss_decision, match_won_by, player_of_match, runs_not_boundary`, plus an innings column.\[7\]\[8\] That covers every state variable a WASP-style table needs; the target has to be derived.
5. **The Impact Player rule is the main cross-era confounder.** Vishal Misra (Columbia, 2026 working paper) estimates +12.3 runs per innings attributable to the rule (Robust Synthetic Control), against a raw +25.0, with "no statistically detectable effect on win probability".\[9\] This is a strong argument for a WP-based metric over raw runs.
6. **The business stakes are large and well documented.** IPL media rights for 2023–27 total ₹48,390.32 crore according to the BCCI's official release (ESPNcricinfo reports ₹48,390.5 crore). The 2025 mega auction spent ₹639.15 crore on 182 players.\[10\] Houlihan Lokey's "IPL Valuation Study 2025" values the IPL business at US$18.5 billion (+12.9%), with RCB the top brand at US$269 million.

## Details

### 1. Dataset comparison

| Criterion | chaitu20 "IPL Dataset(2008-2025)" | patrickb1912 "IPL Complete Dataset (2008-2024)" | Cricsheet IPL (direct) | vedantbhavsar43 "IPL 2007 to 2026 Complete Ball-by-Ball" | krishd123 "IPL 2026 – Complete Dataset" | maratheabhishek "IPL Dataset 2008 to 2026" |
|---|---|---|---|---|---|---|
| URL | kaggle.com/datasets/chaitu20/ipl-dataset2008-2025 | kaggle.com/datasets/patrickb1912/ipl-complete-dataset-20082020 | cricsheet.org/downloads/ | kaggle.com/datasets/vedantbhavsar43/ipl-2007-to-2026-complete-ball-by-ball-dataset | kaggle.com/datasets/krishd123/ipl-2026-complete-dataset | kaggle.com/datasets/maratheabhishek/ipl-dataset-2008-to-2025 |
| Provenance | "compiled and organized from Cricsheet data" | Not stated in snippets; widely used in academic work | Primary: Stephen Rushe's extraction and validation | Consistent with Cricsheet (unconfirmed) | "compiled from ESPNcricinfo, IPL official website, and Google… efforts are manual" | Cricsheet JSON "enriched using… ESPN Cricinfo and IPL official stats" |
| Licence | **Unverified on Kaggle**; third-party mirror says "CC0 (Public Domain)" | Unverified; third party says "CC0: Public Domain" (older version) | ODC-BY 1.0 | Not found | Not found; source rights doubtful | Not verified |
| Files | 1 (IPL.csv) | 2 (matches, deliveries) | JSON/YAML zips; CSV per match (two files each) | Not verified | 9 files (deliveries, matches, squads, etc.) | Multiple |
| Size | 295,732 rows × 64 cols (GitHub READMEs) | Not verified | 1,243 matches | 1,212 matches, 288,226 deliveries | 2.37 MB | Not verified |
| Seasons | 2008–2025 (a newer 2026 version is possible, unconfirmed) | 2008–2024 | 2008–2026 (inferred from the match count) | Title says 2007–2026; updated about 2 May 2026, so 2026 is likely incomplete | 2026 only | 2008–2026 (per title) |
| Anthrena fit | Best: single CSV | Good, but needs XLOOKUP joins on about 260K rows | Poor: JSON not importable; thousands of CSVs | Unclear | Rights risk | Rights contamination risk |
| Verdict | **PRIMARY** | **BACKUP** | **Source of truth / spot-check** | Reject | Reject | Reject |

Notes:
- The Kaggle row counts come from third-party GitHub READMEs, and two repos report 295,732 rows against different season ranges (2008–2025 and 2008–2026).\[7\]\[8\] Check the `season` column yourself after downloading.
- patrickb1912's dataset is cited as "Bhardwaj, P. (2024). IPL complete dataset (2008-2024). Kaggle" in Bhatnagar & Bhatnagar's De Gruyter JQAS paper "Analyzing key factors influencing IPL cricket scores using explainability and multimodal data" (JQAS 2025;21(3):253–267, doi:10.1515/jqas-2025-0006), and in an IJCA paper on IPL player performance. That gives it academic credibility as a fallback.
- The "Enhanced Edition" by meruvakodandasuraj claims CC0 but describes its provenance only as "publicly available IPL match records, scorecards, and auction data".\[11\] It is too vague to defend at a legal-rules check.

**Does anything include IPL 2026?** Cricsheet does: its 1,243-match total is consistent with the 74-match 2026 season having been added.\[2\]\[12\] Among Kaggle files, the 2026 candidates are either incomplete or of uncertain rights. Excluding 2026 is defensible and even useful: your auction story is about the 2025 mega auction, and 2026 can be a stated "next step" for out-of-sample validation.

**Known data-quality issues to clean (from Cricsheet's format specification, which chaitu20 inherits):**
- **Over numbering is 0-indexed.** Cricsheet's `ball` value "23.5" means "the 5th ball of the 24th over".\[4\] Expect `over` values of 0–19; add 1 for display.\[7\]
- **Extras repeat ball numbers.** `actual_delivery` "takes into account wides and no-balls, meaning that a delivery after one of those will have the same actual_delivery value as the previous delivery".\[4\]\[13\] Repeated (match, innings, over, ball) keys are therefore *not* duplicates. Deduplicate on the full row, and count balls faced only where `valid_ball = 1`.
- **Blank means zero for extras.** `wides`, `noballs`, `byes`, `legbyes` and `penalty` are blank when there were none,\[4\] so fill them with 0.
- **Super overs** are recorded as extra innings (3 and 4).\[4\] Filter to innings 1–2 for the WP model.
- **Rain-affected matches** carry `method = D/L`, and revised targets appear as `target_runs`/`target_overs`.\[4\] Flag them and exclude them from model fitting.
- **No results and ties** use `outcome` values "no result" and "tie".\[4\] Exclude no-results, and resolve ties through the super-over winner (`eliminator`).
- **Team and venue labels change over time.** Cricsheet keeps names as they were at the time (for example, "Kings XI Punjab" appears in its own examples).\[4\] Build a canonical-name lookup, such as Kings XI Punjab → Punjab Kings and Delhi Daredevils → Delhi Capitals, and a venue lookup that merges variants like "Wankhede Stadium" and "Wankhede Stadium, Mumbai". The specific venue variants in chaitu20 need checking after download.
- **Mixed season labels.** One repo notes that `season` mixes values like "2007/08" and "2023".\[7\] Normalise to the year of the match date.
- **Impact Player substitutes.** Cricsheet's JSON has `replacements`/`supersubs` fields,\[14\] but whether chaitu20 carries a substitute flag is unverified. The ESPNcricinfo 2025-final scorecard records "Impact player: Prabhsimran Singh in, Yuzvendra Chahal out" and "Suyash Sharma in, Mayank Agarwal out".\[15\]
- **DRS for wides and no-balls.** Cricsheet noted in April 2023 that it had to "cope with the IPL allowing reviews for no-balls and wides".\[16\]

**WP-model suitability checklist for chaitu20:**
- Innings: yes.
- Legal-ball flag: `valid_ball`.
- Cumulative score and wickets: derive from `runs_total`, `bowler_wicket` and `wicket_kind`; the description mentions "cumulative statistics", but the exact columns are unverified.
- Target: not confirmed as a column. Derive it as first-innings total + 1, and exclude D/L matches.
- Match winner: `match_won_by`.
- Toss: yes.
- Venue: yes.
- Player of the match: yes.

### 2. Other public sources and why they're only for spot-checks

- **ESPNcricinfo / Statsguru.** We couldn't verify its terms of use in this research. Treat it as read-only for manual verification of a few facts, such as the 2025 final scorecard, and do not scrape it. Its scorecards already show a "Win Probability" feature (the 2025 final page shows "RCB 100%").\[15\] That is a useful "why not just use theirs?" point: it is closed, not reproducible, and doesn't aggregate to a per-player rate.
- **IPLT20.com.** This is the official source for auction totals: "182 players, including 62 overseas… 8 Right To Match, spending INR 639.15 Crore".\[17\] Use it for manually typed facts with citation, not bulk data.
- **The cricketdata R package** (Hyndman et al.) documents that Cricsheet is "maintained by a great fan of the game, Stephen Rushe" and that ESPNcricinfo data requires copy-paste or scripts.\[18\] That confirms there is no clean official bulk API.
- **CricAPI and data.gov.in:** not verified in this research. Don't rely on them.
- **Auction prices.** We found no licensed auction CSV. The legal route is to hand-type a small companion table (about 20–40 shortlisted players: name, team, auction year, price in ₹ crore) from IPLT20.com/auction/2025, ESPNcricinfo and Business Standard, with a "Source" column on every row. Join it to your MSI table with XLOOKUP on a cleaned player-name key. Facts such as prices aren't copyrightable databases in themselves, but credit every source anyway.

### 3. Cricsheet background (for the "is this data trustworthy?" question)

- **Origins.** Cricsheet was "started in 2009", inspired by *Moneyball* and named as "a homage to Retrosheet", the baseball event-data project.\[1\]
- **Who runs it.** "That would be Stephen Rushe. He has written all of the code which extracts and validates the data."\[1\]
- **Formats.** JSON is "the official Cricsheet format… most likely to receive updates". YAML is legacy and CSV/XML are experimental.\[5\] The Ashwin CSV format is at version 2.3.0.\[4\]
- **The Register.** It covers 18,554 people and 28,456 identifiers from 12 sources, with 8,816 name variations.\[19\] Each person gets a stable 8-character hexadecimal ID, "the same identifier across all matches".\[4\] This is useful for joins and must *not* be displayed.
- **Limitations.** 377 matches involving Afghanistan are withheld\[20\] (this doesn't affect the IPL). Cricsheet invites error reports ("Ideally we won't have any but there's always the chance").\[19\] Its CSV formats are experimental.
- **Licence.** The register page states: "This dataset is made available under the Open Data Commons Attribution License: http://opendatacommons.org/licenses/by/1.0/." \[21\] A third-party guide (TIGZIG) notes the terms "sit on the Cricsheet register page rather than its home or downloads page".\[22\] We did not see the licence text on the downloads page itself.
- **What ODC-BY requires.** Its preamble lets users "freely share, modify, and use this Database subject only to the attribution requirements set out in Section 4". Section 4.3's model notice is: "Contains information from DATABASE NAME which is made available under the ODC Attribution License", with hyperlinks to the database and the licence.\[23\]

### 4. The PII question: a clear recommendation

The hackathon rule bans showing "personally identifiable information, names, phone numbers, emails, or IDs". But the theme's success criterion is that a great solution "names one specific player, driver, or moment". The two rules can be reconciled like this:

- **Show:** professional players' names in the context of their public match performance. This is published on official scorecards and it is the deliverable the brief asks for.
- **Hide:** Cricsheet registry hex IDs, match IDs, and any person identifiers from the dashboard (use them only inside the cleaned table for joins). Also hide umpire and referee names, and any personal attributes such as age or date of birth.
- **Document it:** add one line on the Sources slide: "Player names appear only as public professional sporting records; no personal identifiers or contact data are displayed." Ask the mentor to confirm this at Milestone 1 and write the confirmation down.

We found no ruling from the organisers on this. The recommendation rests on reading the rule's intent (contact and identity data) together with the brief's explicit requirement.

### 5. Theme knowledge base

**Win-probability models in cricket:**
- **WASP** (Winning and Score Predictor) was built by Dr Scott Brooker and Dr Seamus Hogan at the University of Canterbury and first used by Sky Sport in November 2012.\[24\] It works backwards from V(b,w), the expected additional runs after b legal balls and w wickets, using "all non-shortened ODI and Twenty20 games played between top-eight countries since late 2006".\[25\] It assumes "an average batting team is playing an average bowling team".\[26\] This is exactly the transparent lookup-table design you can build in Anthrena.
- **Asif & McHale (2016)**, *International Journal of Forecasting* 32(1):34–43, is a dynamic logistic regression whose coefficients "evolve smoothly as the match progresses". Its forecasts are "similar quantitatively" to betting markets.\[27\]
- **A Springer chapter, "In-Game Win Prediction Models for Cricket" (doi:10.1007/978-3-031-67871-4_11)**, extends Asif–McHale to IPL ball-by-ball data by "integrating historical data via power priors" and Gaussian-process smoothing, tested by "cross validation on data from hundreds of IPL matches".
- **arXiv 2608.14696** calls WASP "the direct ancestor" of ball-by-ball dynamic-programming WP models\[28\] and studies a calibration-versus-leverage trade-off. It is directly relevant to defending an MSI built on WP swings.
- **arXiv 2505.01849** applies higher-order Markov models and a Pressure Index to T20 run chases.
- **Other classics:** Bailey & Clarke (2006, *J Sports Sci Med*) on in-play ODI prediction; Preston & Thompson (2002, *JRSS D*) on rain rules and probabilities of victory; McHale & Asif (2013, *EJOR*) on a modified Duckworth–Lewis method.\[29\]
- **Baseball WPA origins** (the Mills brothers, FanGraphs definitions) and commercial metrics (CricViz Impact, Smart Stats) were not verified in this research. Describe them only generally.

**The Impact Player rule (introduced 2023):**
- **Mechanics.** Teams name five substitutes; Tushar Deshpande was the first Impact Player, on 31 March 2023.\[30\]
- **Misra (2026):**
  - The data covers 2,355 innings.\[9\]
  - Pre-impact average: 155.9 runs and 5.6 sixes per innings. Impact era: 179.6 runs and 8.5 sixes.\[9\]
  - Fixed-effects estimate: +25.0 runs. With a linear time trend: +15.2. Robust Synthetic Control: +12.3. Multi-dimensional RSC: +11.2.\[9\]
  - Win-probability effect: OR = 1.22, p = 0.44.\[9\]
  - 90% of matches see both teams use the rule.\[9\]
  - Toss winners now field 76% of the time, up from 63%.\[9\]
  - Overs bowled by top-order batters fell 38%.\[9\]
  - It is a working paper, not peer-reviewed, and its data comes from ESPNcricinfo.\[9\]
- **Status.** The BCCI's player regulations said "the Impact Player Regulation will continue for the 2025 to 2027 cycle" (reported by Sportskeeda). The BCCI has since asked all 10 franchises for feedback by 31 August 2026, and IPL chairman Arun Dhumal said: "The matter is under discussion. Will take feedback from all the stakeholders and then take a call on this."
- **Why it matters for you.** Compute MSI within eras, or at least flag pre-2023 against 2023+ results. Because a WP model is fitted on outcomes, it automatically re-prices runs in a high-scoring era if you fit it separately for 2023+.

**Other comparability changes:**
- **IPL 2025:** the saliva ban was lifted, a replacement ball became available after the 11th over of the second innings in evening games to counter dew, and DRS was extended to height no-balls and off-side wides using Hawk-Eye.\[31\]\[32\]
- **IPL 2023:** reviews for wides and no-balls were introduced (per Cricsheet).\[16\]
- The two-bouncers-per-over rule (2024) and the history of strategic timeouts were not verified here. The expansion to 10 teams is verified for 2025–26 but its start year was not confirmed.

**Business stakes (sourced):**
- **Media rights 2023–27:** ₹48,390.32 crore per the BCCI's official release (ESPNcricinfo reports ₹48,390.5 crore) for 410 matches, 2.96× the 2018–22 cycle's ₹16,347.5 crore. Disney Star took TV for ₹23,575 crore and Viacom18 took digital for ₹23,758 crore. BCCI secretary Jay Shah told PTI there would be "410 games, with 74 games each in the first two seasons and then 84 games in the next and finally 94 in the 2027 edition" (reported by Scroll.in).
- **Houlihan Lokey 2025:**
  - Business value US$18.5 billion (+12.9%); standalone brand value US$3.9 billion.\[33\]
  - Franchise brand values: RCB US$269 million, MI 242, CSK 235, KKR 227, SRH 154, PBKS 141 (+39.6%), LSG 122.\[33\]\[34\]
  - The 2025 final drew 67.8 crore JioHotstar views.\[33\]
  - Brand Finance and D&P Advisory figures were not verified.
- **2025 mega auction (Jeddah, 24–25 Nov 2024):**
  - ₹639.15 crore spent on 182 players, from a ₹120 crore purse per team and a maximum of six retentions.\[10\]\[35\]
  - Top buys: Rishabh Pant ₹27 crore (LSG), Shreyas Iyer ₹26.75 crore (PBKS), Venkatesh Iyer ₹23.75 crore (KKR).\[10\]
  - 13-year-old Vaibhav Sooryavanshi went to RR for ₹1.1 crore.\[17\] He topped IPL 2026 with 776 runs and was named MVP,\[12\] a ready-made "market undervalued" hook.
- **2026 mini-auction (Abu Dhabi, 16 Dec 2025):**
  - Cameron Green went to KKR for ₹25.20 crore but is paid only ₹18 crore under the overseas mini-auction cap; the ₹7.2 crore excess goes to BCCI player welfare.\[36\]
  - Other big buys: Pathirana ₹18 crore (KKR); Prashant Veer and Kartik Sharma ₹14.2 crore each (CSK).\[36\]
  - The purse was ₹125 crore per team. The combined ₹237.55 crore is reported by different outlets as either the purse available or the amount spent;\[37\]\[38\] cite it as "available purse".
- **IPL 2026:** 28 March – 31 May, 10 teams, 74 matches. RCB beat GT by 5 wickets for back-to-back titles. Kagiso Rabada took 29 wickets.\[12\]

**The anchor "scoreboard lies" moment: the IPL 2025 final (3 June 2025, Ahmedabad, ESPNcricinfo match 1473511).**
- RCB made 190/9 (Kohli 43) and beat PBKS, 184/7 (Shashank Singh 61* off 30), by 6 runs.\[39\]
- Krunal Pandya was Player of the Match for 2/17 in four overs.\[40\] He took no top-scoring batting role, and had the match's most dot balls (12).\[40\]
- ESPNcricinfo called the six-run margin "deceptive". PBKS needed 29 off the last over, and Hazlewood's two opening dots "all but ended the contest mathematically" before Shashank's late 6-4-6-6.\[39\]
- That is textbook garbage-time inflation: Shashank's 61* looks match-defining on the scorecard, but the win-probability gain from his late sixes was near zero. Validate this in your own WP curve before you claim it.

### 6. Data-collection plan (Milestone 1)

1. **Download** IPL.csv from chaitu20 while logged into Kaggle. Screenshot the licence field, the version or "Updated" date, and the file panel ("64 columns"). Keep the zip unmodified.
2. **Download the backup** patrickb1912 (both CSVs) and screenshot its licence field the same way.
3. **Download the reference** Cricsheet `ipl_json.zip` (1,243 matches) for provenance only, not for import. Screenshot the Cricsheet register page's ODC-BY statement.
4. **Verify in Anthrena:**
   - The row count matches about 295,732.
   - Distinct `season` values run 2008–2025 (note any 2026 rows).
   - Distinct `match_id` count is recorded.
   - Rows per match are about 240–260.
5. **Spot-check the 2025 final.** Filter the date to 2025-06-03. Batting-team sums should give RCB 190 and PBKS 184, wickets 9 and 7, with Krunal Pandya's bowling rows showing 17 runs and 2 wickets, and `match_won_by` = Royal Challengers Bengaluru.
6. **Write a provenance log**: file name, URL, download timestamp, row and column counts, licence screenshot, and the cleaning steps listed above.
7. **Clean in Anthrena:**
   - Fill blank extras with 0.
   - Normalise team, venue and season labels.
   - Remove true duplicates (whole-row matches).
   - Keep only innings 1–2.
   - Flag D/L, no-result and tie matches.
   - Cap or flag outliers rather than deleting them (a 30-run over is real).
   - Cast data types.
   - Export this as the one "cleaned" table that every visual uses.

**Paste-ready "Sources & credits" block:**

> **Data sources.** Ball-by-ball data: "IPL Dataset(2008-2025)", uploaded by chaitu20 on Kaggle, https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025 (licence as shown on Kaggle, screenshot on file), compiled from Cricsheet. Contains information from Cricsheet (https://cricsheet.org), which is made available under the ODC Attribution License (https://opendatacommons.org/licenses/by/1-0/). Cricsheet data © Stephen Rushe / Cricsheet. Auction prices hand-compiled from IPLT20.com (https://www.iplt20.com/auction/2025), ESPNcricinfo and Business Standard. Match verification: ESPNcricinfo scorecard, IPL 2025 Final. Player names appear only as public professional sporting records; no personal identifiers are displayed. All analysis performed in Anthrena Desk.

### 7. Mentor / judge Q&A bank

1. **Why this theme?** Batting average divides runs by dismissals\[41\] and ignores when runs came.\[41\] WP-added measures whether runs changed the result, which is exactly the "hidden scoreboard".
2. **Why IPL?** It has the densest open T20 ball-by-ball record (1,243 matches on Cricsheet) and the largest money at stake (₹639.15 crore at the 2025 mega auction).
3. **Why this dataset?** It is a single CSV derived from Cricsheet, with 64 columns including a legal-ball flag and the winner,\[6\]\[7\] so it can be imported without conversion under the Anthrena-only rule.
4. **Is it legal?** The underlying data is Cricsheet's, under ODC-BY 1.0, which permits use and adaptation "subject only to the attribution requirements".\[23\] We credit both Cricsheet and the uploader.
5. **What if the Kaggle licence says "Unknown"?** Our rights flow from Cricsheet's ODC-BY. The backup is patrickb1912, and the last resort is Cricsheet itself.
6. **Why not Cricsheet directly?** Its main format is JSON (not importable), and its CSVs come as two files per match (about 2,486 files).\[3\]\[5\] Converting them outside Anthrena would break the rules.
7. **Did you convert any format?** No. We imported the Kaggle CSV as downloaded.
8. **Why not include 2026?** No complete, clean-rights single file exists. 2026 is our planned out-of-sample test.
9. **How do you clean it?** Blank extras become 0; labels are normalised; true duplicates are removed on the whole row, not on the ball key; super overs are dropped; D/L and no-result matches are flagged; types are cast; outliers are flagged.
10. **Aren't repeated ball numbers duplicates?** No. Cricsheet assigns the same `actual_delivery` to a wide or no-ball and the re-bowled ball.\[4\]\[13\]
11. **Why are overs 0–19?** Cricsheet's "23.5" means the 5th ball of the 24th over, so overs are 0-indexed. We add 1 for display.
12. **How do you handle rain and DLS?** We exclude matches with method = D/L from fitting, because the targets are revised and states aren't comparable.
13. **Super overs?** They are innings 3 and 4 and are excluded from the model;\[42\] ties are resolved through the eliminator winner.
14. **Wides and no-balls?** They count toward runs and state but not toward balls faced (valid_ball = 0).
15. **Why win probability rather than runs?** Misra shows the Impact Player rule adds about 12 runs per innings with no detectable change in who wins.\[9\] Runs inflate; WP doesn't.
16. **How is the WP model built?** It is a WASP-style empirical lookup: WP = the share of historical chases won from the state (balls left bucket, wickets in hand, runs required bucket). The first innings uses an expected-final-score table.
17. **What exactly is MSI?** Sum the batter's ΔWP on legal balls faced, divide by legal balls faced, and multiply by 100.
18. **How do you validate the model?** Check calibration by bin (predicted against actual win rate), compute a Brier score, and hold out 2025. Show a curve that ends at RCB 100% for the 2025 final.
19. **What about small samples?** Set a minimum of 300 legal balls and show confidence bands or a shrinkage note.
20. **What about selection bias?** Openers and finishers face different states, so compare MSI within batting role or phase.
21. **How do you adjust for era?** Fit separate WP tables for 2008–2022 and 2023+.
22. **Correlation versus causation?** MSI is descriptive credit assignment, not a causal effect. We say so.
23. **Why not ESPNcricinfo's win probability, or CricViz?** They are closed and not reproducible. Ours is fully auditable in a spreadsheet, like WASP.
24. **What is the business value?** Shortlist re-ranking against ₹120–125 crore purses. One misprice at the ₹18–27 crore level is worth more than an analyst's salary.
25. **Who would pay for this?** Franchise analytics teams, fantasy platforms and broadcasters. WASP itself went from university research to TV and is now owned by NV Play.\[43\]
26. **Isn't showing names PII?** They are public professional records required by the brief. We display no IDs or contact data.
27. **What are the limitations?** No ball-tracking or fielding data, no bowler-quality adjustment, and a lookup-table WP that assumes average teams (WASP's own caveat).
28. **What would you do with more time?** Build a logistic WP model (Asif–McHale style), add bowler-strength adjustment and 2026 validation, and publish an MSI for bowlers.
29. **How does Anthrena help?** All joins (XLOOKUP for state→WP), cleaning and visuals happen in one auditable tool; the cleaned table is the single source.
30. **Which player will you name?** Decide from the data. Strong pre-registered candidates are Krunal Pandya (2025 final) and a late-innings batter whose runs came when WP was already near 0 or 1.

## Recommendations

- At the mentor meeting, present chaitu20 as the primary dataset, patrickb1912 as the backup and Cricsheet as the source of truth, and show the licence screenshots and the 2025-final spot-check.
- Get written mentor confirmation on two points: that player names are allowed, and that importing a Kaggle CSV derived from Cricsheet is allowed.
- Freeze the dataset version: record the download time and row count, and never re-download mid-hackathon.
- Build the WP table on 2008–2024 and validate on 2025 so you have an honest holdout.

## Caveats and risks

- **Licence uncertainty:** chaitu20's Kaggle licence field was not directly visible to us. The mitigation is ODC-BY attribution to Cricsheet plus the backup dataset.
- **Row-count ambiguity:** 295,732 rows is reported for both 2008–2025 and 2008–2026 versions,\[7\]\[8\] so verify on download.
- **File size:** a file of about 300K rows × 64 columns may be slow. Hide unused columns early and work from a pivoted innings-state table.
- **Column-name confusion:** only 21 of the 64 columns were confirmed. Map the rest to the Cricsheet Ashwin specification on arrival.
- **Unverified items:** ESPNcricinfo terms of use, CricAPI and data.gov.in, the 2024 bouncer rule, and baseball WPA history. The Misra paper is a working paper.
- **Unexpected gaps:** if 2025 turns out to be missing from the chaitu20 file, switch to patrickb1912 (2008–2024) and treat 2025 as out of scope.

## Sources

1. [About - Cricsheet](https://cricsheet.org/about/)
2. [Match data - Cricsheet](https://cricsheet.org/matches/)
3. [Introducing the Cricsheet Register, and a new data format, JSON - Cricsheet](https://cricsheet.org/article/introducing-the-cricsheet-register-and-a-new-data-format-json/)
4. [Cricsheet "Ashwin" CSV format](https://cricsheet.org/format/csv_ashwin/)
5. [Match Data Formats - Cricsheet](https://cricsheet.org/format/)
6. [IPL Dataset](https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025)
7. [GitHub - HemangiGadhavi/IPL-Data-Analytics-Dashboard: Interactive IPL Data Analytics Dashboard built with Python, Pandas, Streamlit & Plotly. Analyze batting, bowling, teams, venues, toss impact, season trends, and over-wise scoring using ball-by-ball IPL data from 2008–2025.](https://github.com/HemangiGadhavi/IPL-Data-Analytics-Dashboard)
8. [GitHub - poonamjundre725-dotcom/ibm-bob-project: IPL Cricket Data Analytics Dashboard — End-to-End Data Analytics Project using Python, Pandas, Plotly & Streamlit](https://github.com/poonamjundre725-dotcom/ibm-bob-project)
9. <https://www.cs.columbia.edu/~misra/impact-player-2026.pdf>
10. [IPL 2025 mega auction: Full list of players sold, teamwise players' salary | IPL 2024 News - Business Standard](https://www.business-standard.com/cricket/ipl/ipl-2025-mega-auction-full-list-of-players-sold-teamwise-players-salary-124112600201_1.html)
11. [IPL Complete Dataset 2008-2025 (Enhanced Edition)](https://www.kaggle.com/datasets/meruvakodandasuraj/ipl-complete-dataset-2008-2025-enhanced-edition)
12. [2026 Indian Premier League](https://en.wikipedia.org/wiki/2026_Indian_Premier_League)
13. [Introduction to the JSON format](https://cricsheet.org/format/json/)
14. [Introduction to the YAML format](https://cricsheet.org/format/yaml/)
15. [PBKS vs RCB Cricket Scorecard, Final at Ahmedabad, June 03, 2025](https://www.espncricinfo.com/series/ipl-2025-1449924/punjab-kings-vs-royal-challengers-bengaluru-final-1473511/full-scorecard)
16. [Monthnotes: April 2023 - Cricsheet](https://cricsheet.org/article/monthnotes-april-2023/)
17. [IPL 2025 Auction | Live Updates & Overview | IPLT20](https://www.iplt20.com/auction/2025)
18. [cricketdata: An Open Source R package](https://archive.linux.duke.edu/cran/web/packages/cricketdata/vignettes/cricketdata_R_pkg.html)
19. [Cricsheet](https://cricsheet.org/)
20. [Available match data downloads - Cricsheet](https://cricsheet.org/downloads/)
21. [Cricsheet Register - Cricsheet](https://cricsheet.org/register/)
22. [How to download and process Cricsheet data (ball-by-ball, CSV, DuckDB) | TIGZIG](https://www.tigzig.com/agents-faq/how-to-download-and-process-cricsheet-data)
23. [Open Data Commons Attribution License (ODC-By) v1.0 — Open Data Commons: legal tools for open data](https://opendatacommons.org/licenses/by/1-0/)
24. [WASP: Winning and Score Predictor makes for an interesting watch on television - Cricket Country](https://www.cricketcountry.com/articles/wasp-winning-and-score-predictor-makes-for-an-interesting-watch-on-television-87588/)
25. [WASP (cricket calculation tool)](<https://en.wikipedia.org/wiki/WASP_(cricket_calculation_tool)>)
26. [CricTrade: Cricket WASP](http://www.crictrade.com/2014/07/cricket-wasp.html)
27. [In-play forecasting of win probability in One-Day International cricket: A dynamic logistic regression model - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0169207015000618)
28. [The Calibration-Leverage Tradeoff in Exactly Solvable Win-Probability Models](https://arxiv.org/pdf/2608.14696)
29. [Regression to Forecast: An In-Play Outcome Prediction for One-Day Cricket Matches | Springer Nature Link](https://link.springer.com/chapter/10.1007/978-981-19-2358-6_5)
30. [Impact Player rule: How it works in the IPL - Olympics.com](https://www.olympics.com/en/news/impact-player-rule-ipl-cricket)
31. [IPL 2025: BCCI Officially Lifts Ban On Saliva; Expands DRS Scope & Gives Option Of Second Ball](https://www.etvbharat.com/en/!sports/ipl-2025-bcci-officially-lifts-ban-on-saliva-expands-drs-scope-and-gives-option-of-second-ball-enn25032107421)
32. [IPL 2025: BCCI Introduces Key Rule Changes; Lifts Saliva Ban, Adds Second Ball For Dew Factor | News Mobile](https://www.newsmobile.in/sports/ipl-2025-bcci-introduces-key-rule-changes-lifts-saliva-ban-adds-second-ball-for-dew-factor/)
33. [Houlihan Lokey Launches IPL Valuation Study 2025](https://hl.com/media/x1kcmcty/houlihan-lokey-ipl-2025-valuation-study.pdf)
34. [IPL valuation leaps 12.9% to US\$18.5bn - SportsPro](https://www.sportspro.com/news/ipl-valuation-teams-franchises-rcb-mumabi-indians-chennai-super-kings-july-2025/)
35. [ben stokes missing ipl 2025 auction long list rishabh pant kl rahul mitchell starc list highest base price](https://africa.espn.com/cricket/story/_/id/42211048/ben-stokes-missing-ipl-2025-auction-long-list-rishabh-pant-kl-rahul-mitchell-starc-list-highest-base-price)
36. [kkr buy cameron green inr 2520 crore ipl 2026 auction](https://africa.espn.com/cricket/story/_/id/47322426/kkr-buy-cameron-green-inr-2520-crore-ipl-2026-auction)
37. [IPL 2026 player list - all teams' squads - Olympics.com](https://www.olympics.com/en/news/ipl-2026-teams-squads-list-player-prices)
38. [IPL 2026 Highest Price Player: Complete List, Records & Auction Analysis](https://iplkibaat.com/ipl-2026-highest-price-player/)
39. [punjab kings vs royal challengers bengaluru final ipl](https://africa.espn.com/cricket/series/8048/report/1473511/punjab-kings-vs-royal-challengers-bengaluru-final-ipl)
40. [RCB vs PBKS, IPL 2025 Final: Full list of award winners, Player of the Match, scorecard & records](https://www.sportskeeda.com/cricket/rcb-vs-pbks-ipl-2025-final-full-list-award-winners-player-match-scorecard-records)
41. [Cricsheet data](https://archive.linux.duke.edu/cran/web/packages/cricketdata/vignettes/cricsheet.html)
42. [IPL Dataset by CricSheet](https://www.kaggle.com/datasets/sanjeesi/ipl-dataset-by-cricsheet)
43. [What is WASP in Cricket? How Does it Work?](https://madaboutsports.in/blog/glossary/what-is-wasp-in-cricket/)
