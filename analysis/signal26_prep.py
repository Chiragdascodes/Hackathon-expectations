# Signal 26 · Theme 1 "The Hidden Scoreboard" — data prep + win-probability + MSI
#
# HOW TO RUN (Kaggle Notebook, ~2-4 min):
#   1. Open https://www.kaggle.com/datasets/chaitu20/ipl-dataset2008-2025 -> Code -> New Notebook
#   2. Paste this whole file into one cell, press Shift+Enter
#   3. Right sidebar -> Output -> /kaggle/working/signal26_outputs.zip -> ⋮ -> Download
#   4. Unzip and import the CSVs into Anthrena Desk (every file is < 100,000 rows)
#
# Outside Anthrena only because the Influencer plan caps imports at 100k rows and
# the raw file has ~2.95 lakh rows; organisers allowed external tools with explanation.
# Every step is recorded in 00_cleaning_log.csv.

import glob, os, re, shutil
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GroupKFold

FIRST_SEASON = 2022          # 2021-25 = 102,115 rows (> 100k limit), so 2022-25
MIN_BALLS_BAT = 300          # qualifier for batting-average ranking
MIN_CHASE_BALLS = 150        # qualifier for MSI (chase balls faced)
MIN_BOWL_BALLS = 300         # qualifier for bowler tables

IN_PATH = os.environ.get("IPL_CSV") or (glob.glob("/kaggle/input/**/IPL.csv", recursive=True) or ["IPL.csv"])[0]
OUT = os.environ.get("OUT_DIR", "/kaggle/working/signal26_outputs")
os.makedirs(OUT, exist_ok=True)

log = []
def note(step, detail, rows):
    log.append({"step": len(log) + 1, "action": step, "detail": detail, "rows_after": rows})
    print(f"[{len(log):02d}] {step}: {detail} -> {rows:,} rows")

def col(df, *names):
    """First existing column among candidate names (case-insensitive), else None."""
    lower = {c.lower(): c for c in df.columns}
    for n in names:
        if n.lower() in lower:
            return lower[n.lower()]
    return None

# ---------------------------------------------------------------- 1. load + filter
df = pd.read_csv(IN_PATH, low_memory=False)
df["row_order"] = np.arange(len(df))            # file is in delivery order; keep it
note("Load raw file", f"{os.path.basename(IN_PATH)}, {df.shape[1]} columns", len(df))
print("Columns:", list(df.columns))

df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["season_year"] = df["date"].dt.year                     # '2020/21'-style labels ignored
df = df[df["season_year"] >= FIRST_SEASON].copy()
note("Filter seasons", f"keep {FIRST_SEASON}-{int(df['season_year'].max())} (platform 100k-row limit)", len(df))

before = len(df)
df = df.drop_duplicates(subset=[c for c in df.columns if c != "row_order"])
note("Remove exact duplicate rows", f"{before - len(df)} identical rows removed (repeated over.ball kept: wides/no-balls)", len(df))

n_super = int((df["innings"] > 2).sum())
df = df[df["innings"].isin([1, 2])].copy()
note("Drop super-over innings", f"{n_super} balls in innings 3+ removed", len(df))

# ---------------------------------------------------------------- 2. clean labels / types
TEAM_MAP = {
    "Royal Challengers Bangalore": "Royal Challengers Bengaluru",
    "Kings XI Punjab": "Punjab Kings",
    "Delhi Daredevils": "Delhi Capitals",
    "Rising Pune Supergiants": "Rising Pune Supergiant",
}
team_cols = [c for c in ["batting_team", "bowling_team", "toss_winner", "match_won_by"] if c in df]
changed = 0
for c in team_cols:
    df[c] = df[c].where(df[c].isna(), df[c].astype(str).str.strip())
    changed += int(df[c].isin(TEAM_MAP.keys()).sum())
    df[c] = df[c].replace(TEAM_MAP)
note("Unify franchise names", f"{changed} cells renamed (e.g. RC Bangalore -> RC Bengaluru)", len(df))

def clean_venue(v):
    if pd.isna(v):
        return v
    v = str(v).split(",")[0].strip()
    v = re.sub(r"\bM\.\s*", "M ", v)                          # M.Chinnaswamy -> M Chinnaswamy
    v = re.sub(r"\s+", " ", v)
    return v
