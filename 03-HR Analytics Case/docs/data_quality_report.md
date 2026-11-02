# Data Quality Report — HR Analytics Attrition Case Study

**Project:** HR Analytics — Employee Attrition Case Study  
**Stage:** 2 — Data Profiling & Quality Audit  
**Source files:** `general_data.csv`, `employee_survey_data.csv`, `manager_survey_data.csv`, `in_time.csv`, `out_time.csv`  
**Date:** (auto-generated)

---

## 1. Executive Summary

The raw HR dataset is unusually clean for a real-world dataset. All three master files (general, employee survey, manager survey) contain exactly **4,410 rows** with **4,410 unique EmployeeIDs**, no duplicates, and no null IDs. The intersection of EmployeeIDs across all files equals the union, meaning a clean 1:1 join is possible with zero orphans.

The data is not perfect, however. Three constant columns carry no analytical value, ~2.5% of employees have at least one missing survey or tenure value, and several columns that *look* numeric are actually coded categoricals. Each issue is documented below with the decision it drives for Stage 3 (cleaning).

---

## 2. File Inventory & Joinability

| File | Rows | Unique IDs | Duplicate IDs | Null IDs |
|---|---|---|---|---|
| general | 4410 | 4410 | 0 | 0 |
| employee_survey | 4410 | 4410 | 0 | 0 |
| manager_survey | 4410 | 4410 | 0 | 0 |

**Union of all IDs:** 4410  
**Intersection of all IDs:** 4410

**Decision:** Clean 1:1 inner join across the three master files. No orphan handling required.

---

## 3. Constant Columns

| File | Column | Constant Value |
|---|---|---|
| general | `EmployeeCount` | `1` |
| general | `Over18` | `Y` |
| general | `StandardHours` | `8` |

**Rationale:** A column with a single value cannot differentiate, segment, or predict anything. It also consumes storage and clutters the schema.

**Decision:** Drop `EmployeeCount`, `Over18`, `StandardHours` in Stage 3.

---

## 4. Numeric Range Check

**Result:** ✅ No numeric range violations detected.

**Note:** This is a pass/fail check against domain-appropriate bounds (e.g., Age 18–100, ratings 1–4, tenure ≥ 0). Observed min/max per column will be logged in the processed data summary (Stage 3).

---

## 5. Categorical Consistency

| File | Column | # Distinct | Values |
|---|---|---|---|
| general | `Attrition` | 2 | `No`, `Yes` |
| general | `BusinessTravel` | 3 | `Non-Travel`, `Travel_Frequently`, `Travel_Rarely` |
| general | `Department` | 3 | `Human Resources`, `Research & Development`, `Sales` |
| general | `EducationField` | 6 | `Human Resources`, `Life Sciences`, `Marketing`, `Medical`, `Other`, `Technical Degree` |
| general | `Gender` | 2 | `Female`, `Male` |
| general | `JobRole` | 9 | `Healthcare Representative`, `Human Resources`, `Laboratory Technician`, `Manager`, `Manufacturing Director`, `Research Director`, `Research Scientist`, `Sales Executive`, `Sales Representative` |
| general | `MaritalStatus` | 3 | `Divorced`, `Married`, `Single` |
| general | `Over18` | 1 | `Y` |

**Decision:** No whitespace, case, or label normalization needed. Categories are internally consistent.

---

## 6. Missing Values

### 6.1 Where the nulls are

| Column | Missing | % of 4,410 |
|---|---|---|
| `employee_survey__WorkLifeBalance` | 38 | 0.86% |
| `employee_survey__EnvironmentSatisfaction` | 25 | 0.57% |
| `employee_survey__JobSatisfaction` | 20 | 0.45% |
| `general__NumCompaniesWorked` | 19 | 0.43% |
| `general__TotalWorkingYears` | 9 | 0.20% |

**Employees with ≥1 missing value:** 110 (2.49%)

### 6.2 Distribution of missingness

Missingness is **scattered**, not concentrated. 111 nulls are spread across 110 employees — essentially one null per affected employee. Only one employee has two missing values.

### 6.3 Missingness vs. Attrition

For each column with nulls, we compared the attrition rate among employees **with** vs. **without** a missing value. Large gaps suggest the missingness is informative rather than random.

| Column | n_null | Attrition (null) | Attrition (present) | Diff (pp) |
|---|---|---|---|---|
| `WorkLifeBalance` | 38 | 10.53% | 16.17% | -5.64 |
| `EnvironmentSatisfaction` | 25 | 20.00% | 16.10% | +3.90 |
| `JobSatisfaction` | 20 | 5.00% | 16.17% | -11.17 |
| `NumCompaniesWorked` | 19 | 21.05% | 16.10% | +4.95 |
| `TotalWorkingYears` | 9 | 22.22% | 16.11% | +6.11 |

**Interpretation:** `JobSatisfaction` shows the largest gap (−11.17 pp): employees who did not report job satisfaction had an observed attrition rate of 5% vs. 16.17% among those who did. However, the null group is small (n=20 → ~1 leaver), so this is flagged as a pattern for further investigation, not a confirmed relationship.

**Decision:** Keep all nulls. Do not drop rows. Do not impute. Handle nulls per-analysis (SQL aggregates already ignore them) and document the handling in each query's output.

---

## 7. Attendance File Cross-Check

| File | IDs | Overlap with Master | Only in Master | Only in Attendance |
|---|---|---|---|---|
| in_time | 4410 | 4410 | 0 | 0 |
| out_time | 4410 | 4410 | 0 | 0 |

**Decision:** Attendance data joins cleanly to master. Processed separately in Stage 4 (wide→long reshape, overnight handling).

---

## 8. Decisions Carried into Stage 3 (Cleaning)

| # | Decision | Justification |
|---|---|---|
| 1 | Drop `EmployeeCount`, `Over18`, `StandardHours` | Constants (Section 3) |
| 2 | Keep all 4,410 rows | Only 2.49% affected by nulls; dropping biases sample (Section 6) |
| 3 | Do not impute nulls | Missingness may be informative; fabrication risk (Section 6.3) |
| 4 | Build dimension tables for coded categoricals | Codes are labels, not quantities; business readability (Stage 5) |
| 5 | Merge master files as 1:1 inner join | Confirmed clean (Section 2) |
| 6 | Process attendance separately in Python | Wide format (~250 date columns); not a SQL-native task (Section 7) |

---

## 9. Limitations of This Audit

- Range checks used domain-appropriate bounds, not exhaustive rules.
- Missingness-vs-attrition analysis is univariate; confounders not controlled.
- The dataset is synthetic/anonymized; some relationships may be artifacts.
- No temporal dimension: `Attrition` is a single binary flag with no exit date.

