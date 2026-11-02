"""
07_logistic_regression.py — Stage 8
Logistic regression: which factors are statistically associated with attrition?

Framing (Section 9): ASSOCIATION, not prediction.
  - Reports odds ratios + 95% CIs.
  - Not "accuracy" — the dataset is ~16% leavers, so accuracy is a misleading metric.
  - Includes the tenure x hours interaction term (08a proved it exists).

Run:    py python\analysis\07_logistic_regression.py
Output: python\outputs\odds_ratios.csv
        python\outputs\charts\chart07_odds_ratios.png
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

# ------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------
BASE    = r"C:\Users\Anonymous\Desktop\projects\03-HR Analytics Case"
IN_DIR  = f"{BASE}\\data\\processed"
OUT_DIR = f"{BASE}\\python\\outputs"
CH_DIR  = f"{OUT_DIR}\\charts"
os.makedirs(CH_DIR, exist_ok=True)

# ------------------------------------------------------------------
# 1. Load + build modelling frame
# ------------------------------------------------------------------
master = pd.read_csv(f"{IN_DIR}\\hr_master_clean.csv")
att    = pd.read_csv(f"{IN_DIR}\\attendance_employee_summary.csv")

# Normalize tenure_band so ordinals work regardless of " years" suffix
master["tenure_band"] = master["tenure_band"].str.replace(" years", "", regex=False)
master["attrition_flag"] = (master["attrition"] == "Yes").astype(int)

# Hours band on attendance_summary
def hours_band(h):
    if pd.isna(h): return None
    if h < 7.5:    return "Short"
    if h < 8.0:    return "Normal"
    return "Long"

att["hours_band"] = att["avg_hours"].apply(hours_band)

df = master.merge(att[["employee_id", "hours_band"]], on="employee_id", how="left")

# Ordinal encodings
tenure_map = {"0-1": 1, "2-3": 2, "4-5": 3, "6-10": 4, "10+": 5}
hours_map  = {"Short": 1, "Normal": 2, "Long": 3}

df["tenure_ord"] = df["tenure_band"].map(tenure_map)
df["hours_ord"]  = df["hours_band"].map(hours_map)
df["tenure_x_hours"] = df["tenure_ord"] * df["hours_ord"]

# Department dummies (R&D = reference)
df["dept_sales"] = (df["department"] == "Sales").astype(int)
df["dept_hr"]    = (df["department"] == "Human Resources").astype(int)

# ------------------------------------------------------------------
# 2. Build model frame, listwise deletion (no imputation, decision #2)
# ------------------------------------------------------------------
predictors = [
    "tenure_ord", "hours_ord", "tenure_x_hours",
    "dept_sales", "dept_hr",
    "job_level", "monthly_income", "distance_from_home",
    "num_companies_worked",
    "work_life_balance", "environment_satisfaction",
    "job_satisfaction", "stock_option_level",
]

frame_cols = ["attrition_flag"] + predictors
model_df = df[frame_cols].copy()

n_before = len(model_df)
null_mask = model_df.isna().any(axis=1)
dropped = model_df[null_mask]
model_df_clean = model_df[~null_mask].copy()
n_after = len(model_df_clean)

dropped_attrition_rate = 100.0 * dropped["attrition_flag"].mean() if len(dropped) else 0.0
retained_attrition_rate = 100.0 * model_df_clean["attrition_flag"].mean()

print("=" * 62)
print("STAGE 8 — LOGISTIC REGRESSION (association, not prediction)")
print("=" * 62)
print(f"Rows before listwise deletion : {n_before:,}")
print(f"Rows dropped (any null)       : {len(dropped):,}")
print(f"Rows retained for model       : {n_after:,}")
print(f"Attrition rate — dropped rows  : {dropped_attrition_rate:5.2f}%")
print(f"Attrition rate — retained rows : {retained_attrition_rate:5.2f}%")
print(f"Company benchmark              :  16.12%")
print()

# ------------------------------------------------------------------
# 3. Fit
# ------------------------------------------------------------------
X = model_df_clean[predictors]
y = model_df_clean["attrition_flag"]
X = sm.add_constant(X)

model  = sm.Logit(y, X).fit(disp=0)
params = model.params
conf   = model.conf_int()
pvals  = model.pvalues

# Odds ratios + CIs
or_table = pd.DataFrame({
    "predictor":   params.index,
    "coef":        params.values,
    "odds_ratio":  np.exp(params.values),
    "ci_lower":    np.exp(conf[0].values),
    "ci_upper":    np.exp(conf[1].values),
    "p_value":     pvals.values,
})
or_table["significant_05"] = or_table["p_value"] < 0.05

print("Model fit")
print("-" * 62)
print(f"Pseudo R² (McFadden) : {model.prsquared:.4f}")
print(f"Log-Likelihood       : {model.llf:.2f}")
print(f"LLR p-value          : {model.llr_pvalue:.2e}")
print(f"n_obs                : {int(model.nobs):,}")
print()

print("Odds ratios (95% CI)")
print("-" * 62)
fmt = or_table.copy()
fmt["odds_ratio"] = fmt["odds_ratio"].map(lambda v: f"{v:6.3f}")
fmt["ci"]         = or_table.apply(lambda r: f"[{r['ci_lower']:.2f} – {r['ci_upper']:.2f}]", axis=1)
fmt["p"]          = fmt["p_value"].map(lambda v: f"{v:.3e}" if v < 0.001 else f"{v:.3f}")
fmt["sig"]        = fmt["significant_05"].map({True: "*", False: ""})
print(fmt[["predictor", "odds_ratio", "ci", "p", "sig"]].to_string(index=False))
print()
print("Interpretation:")
print("  OR > 1 = higher odds of attrition")
print("  OR < 1 = lower odds of attrition")
print("  * = significant at p<0.05")
print()

# ------------------------------------------------------------------
# 4. Save CSV
# ------------------------------------------------------------------
csv_path = f"{OUT_DIR}\\odds_ratios.csv"
or_table.to_csv(csv_path, index=False)
print(f"Saved: {csv_path}")

# ------------------------------------------------------------------
# 5. Forest plot
# ------------------------------------------------------------------
plot_df = or_table[or_table["predictor"] != "const"].copy().sort_values("odds_ratio")
plot_df = plot_df.iloc[::-1]  # so highest OR is at top

fig, ax = plt.subplots(figsize=(10, 7))
y_pos  = np.arange(len(plot_df))
colors = ["#c0392b" if s else "#95a5a6" for s in plot_df["significant_05"]]

ax.errorbar(
    plot_df["odds_ratio"], y_pos,
    xerr=[plot_df["odds_ratio"] - plot_df["ci_lower"],
          plot_df["ci_upper"] - plot_df["odds_ratio"]],
    fmt="o", color="#2c3e50", ecolor="#7f8c8d",
    elinewidth=1.5, capsize=3, markersize=7,
)
for i, (_, row) in enumerate(plot_df.iterrows()):
    ax.scatter(row["odds_ratio"], i, color=colors[i], s=90, zorder=3)

ax.axvline(1.0, color="#7f8c8d", linestyle="--", linewidth=1.2)
ax.set_yticks(y_pos)
ax.set_yticklabels(plot_df["predictor"])
ax.set_xscale("log")
ax.set_xlabel("Odds Ratio (log scale) — 95% CI")
ax.set_title("Which Factors Are Associated With Attrition?\n"
             "Odds ratios with 95% CI — red = significant at p<0.05")
ax.grid(True, axis="x", alpha=0.3)

# Annotate OR + CI to the right of the marker
for i, (_, row) in enumerate(plot_df.iterrows()):
    label = f"OR {row['odds_ratio']:.2f} [{row['ci_lower']:.2f}–{row['ci_upper']:.2f}]"
    xpos = plot_df["ci_upper"].max() * 1.05 if row["ci_upper"] > 0 else 1
    ax.text(xpos, i, label, va="center", fontsize=8, color="#2c3e50")

ax.set_xlim(left=plot_df["ci_lower"].min() * 0.8,
            right=plot_df["ci_upper"].max() * 2.2)
fig.tight_layout()
fig.savefig(f"{CH_DIR}\\chart07_odds_ratios.png", dpi=150)
plt.close(fig)
print(f"Saved: {CH_DIR}\\chart07_odds_ratios.png")