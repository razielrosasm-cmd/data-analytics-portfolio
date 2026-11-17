# Statistical Model Log — Track C Maintenance

This document outlines the methodology, variable selection, and results of the logistic regression model used to predict high-cost maintenance months (Track C). 

The goal of the model was to determine which operational factors actually drive cost, and to simulate the impact of policy changes.

---

## Model Overview

- **Algorithm:** Logistic Regression (binary classification)

- **Target Variable:** `is_high_cost` (1 if total maintenance cost for a truck-month is in the top 25% of all months, 0 otherwise).

- **Dataset:** `master_truck_month_clean.csv` (3,312 rows).

- **Tool Used:** Python (`statsmodels` and `scikit-learn`).

---

## Variable Selection

We tested seven candidate features against the target variable. We included operational metrics, vehicle characteristics, and maintenance history.

### 1. `had_preventive_visit`
- **Type:** Binary (1 = Yes, 0 = No)
- **Hypothesis:** Months with a preventive visit will have higher costs because the truck is in the shop.

### 2. `downtime_hours`
- **Type:** Continuous (Hours)
- **Hypothesis:** The longer a truck is in the shop, the more expensive the month.

### 3. `truck_age_years`
- **Type:** Continuous (Years)
- **Hypothesis:** Older trucks break more often and cost more to fix.

### 4. `total_miles_k`
- **Type:** Continuous (Thousands of miles)
- **Hypothesis:** Higher mileage leads to more wear and tear.

### 5. `utilization_rate`
- **Type:** Continuous (Percentage)
- **Hypothesis:** Trucks that are driven harder require more maintenance.

### 6. `make_premium`
- **Type:** Binary (1 = Premium brand, 0 = Standard brand)
- **Hypothesis:** Premium trucks might have higher parts costs, but better reliability.

### 7. `is_old_truck`
- **Type:** Binary (1 = Over 7 years old, 0 = Under 7 years)
- **Hypothesis:** A threshold effect where very old trucks become money pits.

---

## Results: Odds Ratios

The model calculates an "Odds Ratio" for each feature. An odds ratio greater than 1 means the feature *increases* the likelihood of a high-cost month. An odds ratio less than 1 means it *decreases* the likelihood.

| Feature | Odds Ratio | Interpretation | Statistically Significant? |
|---|---|---|---|
| **`had_preventive_visit`** | **12.54** | A preventive visit makes a high-cost month **12.5 times more likely**. | ✅ Yes |
| `utilization_rate` | 1.96 | Weak positive effect. | ❌ No |
| **`downtime_hours`** | **1.076** | Every extra hour of downtime adds **7.6% to the odds**. | ✅ Yes |
| `truck_age_years` | 1.024 | Almost no effect. | ❌ No |
| `total_miles_k` | 0.990 | Almost no effect. | ❌ No |
| `make_premium` | 0.909 | Almost no effect. | ❌ No |
| `is_old_truck` | 0.747 | Older trucks do not cost more to maintain. | ❌ No |

**The Big Surprise:** Truck age, make, and miles have no clear effect on maintenance cost. The only things that matter are **whether the truck went to the shop** (preventive visit) and **how long it stayed there** (downtime).

---

## Model Calibration

The model assigns a risk score from 1 to 10 to every truck-month (where 10 is the highest risk). We tested the model against the actual data to see if the scores were accurate.

- **Scores 1 to 4:** 0% of these months were actually high-cost.
- **Score 9:** 51% of these months were high-cost.
- **Score 10:** **83%** of these months were high-cost.

Because the model achieves an 83% accuracy at the top end, the Logistics Supervisor can trust the risk score to flag specific months for a cost audit.

---

## What-If Simulation (The Counterintuitive Finding)

Because the model showed that preventive visits *increase* cost, we ran a simulation to see what would happen if the fleet did more of them.

- **Baseline Prediction:** If current operations continue, the fleet will experience **828** high-cost months next year.

- **Intervention:** If the fleet increases preventive visits by 10%, the model predicts **923** high-cost months.

**Conclusion:** Adding preventive maintenance visits adds shop visits. And since shop visits are the cost driver, the cost goes up. The strategy of "do more preventive maintenance" would backfire.

---

## Business Translation

Instead of just adding more visits, the business should focus on **scope discipline at each visit**:

1. Keep the truck in the shop only as long as strictly necessary (reduce downtime).

2. Review every work order and defer non-critical items.

3. Extend the preventive interval for trucks that are running without problems.