if "venue" in df:
    raw_n = df["venue"].nunique()
    df["venue_clean"] = df["venue"].map(clean_venue)
    note("Unify venue spellings", f"{raw_n} raw venue labels -> {df['venue_clean'].nunique()}", len(df))

num_cols = [c for c in df.columns if c.startswith("runs_") or c in
            ("over", "ball", "valid_ball", "bowler_wicket", "innings", "extras", "wides", "noballs", "byes", "legbyes", "penalty")]
filled = 0
for c in num_cols:
    df[c] = pd.to_numeric(df[c], errors="coerce")
    filled += int(df[c].isna().sum())
    df[c] = df[c].fillna(0)
note("Numeric types + blank extras", f"{len(num_cols)} numeric columns cast; {filled} blanks -> 0", len(df))

wk = col(df, "wicket_kind", "wicket_type")
df[wk] = df[wk].where(df[wk].isna(), df[wk].astype(str).str.strip()).replace({"": np.nan, "nan": np.nan, "None": np.nan})
df["is_wicket"] = df[wk].notna().astype(int)
df["wicket_kind_clean"] = df[wk].fillna("none")
note("Structural blanks", "blank wicket_kind -> 'none'; is_wicket flag added", len(df))

# ---------------------------------------------------------------- 3. derived columns
df = df.sort_values(["match_id", "innings", "row_order"]).reset_index(drop=True)
g = df.groupby(["match_id", "innings"], sort=False)

df["over_display"] = df["over"].astype(int) + 1
df["phase"] = pd.cut(df["over"], [-1, 5, 14, 19], labels=["Powerplay", "Middle", "Death"]).astype(str)
df["era"] = np.where(df["season_year"] >= 2023, "Impact (2023+)", "Pre-Impact (2022)")

xt = col(df, "extra_type", "extras_type")
wd = col(df, "wides")
if xt:
    df["is_wide"] = df[xt].astype(str).str.contains("wide", case=False, na=False).astype(int)
elif wd:
    df["is_wide"] = (df[wd] > 0).astype(int)
else:
    df["is_wide"] = 0
df["ball_faced"] = (df["is_wide"] == 0).astype(int)        # no-balls count as faced, wides don't

df["runs_after"] = g["runs_total"].cumsum()
df["wkts_after"] = g["is_wicket"].cumsum()
df["legal_after"] = g["valid_ball"].cumsum()
df["runs_before"] = df["runs_after"] - df["runs_total"]
df["wkts_before"] = df["wkts_after"] - df["is_wicket"]
df["legal_before"] = df["legal_after"] - df["valid_ball"]
df["balls_left_before"] = 120 - df["legal_before"]
df["balls_left_after"] = 120 - df["legal_after"]
df["wkts_in_hand_before"] = 10 - df["wkts_before"]
df["wkts_in_hand_after"] = 10 - df["wkts_after"]

# match-level facts
inn = (df.groupby(["match_id", "innings"])
         .agg(total=("runs_total", "sum"), wkts=("is_wicket", "sum"), legal=("valid_ball", "sum"),
              team=("batting_team", "first"), sixes=("runs_batter", lambda s: int((s == 6).sum())),
              fours=("runs_batter", lambda s: int((s == 4).sum())))
         .reset_index())
first = inn[inn.innings == 1].set_index("match_id")
second = inn[inn.innings == 2].set_index("match_id")
m = df.groupby("match_id").agg(date=("date", "first"), season_year=("season_year", "first"),
                               era=("era", "first"), winner=("match_won_by", "first"),
                               toss_winner=("toss_winner", "first"),
                               toss_decision=("toss_decision", "first"),
                               venue=("venue_clean" if "venue_clean" in df else "venue", "first"))
m["first_total"] = first["total"]
m["target"] = m["first_total"] + 1
m["chasing_team"] = second["team"]
m["second_total"] = second["total"]

