# Validation Report — SQL vs Python

**Purpose:** Independently recompute the critical Stage 6 SQL findings in
Python/pandas. Every number below was produced twice — once by SQLite
(`sql/analysis/`) and once by pandas (`python/analysis/05_validate_sql.py`).
All checks pass with zero difference.

**Script:** `python/analysis/05_validate_sql.py`
**Data source:** `data/processed/hr_master_clean.csv` (4,410 × 28),
`data/processed/attendance_employee_summary.csv` (4,410 × 8)

---

## Results

| Check | Python | SQL | Diff | Status |
|---|---|---|---|---|
| Overall attrition rate (%) | 16.12 | 16.12 | 0.00 | ✅ |
| Overall leavers (n) | 711 | 711 | 0 | ✅ |
| Overall total (n) | 4,410 | 4,410 | 0 | ✅ |
| 0-1 × Long — employees | 215 | 215 | 0 | ✅ |
| 0-1 × Long — leavers | 117 | 117 | 0 | ✅ |
| 0-1 × Long — rate (%) | 54.42 | 54.42 | 0.00 | ✅ |
| R&D × 0-1 × Long — employees | 135 | 135 | 0 | ✅ |
| R&D × 0-1 × Long — leavers | 77 | 77 | 0 | ✅ |
| R&D × 0-1 × Long — rate (%) | 57.04 | 57.04 | 0.00 | ✅ |
| HR × 0-1 × Short — employees | 24 | 24 | 0 | ✅ |
| HR × 0-1 × Short — leavers | 15 | 15 | 0 | ✅ |
| HR × 0-1 × Short — rate (%) | 62.50 | 62.50 | 0.00 | ✅ |

**Result: ALL CHECKS PASS.**

---

## Bug caught during validation

The first run of the validation script returned `0` on all cell checks while
overall checks passed. Diagnosis: `tenure_band` in `hr_master_clean.csv` is
stored as `"0-1 years"` etc., but the pandas filter used `"0-1"`. The
mismatch silently produced empty cells.

- **SQL was correct** (it reads `tenure_band` as-is from the CSV).
- **The bug was in the validation script** — the fix was a one-line
  string normalization: `master["tenure_band"].str.replace(" years", "", regex=False)`.
- **Lesson:** when overall checks pass but cell-level checks return 0,
  the data is fine — suspect the filter, not the data.

---

## What this proves

> "The Stage 6 findings are not an artifact of how I wrote the SQL.
> Every critical number was reproduced independently in pandas, and all
> 12 checks matched to 0.00 difference."


---

## Stage 8 — Regression cross-check

The logistic regression (07) and its impact translation (08) were
built from `hr_master_clean.csv` + `attendance_employee_summary.csv`,
using the same bandings and null-handling as the SQL analysis.

- Overall attrition on the modelled sample (n=4,308): **16.18%** vs
  full-sample 16.12%. The 0.06pp difference reflects listwise deletion.
- Year-1 × Long cell (n=211 in model vs 215 in SQL): consistent —
  the 4-row gap is null drops.
- Model fit (pseudo-R² = 0.14) is consistent with a mid-strength
  attrition signal, matching the Stage 6 effect sizes.

**No SQL-Python divergence.**