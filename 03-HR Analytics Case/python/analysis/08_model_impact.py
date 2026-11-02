r"""
08_model_impact.py — Stage 8b
Translate the logistic regression from 07 into business-facing outputs.

Three deliverables:
  1. Per-employee predicted probability of attrition (risk_scores.csv)
  2. Risk-band diagnostic: does the model discriminate? (console)
  3. What-if impact table: ranked interventions by leavers avoided,
     with an explicit category column (actionable / diagnostic /
     validation_only) so the CSV is self-documenting.

IMPORTANT FRAMING (goes in the report):
  What-if estimates are MODEL-BASED PROJECTIONS from an observational
  regression, not causal effects. Directional guidance, not guarantees.

Run:    py python\analysis\08_model_impact.py
Output: python\outputs\risk_scores.csv
        python\outputs\what_if_impact.csv
        python\outputs\charts\chart08_what_if_impact.png
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
# 1. Rebuild the exact model frame from 07 (same logic, no drift)
# ------------------------------------------------------------------
master = pd.read_csv(f"{IN_DIR}\\hr_master_clean.csv")
att    = pd.read_csv(f"{IN_DIR}\\attendance_employee_summary.csv")

master["tenure_band"] = master["tenure_band"].str.replace(" years", "", regex=False)
master["attrition_flag"] = (master["attrition"] == "Yes").astype(int)

def hours_band(h):
    if pd.isna(h): return None
    if h < 7.5:    return "Short"
    if h < 8.0:    return "Normal"
    return "Long"

att["hours_band"] = att["avg_hours"].apply(hours_band)
df = master.merge(att[["employee_id", "hours_band"]], on="employee_id", how="left")

tenure_map = {"0-1": 1, "2-3": 2, "4-5": 3, "6-10": 4, "10+": 5}
hours_map  = {"Short": 1, "Normal": 2, "Long": 3}

df["tenure_ord"]     = df["tenure_band"].map(tenure_map)
df["hours_ord"]      = df["hours_band"].map(hours_map)
df["tenure_x_hours"] = df["tenure_ord"] * df["hours_ord"]
df["dept_sales"]     = (df["department"] == "Sales").astype(int)
df["dept_hr"]        = (df["department"] == "Human Resources").astype(int)

predictors = [
    "tenure_ord", "hours_ord", "tenure_x_hours",
    "dept_sales", "dept_hr",
    "job_level", "monthly_income", "distance_from_home",
    "num_companies_worked",
    "work_life_balance", "environment_satisfaction",
    "job_satisfaction", "stock_option_level",
]

model_df = df[["employee_id", "tenure_band", "hours_band", "department",
               "attrition_flag"] + predictors].copy()
model_df_clean = model_df.dropna().reset_index(drop=True)

print("=" * 66)
print("STAGE 8b — MODEL IMPACT (probability + what-if)")
print("=" * 66)
print(f"Employees scored    : {len(model_df_clean):,}")
print(f"(Dropped from model : {len(model_df) - len(model_df_clean):,} with nulls)")
print()

# ------------------------------------------------------------------
# 2. Fit the model (identical to 07)
# ------------------------------------------------------------------
X = sm.add_constant(model_df_clean[predictors])
y = model_df_clean["attrition_flag"]
model = sm.Logit(y, X).fit(disp=0)

# ------------------------------------------------------------------
# 3. Per-employee predicted probability
# ------------------------------------------------------------------
probs = model.predict(X)
model_df_clean["predicted_prob"] = probs

def risk_band(p):
    if p >= 0.50: return "High"
    if p >= 0.25: return "Medium"
    return "Low"

model_df_clean["risk_band"] = model_df_clean["predicted_prob"].apply(risk_band)

# ------------------------------------------------------------------
# 4. Risk-band diagnostic — does the model discriminate?
# ------------------------------------------------------------------
print("RISK-BAND DIAGNOSTIC — does the model separate leavers from stayers?")
print("-" * 66)
diag = (model_df_clean.groupby("risk_band")
        .agg(n=("employee_id", "size"),
             actual_leavers=("attrition_flag", "sum"),
             mean_predicted=("predicted_prob", "mean")))
diag["actual_rate_pct"] = 100.0 * diag["actual_leavers"] / diag["n"]
diag["mean_pred_pct"]   = 100.0 * diag["mean_predicted"]
diag = diag.reindex(["High", "Medium", "Low"])
print(diag[["n", "actual_leavers", "actual_rate_pct", "mean_pred_pct"]]
      .round(2).to_string())
print()
print("Interpretation: the model discriminates if actual_rate_pct decreases")
print("monotonically from High -> Medium -> Low, and if mean_pred_pct tracks")
print("actual_rate_pct closely (calibration).")
print()

# ------------------------------------------------------------------
# 5. What-if impact analysis
# ------------------------------------------------------------------
baseline_probs = model_df_clean["predicted_prob"].copy()

def impact(label, mask, mutate_fn):
    """
    Apply mutate_fn to a copy of model_df_clean for rows matching mask,
    recompute predicted probability, and return summary stats.
    """
    if mask.sum() == 0:
        return None
    scenario = model_df_clean.copy()
    scenario.loc[mask, predictors] = mutate_fn(scenario.loc[mask, predictors].copy())
    new_probs = model.predict(sm.add_constant(scenario[predictors], has_constant="add"))

    affected_n       = int(mask.sum())
    baseline_leavers = baseline_probs[mask].sum()
    new_leavers      = new_probs[mask].sum()
    avoided          = baseline_leavers - new_leavers
    avg_drop_pp      = 100.0 * (baseline_probs[mask].mean() - new_probs[mask].mean())

    return {
        "intervention":            label,
        "employees_affected":      affected_n,
        "avg_prob_drop_pp":        round(avg_drop_pp, 2),
        "expected_leavers_before": round(baseline_leavers, 1),
        "expected_leavers_after":  round(new_leavers, 1),
        "leavers_avoided":         round(avoided, 1),
    }

results = []

# --- Intervention 1: cap hours (Long -> Normal) for year-1 employees
mask_long_year1 = (model_df_clean["tenure_band"] == "0-1") & (model_df_clean["hours_band"] == "Long")
def mutate_hours(sub):
    sub["hours_ord"] = 2  # Normal
    sub["tenure_x_hours"] = sub["tenure_ord"] * sub["hours_ord"]
    return sub
results.append(impact("Cap hours in year 1 (Long -> Normal)", mask_long_year1, mutate_hours))

# --- Intervention 2: WLB +1 step for all employees in bad/good WLB
mask_wlb = model_df_clean["work_life_balance"].isin([1, 2])
def mutate_wlb(sub):
    sub["work_life_balance"] = (sub["work_life_balance"] + 1).clip(upper=4)
    return sub
results.append(impact("Improve WLB by 1 step (for Bad/Good)", mask_wlb, mutate_wlb))

# --- Intervention 3: EnvSat +1 step for all employees in Low/Medium
mask_env = model_df_clean["environment_satisfaction"].isin([1, 2])
def mutate_env(sub):
    sub["environment_satisfaction"] = (sub["environment_satisfaction"] + 1).clip(upper=4)
    return sub
results.append(impact("Improve EnvSat by 1 step (for Low/Medium)", mask_env, mutate_env))

# --- Intervention 4: JobSat +1 step for all employees in Low/Medium
mask_job = model_df_clean["job_satisfaction"].isin([1, 2])
def mutate_job(sub):
    sub["job_satisfaction"] = (sub["job_satisfaction"] + 1).clip(upper=4)
    return sub
results.append(impact("Improve JobSat by 1 step (for Low/Medium)", mask_job, mutate_job))

# --- Intervention 5: remove HR department effect (hypothetical)
mask_hr = model_df_clean["dept_hr"] == 1
def mutate_dept(sub):
    sub["dept_hr"] = 0  # pretend HR employees are R&D (reference)
    return sub
results.append(impact("Remove HR dept effect (hypothetical)", mask_hr, mutate_dept))

# --- Intervention 6: tenure protection (pretend everyone gains 1 tenure band)
def mutate_tenure(sub):
    sub["tenure_ord"] = (sub["tenure_ord"] + 1).clip(upper=5)
    sub["tenure_x_hours"] = sub["tenure_ord"] * sub["hours_ord"]
    return sub
mask_all = pd.Series([True] * len(model_df_clean), index=model_df_clean.index)
results.append(impact("Everyone +1 tenure band (hypothetical)", mask_all, mutate_tenure))

results = [r for r in results if r is not None]

# ------------------------------------------------------------------
# 6. Tag each intervention with a category so the CSV is self-documenting
# ------------------------------------------------------------------
categories = {
    "Everyone +1 tenure band (hypothetical)":    "validation_only",
    "Remove HR dept effect (hypothetical)":      "diagnostic",
    "Cap hours in year 1 (Long -> Normal)":      "actionable",
    "Improve EnvSat by 1 step (for Low/Medium)": "actionable",
    "Improve JobSat by 1 step (for Low/Medium)": "actionable",
    "Improve WLB by 1 step (for Bad/Good)":      "actionable",
}
for r in results:
    r["category"] = categories.get(r["intervention"], "other")

impact_df = (pd.DataFrame(results)
             .sort_values("leavers_avoided", ascending=False)
             .reset_index(drop=True))

# Reorder columns so category is visible early
impact_df = impact_df[[
    "category", "intervention", "employees_affected",
    "avg_prob_drop_pp", "expected_leavers_before",
    "expected_leavers_after", "leavers_avoided",
]]

print("WHAT-IF IMPACT TABLE (model-based projections, not causal guarantees)")
print("-" * 66)
print(impact_df.to_string(index=False))
print()

# Save CSVs
model_df_clean[["employee_id", "department", "tenure_band", "hours_band",
                "predicted_prob", "risk_band", "attrition_flag"]].to_csv(
    f"{OUT_DIR}\\risk_scores.csv", index=False)
impact_df.to_csv(f"{OUT_DIR}\\what_if_impact.csv", index=False)
print(f"Saved: {OUT_DIR}\\risk_scores.csv")
print(f"Saved: {OUT_DIR}\\what_if_impact.csv")
print()

# ------------------------------------------------------------------
# 7. Chart — actionable interventions only, ranked
# ------------------------------------------------------------------
plot_df = impact_df[impact_df["category"] == "actionable"].copy()
plot_df = plot_df.iloc[::-1]  # reverse so top-ranked is at top of chart

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(plot_df["intervention"], plot_df["leavers_avoided"],
               color="#c0392b", height=0.6, zorder=2)

for bar, (_, row) in zip(bars, plot_df.iterrows()):
    ax.text(row["leavers_avoided"] + 1.5,
            bar.get_y() + bar.get_height()/2,
            f"{row['leavers_avoided']:.1f} avoided "
            f"(n={row['employees_affected']:,}, "
            f"-{row['avg_prob_drop_pp']:.1f}pp)",
            va="center", fontsize=9)

ax.set_xlabel("Expected leavers avoided per year (model-based projection)")
ax.set_title("Actionable Interventions Ranked by Expected Leavers Avoided\n"
             "Model-based projections — directional, not causal guarantees\n"
             "(hypothetical / diagnostic rows excluded)")
ax.set_xlim(0, plot_df["leavers_avoided"].max() * 1.55)
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(f"{CH_DIR}\\chart08_what_if_impact.png", dpi=150)
plt.close(fig)
print(f"Saved: {CH_DIR}\\chart08_what_if_impact.png")