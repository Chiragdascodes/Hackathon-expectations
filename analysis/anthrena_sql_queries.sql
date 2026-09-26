-- Signal 26 · Anthrena Desk SQL pack
-- Where: open the sheet 01_ipl_clean_balls -> Data -> Query
-- Paste ONE query, Run (preview), then "Use result" -> it becomes a new Sheet.
-- Rename each new Sheet with the name in its header (double-click the tab).
-- The active sheet is always called `dataset` inside Query.
-- Tested for syntax on both DuckDB and SQLite (Anthrena's engine is not documented).


-- ============ Q0 · smoke test (run first: proves Query works on your sheet)
SELECT COUNT(*) AS balls, COUNT(DISTINCT match_id) AS matches,
       MIN(season_year) AS first_season, MAX(season_year) AS last_season
FROM dataset;


-- ============ Q1 · Sheet "innings_totals"  (H2 Impact-era test, box plot, trend line)
SELECT match_id, innings, season_year, era, batting_team,
       SUM(runs_total) AS total,
       SUM(is_wicket) AS wickets,
       SUM(CASE WHEN runs_batter = 6 THEN 1 ELSE 0 END) AS sixes,
       SUM(CASE WHEN runs_batter = 4 THEN 1 ELSE 0 END) AS fours,
       MAX(flag_dl_or_reduced) AS flag_dl_or_reduced
FROM dataset
GROUP BY match_id, innings, season_year, era, batting_team;


-- ============ Q2 · Sheet "phase_run_rate"  (line chart: run rate by season x phase)
SELECT season_year, era, phase,
       ROUND(SUM(runs_total) * 6.0 / SUM(valid_ball), 2) AS run_rate,
       ROUND(SUM(CASE WHEN runs_batter = 6 THEN 1 ELSE 0 END) * 1.0 / COUNT(DISTINCT match_id), 2) AS sixes_per_match,
       ROUND(SUM(valid_ball) * 1.0 / NULLIF(SUM(is_wicket), 0), 1) AS balls_per_wicket
FROM dataset
GROUP BY season_year, era, phase
ORDER BY season_year, phase;


-- ============ Q3 · Sheet "toss_table"  (H3 chi-square: toss result x era)
SELECT match_id, era, toss_decision,
       CASE WHEN toss_winner = match_won_by THEN 'Toss winner won' ELSE 'Toss winner lost' END AS toss_outcome
FROM dataset
WHERE flag_no_result = 0
GROUP BY match_id, era, toss_decision, toss_winner, match_won_by;


-- ============ Q4 · Sheet "wp_heatmap"  (transparent win-probability table)
-- chase state at the start of every over, clean matches only
SELECT wkts_group, balls_left_band, runs_req_band,
       ROUND(AVG(chase_won) * 100, 1) AS chase_win_pct,
       COUNT(*) AS states
FROM (
    SELECT match_id, legal_before, MAX(chase_won) AS chase_won,
           CASE WHEN MIN(wkts_in_hand_before) <= 3 THEN '0-3'
                WHEN MIN(wkts_in_hand_before) <= 6 THEN '4-6' ELSE '7-10' END AS wkts_group,
           CASE WHEN MIN(balls_left_before) <= 24 THEN '01-24'
                WHEN MIN(balls_left_before) <= 48 THEN '25-48'
                WHEN MIN(balls_left_before) <= 72 THEN '49-72'
                WHEN MIN(balls_left_before) <= 96 THEN '73-96' ELSE '97-120' END AS balls_left_band,
           CASE WHEN MIN(runs_required_before) <= 20 THEN '000-020'
                WHEN MIN(runs_required_before) <= 40 THEN '021-040'
                WHEN MIN(runs_required_before) <= 60 THEN '041-060'
                WHEN MIN(runs_required_before) <= 80 THEN '061-080'
                WHEN MIN(runs_required_before) <= 100 THEN '081-100'
                WHEN MIN(runs_required_before) <= 120 THEN '101-120' ELSE '121+' END AS runs_req_band
    FROM dataset
    WHERE innings = 2 AND model_ok = 1 AND legal_before % 6 = 0
    GROUP BY match_id, legal_before
) s
GROUP BY wkts_group, balls_left_band, runs_req_band
ORDER BY wkts_group, balls_left_band, runs_req_band;


-- ============ Q5 · Sheet "batter_impact"  (MSI computed INSIDE Anthrena from the per-ball WPA)
SELECT batter,
       SUM(runs_batter) AS runs,
       SUM(ball_faced) AS balls,
       ROUND(SUM(runs_batter) * 100.0 / NULLIF(SUM(ball_faced), 0), 1) AS strike_rate,
       SUM(CASE WHEN innings = 2 AND model_ok = 1 THEN ball_faced ELSE 0 END) AS chase_balls,
       ROUND(SUM(CASE WHEN innings = 2 AND model_ok = 1 THEN wpa_batting ELSE 0 END) * 10000.0
             / NULLIF(SUM(CASE WHEN innings = 2 AND model_ok = 1 THEN ball_faced ELSE 0 END), 0), 2) AS msi,
       ROUND(SUM(CASE WHEN innings = 1 AND model_ok = 1 THEN runs_above_exp ELSE 0 END) * 100.0
             / NULLIF(SUM(CASE WHEN innings = 1 AND model_ok = 1 THEN ball_faced ELSE 0 END), 0), 2) AS runs_above_exp_per100,
       ROUND(SUM(CASE WHEN phase = 'Death' THEN runs_batter ELSE 0 END) * 100.0
             / NULLIF(SUM(CASE WHEN phase = 'Death' THEN ball_faced ELSE 0 END), 0), 1) AS death_strike_rate
FROM dataset
GROUP BY batter
HAVING SUM(ball_faced) >= 300
ORDER BY msi DESC;
-- batting average needs dismissals: join 07_batters_msi (Data -> Query, JOIN on batter) or use that file directly


-- ============ Q6 · Sheet "bowler_impact"  (the Krunal Pandya question)
SELECT bowler,
       SUM(valid_ball) AS balls,
       SUM(bowler_wicket) AS wickets,
       ROUND(SUM(runs_total) * 6.0 / NULLIF(SUM(valid_ball), 0), 2) AS economy,
       ROUND(-SUM(CASE WHEN innings = 2 AND model_ok = 1 THEN wpa_batting ELSE 0 END) * 10000.0
             / NULLIF(SUM(CASE WHEN innings = 2 AND model_ok = 1 THEN valid_ball ELSE 0 END), 0), 2) AS bowler_msi
FROM dataset
GROUP BY bowler
HAVING SUM(valid_ball) >= 300
ORDER BY bowler_msi DESC;


-- ============ Q7 · Sheet "finals_worm"  (win-probability line for every final; filter season_year on the chart)
SELECT season_year, delivery_seq, innings, over_display, ball, batter, bowler, runs_total, is_wicket,
       runs_after, wkts_after, runs_required_after,
       ROUND(wp_after * 100, 1) AS chase_win_prob_pct,
       ROUND(wpa_batting * 100, 1) AS swing_pct_pts
FROM dataset
WHERE stage = 'Final' AND innings = 2
ORDER BY season_year, delivery_seq;


-- ============ Q8 · Sheet "garbage_time"  (runs scored after the match was already decided)
SELECT batter,
       SUM(runs_batter) AS chase_runs,
       SUM(CASE WHEN wp_before < 0.10 OR wp_before > 0.90 THEN runs_batter ELSE 0 END) AS runs_when_decided,
       ROUND(SUM(CASE WHEN wp_before < 0.10 OR wp_before > 0.90 THEN runs_batter ELSE 0 END) * 100.0
             / NULLIF(SUM(runs_batter), 0), 1) AS pct_runs_when_decided
FROM dataset
WHERE innings = 2 AND model_ok = 1
GROUP BY batter
HAVING SUM(ball_faced) >= 150
ORDER BY pct_runs_when_decided DESC;
