# Python Analysis — Preparation, Validation, Modeling

Python does three jobs in this project: prepare the data, validate the SQL findings, and build the statistical model that turns findings into a decision tool.

---

## Scripts (`analysis/`)

**Data preparation**

| File | What it does |
|------|--------------|
| `01_inspect_raw_data.py` | Inspects all five raw files — shape, dtypes, null counts, sample rows |
| `02_data_quality_audit.py` | Audits nulls, duplicates, range violations, and cross-file key consistency |
| `03_clean_master.py` | Merges raw files into `data/processed/hr_master_clean.csv` (4,410 × 28) |
| `04a_inspect_attendance.py` | Inspects the 1,041,930-row in/out time files — coverage, duplicates, ranges |
| `04_process_attendance.py` | Summarizes attendance into per-employee averages → `attendance_employee_summary.csv` |

**Validation**

| File | What it does |
|------|--------------|
| `05_validate_sql.py` | Re-runs every SQL finding in pandas and compares. **12/12 checks passed** — SQL and Python agree on every number. |

**Modeling**

| File | What it does |
|------|--------------|
| `06_eda_charts.py` | Generates 8 EDA charts → `outputs/charts/chart01–08.png` |
| `07_logistic_regression.py` | Fits the logistic regression — odds ratios, risk scores, calibration |
| `08_model_impact.py` | What-if analysis — projects leavers avoided per intervention |

---

## Outputs (`outputs/`)

**Reports**
- `validation_report.md` — 12/12 SQL vs Python cross-checks
- `logistic_regression_report.md` — model fit, odds ratios, calibration, interpretation

**Data**
- `odds_ratios.csv` — every model coefficient as an odds ratio
- `risk_scores.csv` — per-employee predicted probability + risk band
- `what_if_impact.csv` — leavers avoided per intervention

**Charts** (`outputs/charts/`)

| Chart File | Description |
|------------|-------------|
| `chart01_attrition_by_department.png` | Attrition by department |
| `chart02_attrition_by_tenure.png` | Attrition by tenure |
| `chart03_attrition_by_satisfaction.png` | Attrition by satisfaction |
| `chart04_tenure_hours_heatmap.png` | Tenure vs Hours heatmap |
| `chart05_year7_spike.png` | Year-7 attrition spike |
| `chart06_high_risk_by_department.png` | High-risk by department |
| `chart07_odds_ratios.png` | Logistic regression odds ratios |
| `chart08_what_if_impact.png` | What-if intervention impact |

---

## The Model

**Method:** Logistic regression on `attrition_flag` (binary target), fit with `statsmodels`.

**Data:** 4,308 employees — 102 dropped via listwise deletion of incomplete records. Nulls were **not imputed** — missingness is informative.

**Fit:** Pseudo R² = 0.14, likelihood-ratio p = 1.2e-105 (the model strongly outperforms the null model).

**Key odds ratios:**
- `hours_ord` = **2.54** — the largest driver
- `dept_hr` = **2.29** — HR anomaly survives controls
- `env_sat` = **0.73**, `job_sat` = **0.76**, `wlb` = **0.78** — protective
- `tenure_ord` = **0.76** — protective

**Calibration** — risk bands separate cleanly:

| Band | Employees | Actual attrition |
|------|-----------|------------------|
| High | 142 | 59.15% |
| Medium | 768 | 36.59% |
| Low | 3,398 | 9.77% |

---

## Design Principles

- **Validation is not optional.** Every SQL finding is re-run in pandas. If SQL and Python disagree, the project stops.
- **No imputation.** Missing values stay missing, and the cost of that is documented.
- **The model serves the business, not the other way around.** Every coefficient feeds a what-if analysis that answers "how many leavers avoided?"
- **Report calibration.** A model that predicts but doesn't calibrate is a toy. The risk-band table is the proof.