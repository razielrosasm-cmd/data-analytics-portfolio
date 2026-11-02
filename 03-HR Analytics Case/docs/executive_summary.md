
# Executive Summary — HR Attrition Analysis

**Prepared for:** HR Leadership & Department Heads
**Analyst:** Raziel Rosas
**Dataset:** 4,410 employees | 711 leavers | single-snapshot HR dataset
**Tools:** SQL (SQLite) · Python (pandas, statsmodels) · Power BI

---

## Bottom Line

The company is losing **711 of 4,410 employees — a 16.12% attrition rate** — and the pattern is not random. Three drivers explain most of it: **first-year workload** (the single largest factor, more than doubling a new hire's risk of leaving), **environmental satisfaction** (the broadest lever across the workforce), and an **unexplained HR department anomaly** that holds even after accounting for tenure, hours, and satisfaction. A two-track intervention — capping first-year hours and improving environmental satisfaction — is projected to avoid **~107 leavers combined (~15% of the 711 observed)**, with an HR-specific diagnostic run in parallel. The model turns attrition from a reactive exit-interview conversation into a predictable, addressable business problem.

---

## Finding 1 — The Year-1 Workload Shock

**Finding.** Employees in their first year who work long hours leave at **54.42%** — more than **3× the company benchmark** of 16.12%.

**Evidence.**

- Tenure alone is a strong predictor: attrition runs **34.88%** for 0–1
  years, falling steadily to **8.13%** at 10+ years
  (`04_attrition_by_tenure.sql`).

- Hours is the single strongest driver in our statistical model:    employees working long hours are **2.5× more likely to leave**, and no other factor comes close.

- Combined, the two compound: the **0–1 yrs × Long hours** cell reaches
  **54.42% attrition** across **215 employees**
  (`08a_tenure_x_hours_overlap.sql`).

- The effect is not concentrated in one role: within R&D specifically,
  **0–1 yrs × Long hours = 57.04%** across 77 leavers
  (`08d2_rd_year1_long_hours_role_breakdown.sql`) — it is role-uniform.

**Business meaning.** New hires are being loaded with long hours before they have the tenure, relationships, or institutional knowledge to absorb them.

This is the single most actionable group in the analysis: **211 employees, one lever (hours), one policy change.** It is a scheduling problem, not a culture problem — which is why it can be fixed in a quarter, not a year.

---

## Finding 2 — Environmental Satisfaction Is the Broadest Lever

**Finding.** Environmental satisfaction is the strongest **protective** factor in the model: raising it by one level is projected to avoid
**~67 leavers** — the highest absolute return of any single intervention.

**Evidence.**

- Three satisfaction measures all point the same way — higher satisfaction means lower attrition:
  - **Environmental satisfaction**: each level up reduces risk of leaving
    by about **27%**
  - **Job satisfaction**: each level up reduces risk by about **24%**
  - **Work-life balance**: each level up reduces risk by about **22%**

- The pattern is consistent across all three measures — not a fluke of one
  variable (`07_logistic_regression.py`).

- Applied across the lowest-satisfaction employees, raising environmental
  satisfaction by one level is projected to avoid **~67 leavers**
  (`08_model_impact.py`).

**Business meaning.** This is a *broad* lever — it touches the whole
workforce, not one segment. It takes longer than the hours cap because it
requires cultural and resource investment, but the **absolute payoff is
largest**. Job satisfaction (~60 leavers avoided) and work-life balance
(~39) follow the same pattern; environmental satisfaction leads because it
has the widest reach.

---

## Finding 3 — The HR Department Anomaly

**Finding.** HR employees leave at **30.16%** — roughly **twice** the R&D
and Sales rates (15.71% and 15.02%) — and the gap **holds even after
accounting for tenure, hours, and satisfaction**. HR department membership
alone is linked to **~23 expected leavers**.

**Evidence.**

- Raw attrition by department (`02_attrition_by_department.sql`):
  - HR:    **30.16%**
  - R&D:   **15.71%**
  - Sales: **15.02%**

- In the statistical model, being in HR roughly **doubles** the chance of
  leaving — even after controlling for tenure, hours, satisfaction, and
  work-life balance.

- The effect is not explained by hours or tenure: once HR's small
  Year-1 × Short-hours cell (62.5%) is removed, HR's attrition drops to
  **~25%** — still well above R&D and Sales
  (`08d_high_risk_cells_department.sql`).

**Business meaning.** Unlike the Year-1 workload shock, this is **not a
scheduling problem** — the model has stripped out the usual suspects and HR
still stands out. That points to something department-specific: hiring
profile, role design, management style, career-path clarity, or
compensation. It needs a **focused investigation** before any policy is
prescribed. Bringing HR to parity with R&D/Sales represents roughly **23
expected leavers avoided**.

---

## The Recommendation — A Two-Track Approach

The model allows us to move away from reactive exit interviews and toward predictive retention. Based on volume, feasibility, and time-to-effect, management should execute a two-track strategy with a diagnostic workstream running in parallel.

### Track 1 (Immediate / 90 days): Cap First-Year Hours

The most direct, controllable lever is reducing overtime for new hires.

Capping hours at 7.5–8 hours per day for the **211 employees in their first year** is projected to avoid **~40 leavers** — roughly **5.6% of the 711 observed** — and directly addresses the **54.4% attrition** cell shown in Finding 1.

This is a policy change, not a cultural one — it can be executed next quarter.

### Track 2 (Strategic / 6–12 months): Improve Environmental Satisfaction

The broadest lever is improving environmental satisfaction by one level for employees currently in the lowest satisfaction tiers.

This is projected to avoid **~67 leavers** — the **highest absolute return** of any single intervention. Because it requires sustained investment in workplace culture and resources, it is a slower initiative — but the payoff is largest across the whole workforce.

### Diagnostic: HR Department Investigation

The model links **~23 expected leavers** to HR department membership alone — above and beyond tenure and hours. This warrants a separate, focused investigation into HR hiring, role design, and management practices — not a blanket policy change.

---

## Limitations

This analysis is honest about what it can and cannot claim.

- **Observational, not experimental.** The data shows strong associations — for example, long hours go with higher attrition — but does not prove causation. A hours-cap policy should be piloted and measured, not assumed to work exactly as projected.

- **Synthetic dataset.** The data is a constructed portfolio dataset, not a live company's HR records. The methodology transfers; the exact percentages would not.

- **Year-7 anomaly remains unexplained.** Attrition spikes at Year 7 (47.8% for 69 employees), but the model does not identify a driver. It is reported as an observation, not a conclusion.

- **Missing values were not imputed.** Blank satisfaction and survey fields were left blank, not filled in. This preserves the honest signal in the missingness but means the model is fitted on the 4,308 employees with complete records, not all 4,410.

---

*Analysis, queries, and model code available in the project repository. Reproducible end-to-end from raw CSV to dashboard.*