# Logistic Regression — Factor Association & Impact

**Scripts:** `python/analysis/07_logistic_regression.py`, `python/analysis/08_model_impact.py`
**Framing:** Association and model-based impact projection — **not** prediction accuracy.
**Why not accuracy:** The dataset is ~16% leavers; a naive "nobody leaves" model would score ~84% accuracy and be useless. The correct diagnostics for this question are odds ratios with confidence intervals, plus risk-band calibration.

---

## Model

- **Method:** Logistic regression (`statsmodels.Logit`)
- **Target:** `attrition_flag` (1 = leaver, 0 = stayed)
- **Predictors (13):** tenure band (ordinal), hours band (ordinal), tenure × hours interaction, department dummies (R&D = reference; Sales, HR), job level, monthly income, distance from home, num companies worked, work-life balance, environment satisfaction, job satisfaction, stock option level
- **Sample:** 4,308 of 4,410 employees (102 dropped via listwise deletion — see below)
- **Fit:** McFadden pseudo-R² = 0.14; LLR p = 1.2e-105 (model beats intercept-only)

## Listwise deletion (no imputation — pre-registered decision)

- 102 rows dropped (2.3%) for having ≥1 null in the predictors
- Dropped-row attrition: **13.73%** vs retained **16.18%** — a gap within the 95% CI on n=102, so deletion is defensible here
- Caveat: if future data shows dropped-row attrition far from benchmark, deletion would need re-examination

## Headline findings (odds ratios with 95% CI)

| Predictor | OR | 95% CI | p | Read |
|---|---|---|---|---|
| **hours_ord** | 2.54 | [2.02 – 3.19] | <1e-15 | Each one-step increase in hours **more than doubles** odds of attrition |
| **dept_hr** | 2.29 | [1.58 – 3.31] | <1e-5 | HR department shows **2.3×** the odds of R&D after full controls |
| environment_satisfaction | 0.73 | [0.68 – 0.79] | <1e-13 | Each step up reduces odds by 27% |
| job_satisfaction | 0.76 | [0.70 – 0.82] | <1e-11 | Each step up reduces odds by 24% |
| work_life_balance | 0.78 | [0.69 – 0.88] | <1e-4 | Each step up reduces odds by 22% |
| tenure_ord | 0.76 | [0.64 – 0.90] | 0.002 | Each tenure band up reduces odds by 24% |
| job_level | 0.92 | [0.85 – 1.00] | 0.048 | Marginal — 8% reduction per level |
| tenure_x_hours | 0.93 | [0.86 – 1.00] | 0.051 | Borderline — direction matches 08a but not conventionally significant |
| dept_sales | 0.99 | [0.81 – 1.21] | 0.93 | Not distinguishable from R&D |
| monthly_income | 1.00 | [1.00 – 1.00] | 0.19 | No effect after controls |
| stock_option_level | 0.97 | [0.88 – 1.08] | 0.58 | No protective effect |
| distance_from_home | 1.00 | [0.99 – 1.01] | 0.79 | No effect |
| num_companies_worked | 1.03 | [0.99 – 1.06] | 0.12 | No effect |

## Risk-band diagnostic (model discrimination & calibration)

| Risk band | n | Actual leavers | Actual rate | Mean predicted |
|---|---|---|---|---|
| High (≥50%) | 142 | 84 | 59.15% | 61.05% |
| Medium (25–50%) | 768 | 281 | 36.59% | 34.25% |
| Low (<25%) | 3,398 | 332 | 9.77% | 10.22% |

Monotonic decrease, calibrated within ~2pp per band. 142 employees (3.3%) contain 12% of all leavers.

## What-if impact (model-based projections — **not causal**)

| Category | Intervention | Affected | Avg prob drop | Leavers avoided |
|---|---|---|---|---|
| actionable | Improve EnvSat +1 step | 1,672 | −4.02 pp | 67.2 |
| actionable | Improve JobSat +1 step | 1,672 | −3.59 pp | 60.0 |
| actionable | Cap year-1 hours (Long→Normal) | 211 | −18.72 pp | 39.5 |
| actionable | Improve WLB +1 step | 1,241 | −3.13 pp | 38.9 |
| diagnostic | Remove HR dept effect | 187 | −12.07 pp | 22.6 |
| validation_only | Everyone +1 tenure band | 4,308 | −4.09 pp | 176.2 |

**Interpretation caveat:** what-if numbers assume causal response from an observational model. They are directional guidance, not guarantees. A real intervention requires a pilot / A/B test.

**Ranking nuance:** satisfaction interventions touch ~1,700 employees each at ~4pp; the hours intervention touches 211 at ~19pp. In *absolute* leavers avoided, satisfaction wins. In *actionability within 90 days*, hours wins. Recommendation is a two-track program, not a single lever.

## Limitations

- Observational data: associations and projections, not causal effects
- Ordinal encodings (tenure, hours, satisfaction) lose resolution — 5 bands is a coarse proxy for a continuous variable
- Interaction term is borderline (p=0.051) — treated as directional support, not proof
- Synthetic dataset — patterns are representative but not from a real firm
- 102-row listwise deletion (2.3%) — defensible here, monitor in future
- HR "Remove dept effect" row is a diagnostic quantity (how much attrition is attributable to HR-department membership alone), not an intervention