meth = col(df, "method", "result_method")
dl_ids = set(df.loc[df[meth].astype(str).str.contains("D/L|DLS", case=False, na=False), "match_id"]) if meth else set()
# Heuristic too: first innings stopped short (<120 legal balls, <10 wkts) = reduced-overs match
short = first[(first.legal < 120) & (first.wkts < 10)].index
m["flag_dl_or_reduced"] = m.index.isin(dl_ids | set(short))
m["flag_no_result"] = m["winner"].isna() | ~m["winner"].isin(set(df["batting_team"].dropna())) | m["second_total"].isna()
m["flag_tie"] = m["second_total"] == m["first_total"]
m["model_ok"] = ~(m.flag_dl_or_reduced | m.flag_no_result | m.flag_tie)
m["chase_won"] = m["winner"].eq(m["chasing_team"]).fillna(False).astype(int)
note("Flag matches", f"{int(m.flag_dl_or_reduced.sum())} D/L-or-reduced, {int(m.flag_no_result.sum())} no-result, "
     f"{int(m.flag_tie.sum())} tied (kept, excluded from model); {int(m.model_ok.sum())} clean matches", len(df))

df = df.merge(m[["target", "chase_won", "model_ok", "flag_dl_or_reduced", "flag_no_result", "flag_tie"]],
              left_on="match_id", right_index=True, how="left")
is2 = df["innings"] == 2
df["runs_required_before"] = np.where(is2, df["target"] - df["runs_before"], np.nan)
df["runs_required_after"] = np.where(is2, df["target"] - df["runs_after"], np.nan)
df["rrr_before"] = np.where(is2, df["runs_required_before"] / np.maximum(df["balls_left_before"], 1) * 6, np.nan)

# outliers: flag, don't delete
inn["z"] = inn.groupby("innings")["total"].transform(lambda s: (s - s.mean()) / s.std())
inn["flag_outlier_total"] = (inn["total"] >= 250) | (inn["z"].abs() > 3)
over_runs = df.groupby(["match_id", "innings", "over"])["runs_total"].transform("sum")
df["flag_big_over"] = (over_runs >= 25).astype(int)
note("Flag outliers", f"{int(inn.flag_outlier_total.sum())} innings totals >=250 or |z|>3; "
     f"{df.loc[df.flag_big_over == 1, ['match_id','innings','over']].drop_duplicates().shape[0]} overs of 25+ runs (kept)", len(df))

# ---------------------------------------------------------------- 4. chase win-probability model
F = ["runs_req", "balls_left", "wkts_in_hand"]
def states(frame, when):
    return pd.DataFrame({"runs_req": frame[f"runs_required_{when}"],
                         "balls_left": frame[f"balls_left_{when}"],
                         "wkts_in_hand": frame[f"wkts_in_hand_{when}"]})

ch = df[is2 & df["model_ok"]].copy()
X, y, grp = states(ch, "before"), ch["chase_won"].values, ch["match_id"].values
wp_oof = np.zeros(len(ch))
def model():
    # monotone: more runs needed -> lower WP; more balls / wickets -> higher WP
    return HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, min_samples_leaf=80,
                                          monotonic_cst=[-1, 1, 1], random_state=0)
for tr, te in GroupKFold(n_splits=5).split(X, y, grp):                      # match-level cross-fitting
    wp_oof[te] = model().fit(X.iloc[tr], y[tr]).predict_proba(X.iloc[te])[:, 1]
brier = float(np.mean((wp_oof - y) ** 2))
base_brier = float(np.mean((y.mean() - y) ** 2))
full = model().fit(X, y)
note("Win-probability model", f"monotone gradient boosting on {len(ch):,} chase balls, 5-fold by match; "
     f"Brier {brier:.3f} vs {base_brier:.3f} baseline", len(df))

def wp(frame, when):
    s = states(frame, when)
    p = full.predict_proba(s.fillna(0))[:, 1]
    p = np.where(s.runs_req <= 0, 1.0, p)
    p = np.where((s.runs_req > 0) & ((s.balls_left <= 0) | (s.wkts_in_hand <= 0)), 0.0, p)
    return p

