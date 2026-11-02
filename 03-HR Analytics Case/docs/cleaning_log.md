# Cleaning Log — HR Analytics Attrition Case Study

**Stage:** 3 — Data Cleaning & Preprocessing  
**Input:** `general_data.csv`, `employee_survey_data.csv`, `manager_survey_data.csv`  
**Output:** `data/processed/hr_master_clean.csv`  
**Script:** `python/analysis/03_clean_master.py`

---

## 1. Summary of Transformations

| Step | Transformation | Rows affected | Columns affected |
|---|---|---|---|
| 3.1 | Loaded 3 raw master files | 4,410 each | — |
| 3.2 | Dropped constant columns | 0 | −3 (`EmployeeCount`, `Over18`, `StandardHours`) |
| 3.3 | Merged 3 files (1:1 inner join on `EmployeeID`) | 0 | combined |
| 3.4 | Renamed columns to snake_case | 0 | all |
| 3.5 | Derived `attrition_flag` (0/1) | 0 | +1 |
| 3.6 | Derived `tenure_band` | 0 | +1 |
| 3.7 | Validated row count, null counts, no dupes | 0 | — |
| 3.8 | Exported to CSV | — | — |

---

## 2. Row Count Preservation

| Stage | Rows |
|---|---|
| general (raw) | 4410 |
| employee_survey (raw) | 4410 |
| manager_survey (raw) | 4410 |
| **merged + cleaned** | **4410** |

No rows were added or removed at any step. Every one of the 4,410 employees is present in the output.

---

## 3. Columns Dropped

| Column | Reason |
|---|---|
| `EmployeeCount` | Constant = 1 (Stage 2 §3) |
| `Over18` | Constant = 'Y' (Stage 2 §3) |
| `StandardHours` | Constant = 8 (Stage 2 §3) |

Constant columns cannot differentiate, segment, or predict anything. Their removal is a documented decision, not a default.

---

## 4. Null Values Preserved

| Column | Nulls in output |
|---|---|
| `work_life_balance` | 38 ✅ |
| `environment_satisfaction` | 25 ✅ |
| `job_satisfaction` | 20 ✅ |
| `num_companies_worked` | 19 ✅ |
| `total_working_years` | 9 ✅ |

No nulls were imputed or removed. This decision was made in Stage 2 §6 based on the discovery that missingness in `job_satisfaction` is informative (associated with a 11.17pp lower attrition rate). Imputing would erase that signal.

---

## 5. Derived Columns

### `attrition_flag`

- Type: integer (0 or 1)
- Derivation: `1` if `attrition == 'Yes'`, else `0`
- Purpose: numeric aggregation in SQL / Python / Power BI
- The original string column `attrition` is preserved for readability

### `tenure_band`

- Type: categorical (ordered)
- Bands: `0-1 years`, `2-3 years`, `4-5 years`, `6-10 years`, `10+ years`
- Derivation: `pd.cut(years_at_company, [-1, 1, 3, 5, 10, 100])`
- Purpose: HR-standard tenure segmentation; simplifies grouping in SQL and enables a clean Power BI slicer

---

## 6. Column Name Standardization

All column names converted to `snake_case` for portability across SQL, Python, and Power BI. Examples:

| Original | Standardized |
|---|---|
| `EmployeeID` | `employee_id` |
| `DistanceFromHome` | `distance_from_home` |
| `MonthlyIncome` | `monthly_income` |
| `NumCompaniesWorked` | `num_companies_worked` |
| `YearsWithCurrManager` | `years_with_curr_manager` |

---

## 7. Final Schema

**Rows:** 4410  
**Columns:** 28

| # | Column | Dtype |
|---|---|---|
| 1 | `age` | `int64` |
| 2 | `attrition` | `str` |
| 3 | `business_travel` | `str` |
| 4 | `department` | `str` |
| 5 | `distance_from_home` | `int64` |
| 6 | `education` | `int64` |
| 7 | `education_field` | `str` |
| 8 | `employee_id` | `int64` |
| 9 | `gender` | `str` |
| 10 | `job_level` | `int64` |
| 11 | `job_role` | `str` |
| 12 | `marital_status` | `str` |
| 13 | `monthly_income` | `int64` |
| 14 | `num_companies_worked` | `float64` |
| 15 | `percent_salary_hike` | `int64` |
| 16 | `stock_option_level` | `int64` |
| 17 | `total_working_years` | `float64` |
| 18 | `training_times_last_year` | `int64` |
| 19 | `years_at_company` | `int64` |
| 20 | `years_since_last_promotion` | `int64` |
| 21 | `years_with_curr_manager` | `int64` |
| 22 | `environment_satisfaction` | `float64` |
| 23 | `job_satisfaction` | `float64` |
| 24 | `work_life_balance` | `float64` |
| 25 | `job_involvement` | `int64` |
| 26 | `performance_rating` | `int64` |
| 27 | `attrition_flag` | `int64` |
| 28 | `tenure_band` | `category` |

---

## 8. Decisions Deferred to Later Stages

| Decision | Stage |
|---|---|
| Build dimension tables for coded categoricals (`education`, `job_satisfaction`, etc.) | Stage 5 |
| Process attendance data (`in_time.csv`, `out_time.csv`) | Stage 4 |
| Handle nulls per-analysis (never impute) | Stages 6–7 |

---

## 9. Validation Results

All Stage 3 validation checks passed:

- Row count = 4410 (unchanged from raw)
- No duplicate `employee_id`
- No null `employee_id`
- Null counts in affected columns match Stage 2 audit exactly
- Constant columns successfully removed
- `attrition_flag` consistent with `attrition` string
- `tenure_band` assigned to all rows

