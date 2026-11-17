"""
07_track_c_model.py — Step 7: Logistic regression for Track C.

Goal: turn the C5 shop-visit finding into a quantified coefficient that can
      support a supervisor recommendation. The model is inferential, not
      predictive — odds ratios are the deliverable, not AUC.

Tracks A and B are not modelled. Their Step 5 evidence base showed no
signal in the features:
  - Track A: 26 positives, leavers indistinguishable from actives (A8).
  - Track B: 55.39% late rate invariant across every segment (B1-B10).
Modelling either would produce coefficients that are artifacts of the model,
not the data. Step 6 validated this — the SQL findings agree with pandas
exactly, so the "no signal" conclusion is not a SQL artifact.

Run with: py -3.12 python/analysis/07_track_c_model.py
Exit codes:
  0  — model fit and all outputs written
  1  — fit failed or sanity check triggered (STOP and investigate)
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
import os
import sys

# === CONFIG ===
PROJECT   = r"C:\Users\Anonymous\Desktop\projects\04-Logistics Operations Database"
PROCESSED = os.path.join(PROJECT, "data", "processed")
OUTPUTS   = os.path.join(PROJECT, "python", "outputs")
LOG_PATH  = os.path.join(OUTPUTS, "07_model_report.txt")

log_lines = []

def log(text=""):
    print(text)
    log_lines.append(str(text))
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

log("=" * 75)
log("STEP 7 — TRACK C LOGISTIC REGRESSION")
log("=" * 75)
log()

# ============================================================================
# 1. LOAD AND ENGINEER FEATURES
# ============================================================================
log("=" * 75)
log("1. DATA PREPARATION")
log("=" * 75)
log()

df = pd.read_csv(os.path.join(PROCESSED, "master_truck_month_clean.csv"))
log(f"Loaded master_truck_month_clean.csv: {len(df):,} rows")
log()

# Feature engineering
df["had_preventive_visit"] = (df["n_preventive"] >= 1).astype(int)
df["is_old_truck"]         = (df["truck_age_years"] >= 8).astype(int)
df["make_premium"]         = df["make"].isin(["Peterbilt", "Kenworth"]).astype(int)
df["total_miles_k"]        = df["total_miles"] / 1000.0

FEATURES = [
    "had_preventive_visit",
    "truck_age_years",
    "is_old_truck",
    "total_miles_k",
    "downtime_hours",
    "utilization_rate",
    "make_premium",
]
TARGET = "high_maintenance_flag"

log("Feature construction:")
log(f"  had_preventive_visit : 1 if n_preventive >= 1, else 0")
log(f"  is_old_truck         : 1 if truck_age_years >= 8, else 0")
log(f"  make_premium         : 1 if make in [Peterbilt, Kenworth], else 0")
log(f"  total_miles_k        : total_miles / 1000")
log()

# Class balance
n_pos = int(df[TARGET].sum())
n_neg = len(df) - n_pos
log(f"Target '{TARGET}': {n_pos:,} positive / {len(df):,} total = {n_pos*100.0/len(df):.2f}%")
log(f"Class ratio (negative / positive): {n_neg / n_pos:.2f}")
log(f"Events per feature: {n_pos / len(FEATURES):.1f} (rule of thumb: >= 10)")
log()

# Univariate summary
log("Feature univariate summary:")
log(df[FEATURES + [TARGET]].describe().round(3).to_string())
log()

# Null check — no model feature should have nulls
nulls = df[FEATURES + [TARGET]].isnull().sum()
if nulls.sum() > 0:
    log("WARNING — features with nulls:")
    log(nulls[nulls > 0].to_string())
    log("Listwise deletion will be applied to remaining rows.")
    df_model = df.dropna(subset=FEATURES + [TARGET]).copy()
    log(f"Rows before listwise deletion: {len(df):,}")
    log(f"Rows after  listwise deletion: {len(df_model):,}")
else:
    log("Null check: no nulls in any model feature or target.")
    df_model = df.copy()
log()

# ============================================================================
# 2. VIF CHECK (multicollinearity pre-flight)
# ============================================================================
log("=" * 75)
log("2. MULTICOLLINEARITY PRE-CHECK (VIF)")
log("=" * 75)
log()

X_vif = df_model[FEATURES].copy()
X_vif = sm.add_constant(X_vif)
vif_data = pd.DataFrame({
    "feature": X_vif.columns,
    "VIF":     [variance_inflation_factor(X_vif.values, i)
                for i in range(X_vif.shape[1])]
})
vif_data = vif_data[vif_data["feature"] != "const"]
vif_data["VIF"] = vif_data["VIF"].round(2)
log(vif_data.to_string(index=False))
log()

high_vif = vif_data[vif_data["VIF"] > 5]
if len(high_vif) > 0:
    log("WARNING — features with VIF > 5 (multicollinearity):")
    log(high_vif.to_string(index=False))
    log("Proceeding with the model; the collinearity will be noted in Limitations.")
else:
    log("All VIF < 5 — no multicollinearity concern.")
log()

# ============================================================================
# 3. FIT THE MODEL
# ============================================================================
log("=" * 75)
log("3. LOGISTIC REGRESSION FIT")
log("=" * 75)
log()

X = df_model[FEATURES].copy()
# Add the interaction: had_preventive_visit x downtime_hours
X["prev_x_downtime"] = X["had_preventive_visit"] * X["downtime_hours"]
y = df_model[TARGET].astype(int)

X_const = sm.add_constant(X)
log(f"Design matrix shape: {X_const.shape}")
log(f"Target shape       : {y.shape}")
log()

try:
    model  = sm.Logit(y, X_const).fit(disp=False)
except Exception as e:
    log(f"FATAL — model fit failed: {e}")
    sys.exit(1)

log(model.summary().as_text())
log()

# ============================================================================
# 4. ODDS RATIO TABLE
# ============================================================================
log("=" * 75)
log("4. ODDS RATIO TABLE")
log("=" * 75)
log()

params  = model.params
conf    = model.conf_int()
pvalues = model.pvalues

or_table = pd.DataFrame({
    "feature":   params.index,
    "coef":      params.round(4).values,
    "odds_ratio": np.exp(params).round(4).values,
    "ci_lower":  np.exp(conf[0]).round(4).values,
    "ci_upper":  np.exp(conf[1]).round(4).values,
    "p_value":   pvalues.round(4).values,
    "significant_at_05": (pvalues < 0.05).values,
})
log(or_table.to_string(index=False))
log()

# Plain-English translation of each OR
log("Plain-English interpretation:")
log()
for _, row in or_table.iterrows():
    if row["feature"] == "const":
        continue
    direction = "more likely" if row["odds_ratio"] > 1 else "less likely"
    pct_change = (row["odds_ratio"] - 1) * 100
    sig_word = "significant" if row["significant_at_05"] else "NOT significant"
    log(f"  {row['feature']:<25} : OR = {row['odds_ratio']:.3f}  "
        f"({pct_change:+.1f}% {direction})  — {sig_word} (p = {row['p_value']:.4f})")
log()

# ============================================================================
# 5. RISK-BAND CALIBRATION
# ============================================================================
log("=" * 75)
log("5. RISK-BAND CALIBRATION")
log("=" * 75)
log()

df_model["predicted_prob"] = model.predict(X_const)

# Decile bands
df_model["pred_decile"] = pd.qcut(
    df_model["predicted_prob"], q=10, labels=False, duplicates="drop"
)
calibration = df_model.groupby("pred_decile").agg(
    truck_months=("predicted_prob", "count"),
    predicted_rate=("predicted_prob", "mean"),
    observed_rate=(TARGET, "mean"),
).reset_index()
calibration["predicted_rate"] = (calibration["predicted_rate"] * 100).round(2)
calibration["observed_rate"]  = (calibration["observed_rate"]  * 100).round(2)
calibration["gap_pp"]         = (calibration["observed_rate"] - calibration["predicted_rate"]).round(2)

log("Decile | Truck-months | Predicted % | Observed % | Gap (pp)")
log("-" * 65)
for _, row in calibration.iterrows():
    log(f"  {int(row['pred_decile']):>2}   | {int(row['truck_months']):>6,}       "
        f"| {row['predicted_rate']:>6.2f}      | {row['observed_rate']:>6.2f}    "
        f"| {row['gap_pp']:>+6.2f}")
log()

top_decile_obs = calibration.loc[calibration["pred_decile"] == calibration["pred_decile"].max(), "observed_rate"].iloc[0]
bot_decile_obs = calibration.loc[calibration["pred_decile"] == 0, "observed_rate"].iloc[0]
log(f"Top decile observed high-maint rate : {top_decile_obs:.2f}%")
log(f"Bottom decile observed high-maint rate: {bot_decile_obs:.2f}%")
log(f"Discrimination gap (top - bottom)   : {top_decile_obs - bot_decile_obs:+.2f} pp")
log()

# ============================================================================
# 6. WHAT-IF SIMULATION
# ============================================================================
log("=" * 75)
log("6. WHAT-IF SIMULATION — shift 10% of zero-visit months into preventive")
log("=" * 75)
log()

# Baseline predictions
df_model["baseline_pred"] = model.predict(X_const)

# Intervention: reassign 10% of the zero-preventive months to had_preventive = 1
zero_visit_mask = df_model["had_preventive_visit"] == 0
n_zero_visit    = int(zero_visit_mask.sum())
n_to_shift      = int(round(n_zero_visit * 0.10))

log(f"Zero-preventive months in sample : {n_zero_visit:,}")
log(f"10% to shift into preventive     : {n_to_shift:,}")
log()

# Deterministic selection: first n_to_shift zero-visit months (by truck_id, month)
shift_idx = df_model[zero_visit_mask].sort_values(["truck_id", "month"]).head(n_to_shift).index

X_intervention = X_const.copy()
X_intervention.loc[shift_idx, "had_preventive_visit"] = 1
X_intervention.loc[shift_idx, "prev_x_downtime"]      = (
    X_intervention.loc[shift_idx, "had_preventive_visit"]
    * X_intervention.loc[shift_idx, "downtime_hours"]
)

df_model["intervention_pred"] = model.predict(X_intervention)

# Business-impact calculation
baseline_expected = df_model["baseline_pred"].sum()
intervention_expected = df_model["intervention_pred"].sum()
delta_expected = intervention_expected - baseline_expected

baseline_flagged = int((df_model["baseline_pred"] >= 0.5).sum())
intervention_flagged = int((df_model["intervention_pred"] >= 0.5).sum())
delta_flagged = intervention_flagged - baseline_flagged

AVG_HIGH_COST = 4052.45   # from C1: avg cost of a high-maintenance month
delta_cost = delta_expected * AVG_HIGH_COST

log("Predicted expected high-maint months (sum of probabilities):")
log(f"  Baseline        : {baseline_expected:>10.1f} expected months")
log(f"  Intervention    : {intervention_expected:>10.1f} expected months")
log(f"  Delta           : {delta_expected:>+10.1f} expected months")
log()
log("Predicted high-maint months at threshold 0.5:")
log(f"  Baseline        : {baseline_flagged:>10,} months")
log(f"  Intervention    : {intervention_flagged:>10,} months")
log(f"  Delta           : {delta_flagged:>+10,} months")
log()
log(f"Cost translation (avg high-maint month = ${AVG_HIGH_COST:,.2f} from C1):")
log(f"  Expected-month delta × avg cost = ${delta_cost:+,.0f}")
log()
log("CAVEAT: This is a causal projection built on an observational model.")
log("        The 'intervention' assumes the model captures a causal effect of")
log("        preventive visits, not a mere correlation. See Limitations.")
log()

# ============================================================================
# 7. MODEL DIAGNOSTICS
# ============================================================================
log("=" * 75)
log("7. MODEL DIAGNOSTICS")
log("=" * 75)
log()

log(f"Pseudo R-squared (McFadden)   : {model.prsquared:.4f}")
log(f"AIC                            : {model.aic:.2f}")
log(f"LL Ratio (model vs null)       : {model.llr:.2f}")
log(f"LL Ratio p-value               : {model.llr_pvalue:.4e}")
log(f"Number of observations         : {int(model.nobs):,}")
log(f"Number of features (incl const): {len(model.params)}")
log()

if model.prsquared < 0.02:
    verdict = "WEAK — model may not be informative. Consider descriptive fallback."
elif model.prsquared > 0.30:
    verdict = "SUSPICIOUSLY HIGH — possible overfit or proxy feature. Investigate."
else:
    verdict = "REASONABLE for operational logistic regression (0.05-0.15 is normal)."

log(f"Verdict on Pseudo R-squared    : {verdict}")
log()

# ============================================================================
# 8. FINAL SUMMARY
# ============================================================================
log("=" * 75)
log("8. FINAL SUMMARY")
log("=" * 75)
log()

top_or = or_table[or_table["feature"] != "const"].sort_values("odds_ratio", ascending=False).iloc[0]
log(f"Strongest positive predictor : {top_or['feature']} (OR = {top_or['odds_ratio']:.3f})")
log(f"Model discriminative range   : {top_decile_obs - bot_decile_obs:+.2f} pp (top decile - bottom decile)")
log(f"What-if cost impact          : ${delta_cost:+,.0f}")
log(f"Report saved                 : {LOG_PATH}")
log()
log("STATUS: Step 7 complete. Review the odds ratio table and calibration before")
log("        writing the executive summary in Step 9.")