c2 = df[is2].copy()
c2["wp_before"] = wp(c2, "before")
c2["wp_after"] = wp(c2, "after")
c2.loc[c2.index.isin(ch.index), "wp_before"] = np.where(ch["runs_required_before"] <= 0, 1.0, wp_oof)
# last ball of each chase resolves to the actual result
last = c2.groupby("match_id")["row_order"].transform("max") == c2["row_order"]
c2.loc[last & c2["model_ok"], "wp_after"] = c2.loc[last & c2["model_ok"], "chase_won"].astype(float)
# chain: wp_after of a ball = wp_before of the next ball (keeps swings additive)
nxt = c2.groupby("match_id")["wp_before"].shift(-1)
c2["wp_after"] = np.where(last, c2["wp_after"], nxt)
c2["wpa_batting"] = c2["wp_after"] - c2["wp_before"]          # credit to batter; minus to bowler
df = df.join(c2[["wp_before", "wp_after", "wpa_batting"]])

cal = pd.DataFrame({"pred": wp_oof, "won": y})
cal["bin"] = pd.cut(cal.pred, np.linspace(0, 1, 11), include_lowest=True)
calib = cal.groupby("bin", observed=True).agg(predicted_wp=("pred", "mean"), actual_win_rate=("won", "mean"),
                                              balls=("won", "size")).reset_index()
calib["bin"] = calib["bin"].astype(str)

# transparent lookup table (heatmap): chase state at the start of each over
st = ch[ch["legal_before"] % 6 == 0].copy()
st = st.drop_duplicates(["match_id", "legal_before"])
st["balls_left_band"] = pd.cut(st["balls_left_before"], [0, 24, 48, 72, 96, 120],
                               labels=["1-24", "25-48", "49-72", "73-96", "97-120"]).astype(str)
st["runs_req_band"] = pd.cut(st["runs_required_before"], [-1, 20, 40, 60, 80, 100, 120, 400],
                             labels=["0-20", "21-40", "41-60", "61-80", "81-100", "101-120", "121+"]).astype(str)
st["wkts_in_hand_group"] = pd.cut(st["wkts_in_hand_before"], [-1, 3, 6, 10], labels=["0-3", "4-6", "7-10"]).astype(str)
wp_table = (st.groupby(["wkts_in_hand_group", "balls_left_band", "runs_req_band"])
              .agg(chase_win_pct=("chase_won", "mean"), states=("chase_won", "size")).reset_index())
wp_table["chase_win_pct"] = (wp_table["chase_win_pct"] * 100).round(1)
wp_table["reliable_n30"] = wp_table["states"] >= 30

