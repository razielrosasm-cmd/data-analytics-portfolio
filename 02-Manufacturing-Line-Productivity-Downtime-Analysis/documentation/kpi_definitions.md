# KPI Definitions

## Manufacturing Line Productivity & Downtime Analysis

This document defines the business logic and formulas used for the primary KPIs in the project.

The purpose is to ensure that the same business definitions are applied consistently across **SQL, Python, and Power BI**.

---

# 1. Production KPIs

## Total Batches

### Definition

The total number of production batches recorded in the production dataset.

### Formula

`Total Batches = COUNT of production batch records`

### Business Purpose

Measures total production activity during the analyzed period.

---

## Total Production Time

### Definition

The total actual production time across all recorded batches.

### Formula

`Total Production Time = SUM(Actual Batch Time)`

### Business Purpose

Measures the total amount of time spent producing the recorded batches.

---

## Average Batch Time

### Definition

The average actual production time required to complete a batch.

### Formula

`Average Batch Time = Total Actual Production Time ÷ Total Batches`

Equivalent calculation:

`AVG(Actual Batch Time)`

### Business Purpose

Provides a general measure of production-cycle duration.

---

## Average Standard Time

### Definition

The average minimum theoretical production time required for the recorded batches.

### Formula

`Average Standard Time = SUM(Standard Batch Time) ÷ Total Batches`

Equivalent calculation:

`AVG(Minimum Batch Time)`

### Business Purpose

Provides the expected production-time benchmark against which actual performance can be evaluated.

---

# 2. Time Performance KPIs

## Time Variance

### Definition

The difference between actual production time and standard production time.

### Formula

`Time Variance = Actual Production Time - Standard Production Time`

At aggregate level:

`Total Time Variance = SUM(Actual Batch Time) - SUM(Standard Batch Time)`

### Interpretation

- Positive value = production took longer than the standard
- Zero = production matched the standard
- Negative value = production was completed faster than the standard

### Business Purpose

Measures production-time loss relative to the expected production benchmark.

---

## Time Variance %

### Definition

Measures the percentage by which actual production time differs from standard production time.

### Formula

`Time Variance % = (Actual Time - Standard Time) ÷ Standard Time × 100`

### Interpretation

A higher positive percentage indicates greater production-time deviation from the standard.

### Business Purpose

Allows time performance to be compared across products or operators with different production standards.

---

## Production Efficiency

### Definition

Measures production performance by comparing standard production time with actual production time.

### Formula

`Production Efficiency = Standard Production Time ÷ Actual Production Time × 100`

### Interpretation

- 100% = actual time equals standard time
- Greater than 100% = actual time is below the standard
- Less than 100% = actual time exceeds the standard

### Business Purpose

Provides an efficiency-oriented measure of production performance.

---

# 3. Downtime KPIs

## Total Downtime

### Definition

The total number of minutes recorded as production downtime.

### Formula

`Total Downtime = SUM(Downtime Minutes)`

### Business Purpose

Measures the overall production time lost due to recorded downtime events.

---

## Average Downtime per Event

### Definition

The average duration of an individual downtime event.

### Formula

`Average Downtime per Event = Total Downtime ÷ Number of Downtime Events`

### Business Purpose

Shows the typical severity of individual downtime events.

---

## Average Downtime per Batch

### Definition

Measures downtime relative to the number of production batches.

### Formula

`Average Downtime per Batch = Total Downtime ÷ Total Production Batches`

### Business Purpose

Allows downtime intensity to be compared against production activity.

---

## Downtime %

### Definition

Measures downtime as a percentage of the total observed production and downtime period.

### Formula

`Downtime % = Total Downtime ÷ (Total Production Time + Total Downtime) × 100`

### Business Purpose

Provides an indication of how much of the observed operating time was lost to downtime.

### Important Note

The denominator must be defined consistently across all analytical tools.

For this project, downtime percentage is based on:

`Production Time + Downtime`

rather than scheduled calendar time.

---

# 4. Downtime Contribution

## Downtime by Factor

### Definition

Total downtime associated with each downtime factor.

### Formula

`Downtime by Factor = SUM(Downtime Minutes) GROUPED BY Downtime Factor`

### Business Purpose

Identifies the leading sources of downtime and helps prioritize improvement efforts.

