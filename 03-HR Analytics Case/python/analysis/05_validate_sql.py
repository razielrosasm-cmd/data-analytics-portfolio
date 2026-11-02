"""
05_validate_sql.py — Stage 7.1
Recompute the 4 critical Stage 6 SQL numbers in pandas and compare.

SQL source files validated against:
  - 01_attrition_overview.sql   -> overall rate
  - 08a_tenure_x_hours_overlap  -> 0-1 x Long cell
  - 08d_high_risk_cells_by_department -> R&D x 0-1 x Long, HR x 0-1 x Short
"""

import pandas as pd

# ------------------------------------------------------------------
# 1. Load
# ------------------------------------------------------------------
BASE = r"C:\Users\Anonymous\Desktop\projects\03-HR Analytics Case"
master = pd.read_csv(f"{BASE}\\data\\processed\\hr_master_clean.csv")
# Normalize tenure_band to short form ("0-1 years" -> "0-1")
master["tenure_band"] = master["tenure_band"].str.replace(" years", "", regex=False)
att = pd.read_csv(f"{BASE}\\data\\processed\\attendance_employee_summary.csv")

# ------------------------------------------------------------------
# 2. Independent attrition_flag (do NOT trust the CSV's derived col)
# ------------------------------------------------------------------
master["attrition_flag_check"] = (master["attrition"] == "Yes").astype(int)

# Sanity: the CSV's own flag must agree with our independent one
if "attrition_flag" in master.columns:
    disagreement = (master["attrition_flag"] != master["attrition_flag_check"]).sum()
    assert disagreement == 0, f"attrition_flag mismatch on {disagreement} rows"

# ------------------------------------------------------------------
# 3. Hours band — replicate SQL CASE logic exactly
#    <7.5  -> 'Short'
#    7.5-8 -> 'Normal'
#    >= 8  -> 'Long'
# ------------------------------------------------------------------
def hours_band(h):
    if pd.isna(h):
        return None
    if h < 7.5:
        return "Short"
    if h < 8.0:
        return "Normal"
    return "Long"

att["hours_band"] = att["avg_hours"].apply(hours_band)

# ------------------------------------------------------------------
# 4. Merge attendance onto master (LEFT — nulls stay null, never dropped)
# ------------------------------------------------------------------
df = master.merge(att[["employee_id", "avg_hours", "hours_band"]],
                  on="employee_id", how="left")

# ==================================================================
# CHECK 1 — Overall attrition rate
# ==================================================================
total     = len(df)
leavers   = int(df["attrition_flag_check"].sum())
rate_pct  = round(100.0 * leavers / total, 2)

# ==================================================================
# CHECK 2 — 0-1 x Long cell
# ==================================================================
cell_01_long = df[(df["tenure_band"] == "0-1") & (df["hours_band"] == "Long")]
n_01_long    = len(cell_01_long)
lv_01_long   = int(cell_01_long["attrition_flag_check"].sum())
rt_01_long   = round(100.0 * lv_01_long / n_01_long, 2) if n_01_long else 0.0

# ==================================================================
# CHECK 3 — R&D x 0-1 x Long
# ==================================================================
cell_rd = cell_01_long[cell_01_long["department"] == "Research & Development"]
n_rd    = len(cell_rd)
lv_rd   = int(cell_rd["attrition_flag_check"].sum())
rt_rd   = round(100.0 * lv_rd / n_rd, 2) if n_rd else 0.0

# ==================================================================
# CHECK 4 — HR x 0-1 x Short
# ==================================================================
cell_hr = df[(df["tenure_band"] == "0-1")
             & (df["hours_band"] == "Short")
             & (df["department"] == "Human Resources")]
n_hr    = len(cell_hr)
lv_hr   = int(cell_hr["attrition_flag_check"].sum())
rt_hr   = round(100.0 * lv_hr / n_hr, 2) if n_hr else 0.0

# ==================================================================
# 5. Compare to SQL handoff numbers and print PASS/FAIL
# ==================================================================
checks = [
    # name,                       python value, sql value, tol
    ("Overall rate (%)",           rate_pct,     16.12,     0.01),
    ("Overall leavers (n)",        leavers,      711,       0),
    ("Overall total (n)",          total,        4410,      0),
    ("0-1 x Long  emp (n)",        n_01_long,    215,       0),
    ("0-1 x Long  leavers (n)",    lv_01_long,   117,       0),
    ("0-1 x Long  rate (%)",       rt_01_long,   54.42,     0.01),
    ("R&D x 0-1 x Long emp (n)",   n_rd,         135,       0),
    ("R&D x 0-1 x Long leavers",   lv_rd,        77,        0),
    ("R&D x 0-1 x Long rate (%)",  rt_rd,        57.04,     0.01),
    ("HR  x 0-1 x Short emp (n)",  n_hr,         24,        0),
    ("HR  x 0-1 x Short leavers",  lv_hr,        15,        0),
    ("HR  x 0-1 x Short rate (%)", rt_hr,        62.50,     0.01),
]

print(f"{'CHECK':<32} {'PYTHON':>10} {'SQL':>10} {'DIFF':>10} {'STATUS':>8}")
print("-" * 74)
all_pass = True
for name, py, sql, tol in checks:
    diff = abs(py - sql)
    ok   = diff <= tol
    all_pass = all_pass and ok
    print(f"{name:<32} {py:>10} {sql:>10} {diff:>10.2f} {'PASS' if ok else 'FAIL':>8}")
print("-" * 74)
print("RESULT:", "ALL CHECKS PASS" if all_pass else "MISMATCHES FOUND — DO NOT PROCEED TO CHARTS")