# ---------------------------------------------------------------- 5. first-innings runs above expected
f1 = df[(df.innings == 1) & df["model_ok"]]
f1_final = f1.groupby("match_id")["runs_total"].sum()
d1 = df[df.innings == 1].copy()
d1["rem"] = d1["match_id"].map(f1_final) - d1["runs_before"]
d1["over_idx_before"] = (d1["legal_before"] // 6).clip(0, 19)
d1["over_idx_after"] = (d1["legal_after"] // 6).clip(0, 19)
fit = d1[d1["model_ok"]]
cell = fit.groupby(["over_idx_before", "wkts_before"])["rem"].agg(["mean", "size"])
by_over = fit.groupby("over_idx_before")["rem"].mean()
def exp_rem(o, w, legal):
    if legal >= 120 or w >= 10:
        return 0.0
    if (o, w) in cell.index and cell.loc[(o, w), "size"] >= 20:
        return cell.loc[(o, w), "mean"]
    return by_over.get(o, 0.0) * max(0.0, 1 - w / 10)      # sparse cell: shrink toward over mean
d1["exp_before"] = [exp_rem(o, w, l) for o, w, l in zip(d1.over_idx_before, d1.wkts_before, d1.legal_before)]
d1["exp_after"] = [exp_rem(o, w, l) for o, w, l in zip(d1.over_idx_after, d1.wkts_after, d1.legal_after)]
d1["runs_above_exp"] = d1["runs_total"] + d1["exp_after"] - d1["exp_before"]
df = df.join(d1[["runs_above_exp"]])
note("First-innings run expectancy", "expected remaining runs by (over, wickets); runs_above_exp per ball", len(df))

# ---------------------------------------------------------------- 6. player tables
po = col(df, "player_out")
if po:
    outs = df[df[po].notna() & (df["is_wicket"] == 1)].groupby(po).size()
else:
    outs = df[(df["is_wicket"] == 1)].groupby("batter").size()
bb = df.groupby("batter").agg(
    runs=("runs_batter", "sum"), balls=("ball_faced", "sum"),
    innings=("match_id", "nunique"),
    fours=("runs_batter", lambda s: int((s == 4).sum())), sixes=("runs_batter", lambda s: int((s == 6).sum())))
bb["dismissals"] = outs.reindex(bb.index).fillna(0).astype(int)
bb["batting_avg"] = (bb["runs"] / bb["dismissals"].replace(0, np.nan)).round(2)
bb["strike_rate"] = (bb["runs"] / bb["balls"] * 100).round(1)
for ph in ["Powerplay", "Middle", "Death"]:
    s = df[df.phase == ph].groupby("batter").agg(r=("runs_batter", "sum"), b=("ball_faced", "sum"))
    bb[f"sr_{ph.lower()}"] = (s["r"] / s["b"] * 100).round(1).reindex(bb.index)
    bb[f"balls_{ph.lower()}"] = s["b"].reindex(bb.index).fillna(0).astype(int)

cb = df[is2 & df["model_ok"]]
chase = cb.groupby("batter").agg(chase_balls=("ball_faced", "sum"), chase_runs=("runs_batter", "sum"),
                                 wpa_total=("wpa_batting", "sum"))
live = cb[(cb.wp_before >= 0.2) & (cb.wp_before <= 0.8)].groupby("batter")["runs_batter"].sum()
dead = cb[(cb.wp_before < 0.1) | (cb.wp_before > 0.9)].groupby("batter")["runs_batter"].sum()
chase["pct_runs_in_live_states"] = (live.reindex(chase.index).fillna(0) / chase["chase_runs"].replace(0, np.nan) * 100).round(1)
chase["pct_runs_in_decided_states"] = (dead.reindex(chase.index).fillna(0) / chase["chase_runs"].replace(0, np.nan) * 100).round(1)
chase["MSI"] = (chase["wpa_total"] * 100 / chase["chase_balls"].replace(0, np.nan) * 100).round(2)
chase["wpa_total_pct_pts"] = (chase["wpa_total"] * 100).round(1)
bb = bb.join(chase.drop(columns="wpa_total"))
f1b = df[(df.innings == 1) & df["model_ok"]].groupby("batter").agg(first_inn_balls=("ball_faced", "sum"),
                                                                     rae=("runs_above_exp", "sum"))
bb = bb.join(f1b)
bb["runs_above_exp_per100"] = (bb["rae"] / bb["first_inn_balls"].replace(0, np.nan) * 100).round(2)
bb = bb.drop(columns="rae")
bb["qualifies_avg"] = bb["balls"] >= MIN_BALLS_BAT
bb["qualifies_msi"] = bb["chase_balls"].fillna(0) >= MIN_CHASE_BALLS
q = bb[bb.qualifies_avg & bb.qualifies_msi].copy()
q["rank_batting_avg"] = q["batting_avg"].rank(ascending=False, method="min")
q["rank_msi"] = q["MSI"].rank(ascending=False, method="min")
q["rank_gap_avg_minus_msi"] = q["rank_batting_avg"] - q["rank_msi"]     # + = MSI rates them higher
bb = bb.join(q[["rank_batting_avg", "rank_msi", "rank_gap_avg_minus_msi"]])
bb = bb.reset_index().rename(columns={"index": "batter"}).sort_values("MSI", ascending=False)

bw = df.groupby("bowler").agg(balls=("valid_ball", "sum"), runs_conceded=("runs_total", "sum"),
                             wickets=("bowler_wicket", "sum"))
bw["economy"] = (bw["runs_conceded"] / bw["balls"] * 6).round(2)
bw["bowling_avg"] = (bw["runs_conceded"] / bw["wickets"].replace(0, np.nan)).round(2)
bwc = cb.groupby("bowler").agg(chase_balls=("valid_ball", "sum"), wpa=("wpa_batting", "sum"))
bw = bw.join(bwc)
bw["bowler_MSI"] = (-bw["wpa"] * 100 / bw["chase_balls"].replace(0, np.nan) * 100).round(2)
bw = bw.drop(columns="wpa")
bw["qualifies"] = bw["balls"] >= MIN_BOWL_BALLS
bw = bw.reset_index().sort_values("bowler_MSI", ascending=False)

# ---------------------------------------------------------------- 7. story tables
fin = m[(m["date"] == "2025-06-03")].index
final_id = fin[0] if len(fin) else m.sort_values("date").index[-1]
worm_cols = ["match_id", "innings", "over_display", "ball", "batting_team", "batter", "bowler", "runs_total",
             "is_wicket", "runs_after", "wkts_after", "balls_left_after", "runs_required_after",
             "wp_before", "wp_after", "wpa_batting"]
worm = df[df.match_id == final_id][[c for c in worm_cols if c in df]].copy()
worm["ball_seq"] = np.arange(1, len(worm) + 1)
for c in ["wp_before", "wp_after", "wpa_batting"]:
    worm[c] = (worm[c] * 100).round(1)
over_swing = (worm[worm.innings == 2].groupby("over_display")
              .agg(bowler=("bowler", "first"), runs=("runs_total", "sum"), wkts=("is_wicket", "sum"),
                   wp_start=("wp_before", "first"), wp_end=("wp_after", "last")).reset_index())
over_swing["wp_swing_pct_pts"] = (over_swing["wp_end"] - over_swing["wp_start"]).round(1)

moments = df[is2 & df["model_ok"]].copy()
moments["abs_swing"] = moments["wpa_batting"].abs()
moments = moments.nlargest(50, "abs_swing")[["match_id", "date", "season_year", "batting_team", "bowling_team",
                                             "over_display", "batter", "bowler", "runs_total", "wicket_kind_clean",
                                             "wp_before", "wp_after", "wpa_batting"]]
for c in ["wp_before", "wp_after", "wpa_batting"]:
    moments[c] = (moments[c] * 100).round(1)

inn = inn.merge(m[["season_year", "era", "venue", "winner", "flag_dl_or_reduced", "flag_no_result"]],
                left_on="match_id", right_index=True)
inn["won"] = (inn["team"] == inn["winner"]).astype(int)

season = (df.groupby(["season_year", "phase"])
            .agg(runs=("runs_total", "sum"), legal=("valid_ball", "sum"),
                 sixes=("runs_batter", lambda s: int((s == 6).sum())), wkts=("is_wicket", "sum")).reset_index())
season["run_rate"] = (season["runs"] / season["legal"] * 6).round(2)

# ---------------------------------------------------------------- 8. statistical tests (re-run these in Anthrena too)
tests = []
ok1 = inn[(inn.innings == 1) & ~inn.flag_dl_or_reduced & ~inn.flag_no_result]
a = ok1[ok1.era.str.startswith("Pre")]["total"]; b = ok1[ok1.era.str.startswith("Impact")]["total"]
if len(a) and len(b):
    u = stats.mannwhitneyu(a, b, alternative="two-sided")
    t = stats.ttest_ind(a, b, equal_var=False)
    tests.append({"hypothesis": "H2 first-innings totals differ pre vs Impact era", "test": "Mann-Whitney U",
                  "statistic": round(u.statistic, 1), "p_value": u.pvalue,
                  "detail": f"median {a.median():.0f} vs {b.median():.0f}; mean {a.mean():.1f} vs {b.mean():.1f} (n={len(a)},{len(b)})"})
    tests.append({"hypothesis": "H2 (parametric check)", "test": "Welch t-test", "statistic": round(t.statistic, 2),
                  "p_value": t.pvalue, "detail": f"mean diff {b.mean() - a.mean():+.1f} runs"})
mm = m[~m.flag_no_result].copy()
mm["toss_win_match_win"] = (mm["toss_winner"] == mm["winner"]).map({True: "Toss winner won", False: "Toss winner lost"})
ct = pd.crosstab(mm["era"], mm["toss_win_match_win"])
if ct.shape == (2, 2):
    chi = stats.chi2_contingency(ct)
    rates = (ct.get("Toss winner won", 0) / ct.sum(axis=1) * 100).round(1).to_dict()
    tests.append({"hypothesis": "H3 toss advantage changed with era", "test": "Chi-square", "statistic": round(chi[0], 3),
                  "p_value": chi[1], "detail": f"toss-winner win %: {rates}"})
bt = stats.binomtest(int((mm['toss_winner'] == mm['winner']).sum()), len(mm), 0.5)
tests.append({"hypothesis": "H3b toss winner wins more than 50%", "test": "Binomial", "statistic": round(bt.statistic, 3),
              "p_value": bt.pvalue, "detail": f"{(mm['toss_winner'] == mm['winner']).mean() * 100:.1f}% of {len(mm)} matches"})
if len(q) >= 5:
    rho = stats.spearmanr(q["batting_avg"], q["MSI"], nan_policy="omit")
    tests.append({"hypothesis": "H1 batting average tracks match impact (MSI)", "test": "Spearman rank",
                  "statistic": round(rho.statistic, 3), "p_value": rho.pvalue, "detail": f"{len(q)} qualified batters"})
    rho2 = stats.spearmanr(q["strike_rate"], q["MSI"], nan_policy="omit")
    tests.append({"hypothesis": "H1b strike rate tracks MSI", "test": "Spearman rank",
                  "statistic": round(rho2.statistic, 3), "p_value": rho2.pvalue, "detail": f"{len(q)} qualified batters"})
tests.append({"hypothesis": "WP model calibration", "test": "Brier score (out-of-fold)", "statistic": round(brier, 4),
              "p_value": np.nan, "detail": f"baseline (always predict avg) {base_brier:.4f}; lower is better"})
tests = pd.DataFrame(tests)
tests["p_value"] = tests["p_value"].map(lambda p: p if pd.isna(p) else float(f"{p:.4g}"))
tests["significant_5pct"] = tests["p_value"] < 0.05

# ---------------------------------------------------------------- 9. write outputs
hide = [c for c in df.columns if re.search(r"(_id$|registry|identifier|^row_order$|umpire|referee)", c, re.I) and c != "match_id"]
clean = df.drop(columns=hide)
note("Hide identifiers", f"dropped {len(hide)} ID/official columns from export: {hide}", len(clean))
for c in ["wp_before", "wp_after", "wpa_batting", "runs_above_exp", "rrr_before"]:
    clean[c] = clean[c].round(4)

files = {
    "01_ipl_2022_2025_clean_balls.csv": clean,
    "02_innings_totals.csv": inn.drop(columns="z"),
    "03_matches.csv": m.reset_index(),
    "04_season_phase_trends.csv": season,
    "05_wp_lookup_heatmap.csv": wp_table,
    "06_wp_calibration.csv": calib,
    "07_batters_msi.csv": bb,
    "08_bowlers_msi.csv": bw,
    "09_final_2025_wp_worm.csv": worm,
    "10_final_2025_over_swings.csv": over_swing,
    "11_biggest_swing_moments.csv": moments,
    "12_stat_tests.csv": tests,
}
pd.DataFrame(log).to_csv(f"{OUT}/00_cleaning_log.csv", index=False)
for name, frame in files.items():
    assert len(frame) < 100_000, f"{name} has {len(frame)} rows"
    frame.to_csv(f"{OUT}/{name}", index=False)
shutil.make_archive(OUT, "zip", OUT)

print("\n=== OUTPUT FILES ===")
for name, frame in files.items():
    print(f"{name:40s} {len(frame):>7,} rows")
print("\n=== STAT TESTS ===")
print(tests.to_string(index=False))
print("\n=== TOP 10 BATTERS BY MSI (qualified) ===")
print(bb[bb.qualifies_msi & bb.qualifies_avg][["batter", "batting_avg", "strike_rate", "MSI", "rank_batting_avg",
                                               "rank_msi", "pct_runs_in_decided_states"]].head(10).to_string(index=False))
print("\n=== BIGGEST AVG-vs-MSI RANK GAPS ===")
print(bb.dropna(subset=["rank_gap_avg_minus_msi"]).sort_values("rank_gap_avg_minus_msi")
        [["batter", "batting_avg", "MSI", "rank_batting_avg", "rank_msi", "rank_gap_avg_minus_msi"]]
        .iloc[np.r_[0:5, -5:0]].to_string(index=False))
print(f"\nDone. Download {OUT}.zip")