---

## Downtime Contribution %

### Definition

Measures the percentage of total downtime associated with a specific downtime factor.

### Formula

`Downtime Contribution % = Downtime for Factor ÷ Total Downtime × 100`

### Business Purpose

Allows downtime causes to be ranked according to their relative contribution.

---

# 5. Product Performance KPIs

## Product Utilization / Efficiency

Product performance is evaluated using the same production-efficiency logic applied to the overall line.

### Formula

`Product Efficiency = Standard Production Time ÷ Actual Production Time × 100`

### Business Purpose

Identifies products that consistently require more production time than expected.

---

## Product Time Variance

### Definition

Measures the production-time difference between actual and standard production time for a product.

### Formula

`Product Time Variance = Actual Product Time - Standard Product Time`

### Business Purpose

Identifies products with significant production-time losses.

---

# 6. Operator Performance KPIs

## Operator Utilization / Efficiency

Operator performance is evaluated using the production-efficiency calculation.

### Formula

`Operator Efficiency = Standard Production Time ÷ Actual Production Time × 100`

### Business Purpose

Allows operator-level production performance to be compared using a common production-time benchmark.

### Important Interpretation Note

Operator performance should not be interpreted as a direct measure of individual capability without considering:

- Product mix
- Batch complexity
- Equipment conditions
- Downtime
- Production context
- Sample size

The dashboard is intended to identify patterns requiring further investigation.

---

## Operator Time Variance %

### Formula

`Operator Time Variance % = (Actual Operator Time - Standard Operator Time) ÷ Standard Operator Time × 100`

### Business Purpose

Identifies operators associated with greater deviations from expected production time.

---

# 7. Volume KPIs

## Batches by Product

### Definition

Number of production batches associated with each product.

### Formula

`Batches by Product = COUNT(Batch Records) GROUPED BY Product`

### Business Purpose

Shows the production mix and provides context for product-level performance comparisons.

---

## Batches by Operator

### Definition

Number of production batches associated with each operator.

### Formula

`Batches by Operator = COUNT(Batch Records) GROUPED BY Operator`

### Business Purpose

Provides production-volume context when comparing operator performance.

---

# 8. KPI Interpretation Rules

The following principles should be applied when interpreting the KPIs.

### Higher Efficiency

Generally indicates that actual production time is closer to or below the expected standard.

### Higher Time Variance

Indicates greater deviation from the expected production time.

### Higher Downtime

Indicates greater production-time loss.

### Higher Downtime Contribution

Indicates that a downtime factor represents a larger share of total production losses.

### Operator Comparisons

Should be interpreted together with production volume, product mix, downtime, and operating conditions.

---

# 9. Cross-Tool Consistency

The KPI definitions in this document are the reference definitions for:

`SQL`
` ↓`
`Python`
` ↓`
`Power BI / DAX`

The same business logic should be maintained across all three analytical layers.

Differences in presentation, aggregation level, or visualization are acceptable; differences in the underlying business definition are not.

---

# 10. Project KPI Summary

| KPI | Core Formula |
| --- | ------------- |
| Total Batches | COUNT(Batch Records) |
| Total Production Time | SUM(Actual Time) |
| Average Batch Time | AVG(Actual Time) |
| Average Standard Time | AVG(Standard Time) |
| Time Variance | Actual Time − Standard Time |
| Time Variance % | `(Actual − Standard) ÷ Standard × 100` |
| Production Efficiency | `Standard ÷ Actual × 100` |
| Total Downtime | SUM(Downtime Minutes) |
| Avg. Downtime per Event | Total Downtime ÷ Downtime Events |
| Avg. Downtime per Batch | Total Downtime ÷ Total Batches |
| Downtime % | `Downtime ÷ (Production Time + Downtime) × 100` |
| Downtime Contribution % | Factor Downtime ÷ Total Downtime |
| Product Efficiency | Standard Product Time ÷ Actual Product Time |
| Operator Efficiency | Standard Operator Time ÷ Actual Operator Time |

---

# Final Principle

A KPI is only useful when its definition is clear, reproducible, and consistently applied.

For this project:

> **The KPI definition is established first; the tool used to calculate or visualize it comes second.**

This ensures that SQL, Python, and Power BI communicate the same business story.

