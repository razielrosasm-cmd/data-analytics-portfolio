# SQL Analysis — Manufacturing Operations

## Overview

SQL was used as the **primary analytical tool** for the Manufacturing Analysis project.

The analysis focuses on production volume, production efficiency, downtime, product-level performance, batch-level overruns, and operator-level production variance.

The SQL workflow was structured into two analytical phases:

- **Phase 1 — Core Analysis**
- **Phase 2 — Validation & Business Insights**

The objective was to transform the prepared manufacturing data into measurable operational insights that can support production improvement decisions.

---

# Analytical Questions

The SQL analysis answers the following business questions:

1. How many production batches were completed for each product?
2. Which products have the largest production-time variance versus standard?
3. Which downtime factors contribute most to total downtime?
4. Which products are associated with the highest downtime?
5. Which products have the highest downtime per batch?
6. How significant is the overall production-time variance?
7. How concentrated is downtime among the main downtime factors?
8. Which downtime factors affect each product?
9. Which individual batches have the largest production-time overruns?
10. Which downtime factors are associated with the highest-overrun batches?
11. How does production-time variance differ across operators?

---

# SQL Analysis Structure

## Phase 1 — Core Analysis

### `01_production_volume_analysis.sql`

Analyzes production volume by product.

**Main metric:**
- Total production batches

**Business question:**
> How many batches were produced for each product?

---

### `02_production_efficiency_analysis.sql`

Analyzes production-time performance against the minimum batch-time standard.

**Main metrics:**
- Average actual production time
- Standard batch time
- Average time variance
- Average time variance %

**Business questions:**
> Which products take the longest compared with their standard batch time?

> Which products have the largest percentage variance from standard?

---

### `03_downtime_analysis.sql`

Analyzes downtime by factor and product.

**Main metrics:**
- Total downtime
- Downtime percentage
- Total downtime by product
- Average downtime per batch

**Business questions:**
> Which downtime factors contribute most to production downtime?

> Which products are associated with the most downtime?

> Which products have the highest downtime per batch?

---

# Phase 2 — Validation & Business Insights

## `01_overall_production_efficiency.sql`

Validates the overall production-efficiency KPI across all production batches.

**Main metrics:**
- Total batches
- Average actual batch time
- Average standard batch time
- Average time variance
- Average time variance %

**Key result:**

> Across 38 batches, average production time was 36.53 minutes above the standard, representing a 56.17% average variance.

---

## `02_downtime_concentration.sql`

Measures how concentrated downtime is among the largest downtime factors.

**Main metric:**
- Top 5 downtime factors as a percentage of total downtime

**Key result:**

> The top five downtime factors represented 80.40% of total recorded downtime.

---

## `03_product_downtime_factors.sql`

Connects products with their specific downtime factors.

**Analysis structure:**

`Product → Downtime Factor → Total Downtime`

**Business question:**

> Which downtime factors contribute most to downtime for each product?

This analysis supports product-specific improvement priorities.

---

## `04_highest_batch_time_overruns.sql`

Identifies the individual production batches with the largest time overruns versus standard.

**Main metrics:**
- Actual batch time
- Standard batch time
- Time variance

**Business question:**

> Which batches had the largest production-time overruns?

This analysis identifies specific batches that may require operational investigation.

---

## `05_high_overrun_batch_downtime.sql`

Examines the downtime factors associated with the highest-overrun batches.

**Analysis structure:**

`High-Overrun Batch → Downtime Factor → Downtime`

**Business question:**

> Which downtime factors were associated with the largest production overruns?

This connects batch-level production inefficiency with specific downtime events.

---

## `06_operator_production_variance.sql`

Provides supporting analysis of production-time variance across operators.

**Main metrics:**
- Total batches
- Average actual production time
- Average standard time
- Average time variance
- Average time variance %

**Business question:**

> How does average production-time variance differ across operators?

The analysis is used as supporting evidence rather than to assign responsibility to individual operators.

---

# Key Business Findings

### 1. Production efficiency is below standard

Across 38 production batches:

- Average actual batch time: **101.53 minutes**
- Average standard batch time: **65.00 minutes**
- Average variance: **+36.53 minutes**
- Average variance: **+56.17%**

This indicates a substantial gap between actual production time and the defined minimum batch-time standards.

---

### 2. Downtime is highly concentrated

The five largest downtime factors account for:

**80.40% of total downtime.**

This indicates that improvement efforts can be prioritized around a relatively small number of major downtime causes.

---

### 3. Downtime patterns differ by product

The product-level downtime analysis shows that different products experience different dominant downtime factors.

Examples include:

- CO-2L — Machine adjustment
- CO-600 — Machine failure and inventory shortage
- LE-600 — Batch change
- RB-600 — Machine adjustment
- DC-600 — Machine failure
- OR-600 — Batch change

This suggests that improvement opportunities should be evaluated at the product/process level rather than assuming one universal cause.

---

### 4. The largest production overruns are concentrated in specific batches

The highest-overrun batches include:

- CO-2L Batch 422147: **+107 minutes**
- OR-600 Batch 422111: **+75 minutes**
- CO-600 Batch 422123: **+73 minutes**
- RB-600 Batch 422140: **+63 minutes**

These batches provide specific cases for operational investigation.

---

### 5. Downtime is strongly associated with production-time variance

Across products, the ranking of average production-time variance closely follows the ranking of average downtime per batch.

This indicates a strong operational relationship between downtime and production-time overruns.

The analysis describes this as an **association**, not proof of causation.

---

### 6. Production variance is not isolated to one operator

All four operators show substantial average production-time variance.

This suggests that the observed efficiency gap may reflect broader process, equipment, material, training, or standard-work factors rather than being isolated to one individual.

---

# SQL Evidence

The SQL evidence is organized by analytical phase:

```text
sql/
│
├── phase_1_analysis/
│   ├── 01_production_volume_analysis.sql
│   ├── 02_production_efficiency_analysis.sql
│   └── 03_downtime_analysis.sql
│
└── phase_2_validation_and_insights/
    ├── 01_overall_production_efficiency.sql
    ├── 02_downtime_concentration.sql
    ├── 03_product_downtime_factors.sql
    ├── 04_highest_batch_time_overruns.sql
    ├── 05_high_overrun_batch_downtime.sql
    └── 06_operator_production_variance.sql