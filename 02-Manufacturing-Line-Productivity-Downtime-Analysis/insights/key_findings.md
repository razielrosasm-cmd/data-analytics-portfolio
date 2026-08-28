# Key Findings

## Manufacturing Line Productivity & Downtime Analysis

This document summarizes the main findings supported by the validated SQL analysis and the corresponding Power BI analytical model.

---

## Finding 1 — Production Time Is Above Standard

The production line shows a significant difference between actual and standard batch time.

| Metric | Value |
| ------ | ----- |
| Average actual batch time | 101.53 minutes |
| Average standard batch time | 65.00 minutes |
| Average time variance | 36.53 minutes |
| Average time variance % | 56.17% |

### Business Implication

The gap between actual and standard production time represents a significant productivity opportunity.

The next step should be to determine which products, operators, downtime events, and operating conditions contribute most to this variance.

---

## Finding 2 — Machine Adjustment Is the Largest Downtime Factor

The validated downtime analysis identified the following leading downtime factors:

| Rank | Downtime Factor | Total Downtime |
| ---- | --------------- | -------------- |
| 1 | Machine Adjustment | 332 minutes |
| 2 | Machine Failure | 254 minutes |
| 3 | Inventory Shortage | 225 minutes |
| 4 | Batch Change | 160 minutes |
| 5 | Batch Coding Error | 145 minutes |

### Business Implication

**Machine Adjustment is the largest recorded downtime category**, making setup and adjustment activities an important area for improvement investigation.

Reducing adjustment time through standardized procedures, setup practices, and better preparation could provide an opportunity to reduce production losses.

However, operational investigation would be required before attributing the downtime to a particular process issue.

---

## Finding 3 — Downtime Is Concentrated Across Specific Products

The validated analysis identified the following products with the highest total recorded downtime:

| Rank | Product | Total Downtime |
| ---- | ------- | -------------- |
| 1 | CO-600 | 494 minutes |
| 2 | CO-2L | 277 minutes |
| 3 | RB-600 | 258 minutes |
| 4 | LE-600 | 149 minutes |
| 5 | DC-600 | 115 minutes |
| 6 | OR-600 | 75 minutes |

### Business Implication

Downtime is not evenly distributed across products.

**CO-600 has the highest recorded downtime**, substantially above the other products analyzed.

This makes CO-600 a priority for further investigation into machine adjustments, machine failures, inventory availability, and other associated downtime factors.

---

## Finding 4 — Production Performance Should Be Evaluated Relative to Standard Time

The analysis does not evaluate production performance using actual production time alone.

Actual batch time is compared with the corresponding minimum/standard batch time to determine time variance, time variance percentage, and production efficiency.

### Business Implication

A product with a longer absolute batch time is not necessarily underperforming.

Performance should instead be evaluated based on how closely actual production time aligns with the applicable production standard.

---

## Finding 5 — Operator Differences Require Context

The operator analysis identifies differences in production performance across operators.

| Operator | Batches | Avg Time Variance (min) | Time Variance % |
| -------- | ------- | ----------------------- | --------------- |
| Mac | 8 | 41.50 | 64.09% |
| Dennis | 8 | 37.75 | 58.30% |
| Dee | 11 | 33.64 | 56.06% |
| Charlie | 11 | 34.91 | 49.62% |

### Business Implication

These differences should not be interpreted as direct evidence that one operator is responsible for lower productivity.

Operator results may be influenced by product mix, number of batches handled, production conditions, machine condition, downtime, and product-specific requirements.

Operator-level results should be used to identify **patterns for further investigation**, including potential opportunities for standard-work review, process consistency, training, and best-practice sharing.

---

## Finding 6 — Production Losses Are Driven by Both Time Variance and Downtime

The analysis identifies two complementary sources of productivity loss:

### Production-Time Variance

Actual production time exceeds the standard by an average of **36.53 minutes per batch**.

### Downtime

Machine adjustment, machine failure, and inventory shortage are the leading recorded downtime categories.

### Business Implication

Improvement efforts should not focus exclusively on one KPI.

Reducing downtime may improve available production time, while reducing production-time variance can improve the speed at which batches are completed.

Both dimensions should therefore be monitored together.

---

## Finding 7 — The Current Dataset Supports Prioritization, Not Long-Term Trend Analysis

The analysis covers a relatively short observation period:

- **August 29 – September 3, 2024**
- **38 production batches**
- **61 downtime events**
- **6 products**
- **12 downtime factors**

### Business Implication

The findings are useful for identifying operational opportunities within the analyzed dataset, but they should not be treated as proof of long-term manufacturing trends.

A longer period of production data would be required to determine whether these patterns are persistent.

---

## Overall Finding

The strongest evidence from the analysis is the combination of:

- Actual production time significantly above standard
- High recorded downtime
- Concentration of downtime in specific factors and products

This indicates that the most relevant improvement opportunity is to investigate the causes of production-time losses, beginning with the largest recorded downtime contributors and the products experiencing the greatest losses.