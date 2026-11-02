# SQL Analysis — 14 Analytical Queries

All analytical SQL for the HR attrition project. Queries run against the SQLite database `hr_attrition.db`, populated from the cleaned master table via `load_data.py`.

---

## Database Setup

| File | Purpose |
|------|---------|
| `schema.sql` | Table definitions — `hr_master` (28 columns) + constraints |
| `load_data.py` | Loads `data/processed/hr_master_clean.csv` into `hr_attrition.db` |
| `_validate_load.py` | Post-load sanity check — row count, null count, schema integrity |
| `hr_attrition.db` | The SQLite database itself (generated, not committed) |

To rebuild the database from scratch, run: `python load_data.py`

---

## Queries

14 queries in `analysis/`, each paired with its CSV output in `analysis/results/`.

**Baseline & Segmentation**

| # | File | Question answered |
|---|------|-------------------|
| 01 | `01_attrition_overview.sql` | Total employees, leavers, and overall attrition rate (4,410 / 711 / 16.12%) |
| 02 | `02_attrition_by_department.sql` | Attrition by department — HR 30.16%, R&D 15.71%, Sales 15.02% |
| 03 | `03_attrition_by_job_role.sql` | Attrition by job role |
| 04 | `04_attrition_by_tenure.sql` | Attrition by tenure band — 34.88% (0–1) → 8.13% (10+) |
| 05 | `05_attrition_by_income_band.sql` | Attrition by salary band |

**Drivers**

| # | File | Question answered |
|---|------|-------------------|
| 06 | `06_satisfaction_vs_attrition.sql` | Satisfaction levels vs attrition |
| 07 | `07_attrition_by_worklife_overtime.sql` | Work-life balance and overtime vs attrition |

**High-Risk Cells (the core findings)**

| # | File | Question answered |
|---|------|-------------------|
| 08a | `08a_tenure_x_hours_overlap.sql` | The **54.42% cell** — 0–1 yrs × Long hours (215 employees, 117 leavers) |
| 08b | `08b_High_Risk_Segment_Profile.sql` | Profile of the high-risk segment — who they are |
| 08c | `08c_Promotion_Stagnation_Inside_High_Risk.sql` | Promotion stagnation inside the high-risk segment |
| 08c2 | `08c2_Year_7_Spike_Check.sql` | Year-7 attrition spike (47.8%, 69 employees) |
| 08d | `08d_High_Risk_Cells_Department.sql` | High-risk cells by department |
| 08d2 | `08d2_rd_year1_long_hours_role_breakdown.sql` | R&D × 0–1 yrs × Long hours (57.04%, 77 leavers) |

---

## Results

Each query has a matching CSV in `analysis/results/`. These CSVs are the **single source of truth** that feeds:
- The Power BI dashboard
- The Python validation (`05_validate_sql.py` cross-checks them)
- The executive summary and README findings

Every number cited in the project's documentation can be traced back to a specific query and its CSV output.

---

## Design Principles

- **No CTEs, no window functions, no correlated subqueries** — all queries use only `SELECT / FROM / WHERE / GROUP BY / HAVING / JOIN / CASE`, so they read clearly and audit easily.
- **One query = one question.** No query tries to answer multiple things at once.
- **Every output persists as a CSV.** Reproducibility over convenience.
- **Benchmark is consistent.** All percentage comparisons use the 16.12% company benchmark and report **percentage-point gaps**.