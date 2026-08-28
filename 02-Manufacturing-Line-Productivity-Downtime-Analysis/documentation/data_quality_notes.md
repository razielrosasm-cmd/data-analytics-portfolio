# Data Quality Notes

## Manufacturing Line Productivity & Downtime Analysis

This document records the main data-quality issues, preparation decisions, assumptions, and limitations identified during the project.

The purpose is to make the analytical process transparent and explain how the original data was transformed into the final analytical datasets.

---

## 1. Source Data

The original dataset contains manufacturing production and downtime information covering:

**August 29, 2024 through September 3, 2024.**

The final prepared datasets include:

- `line_productivity_prepared.csv`
- `line_downtime_prepared.csv`
- `products.csv`
- `downtime_factors.csv`

These files are used by the SQL, Python, and Power BI layers.

---

## 2. Time Data Standardization

Time fields required special attention during data preparation.

The original Excel data contained time values that could be interpreted inconsistently depending on the software used to read the file.

For example, an end-time value could be interpreted as a full datetime containing the Excel base date:

`1900-01-01 01:05:00`

while the corresponding start time could appear as:

`22:55`

This difference can produce incorrect duration calculations if the fields are subtracted without normalization.

The time fields were therefore standardized before analytical calculations.

---

## 3. Midnight-Crossing Production Batches

Production batches can cross midnight.

Example:

`Start Time: 22:55`
`End Time: 01:05`

A simple subtraction of the two time values would incorrectly produce a negative duration.

The correct duration is:

`22:55 → 24:00 = 65 minutes`
`00:00 → 01:05 = 65 minutes`

`Total = 130 minutes`

Therefore:

`Actual Batch Time = 130 minutes`

rather than a negative value.

This rule was explicitly considered during data preparation and validation.

---

## 4. Data Types

Data types were reviewed and standardized to support reliable analytical calculations.

Important fields include:

| Field Type | Analytical Treatment |
| ---------- | -------------------- |
| Dates | Standardized as date values |
| Time fields | Standardized for duration calculations |
| Durations | Converted/represented consistently for arithmetic |
| Downtime Minutes | Numeric |
| Product | Categorical text |
| Operator | Categorical text |
| Downtime Factor | Categorical text |

During the SQLite import process, some duration fields were stored as text because of the original prepared CSV representation.

Where required, SQL expressions were used to extract and convert the time component for calculations.

---

## 5. Missing Values

Missing values were reviewed during data validation.

The analysis does not assume that a missing value represents zero.

Where a value is required for a KPI calculation, the field must contain a valid value or be handled explicitly according to the calculation logic.

This is particularly important for:

- Production times
- Standard times
- Downtime minutes
- Product identifiers
- Operator identifiers

---

## 6. Duplicate Records

The datasets were reviewed for duplicate records.

Duplicate records can artificially increase:

- Production volume
- Total production time
- Downtime
- KPI values

The prepared analytical datasets were therefore checked before being used for the final analysis.

No duplicate-record assumption should be made when extending this project to a new production dataset; duplicate validation should be repeated as part of the data-ingestion process.

---

## 7. Categorical Consistency

Categorical fields such as:

- Product
- Operator
- Downtime Factor

must remain consistent across the datasets.

Differences in spelling, capitalization, or formatting could create separate categories in SQL or Power BI.

Reference tables such as `products` and `downtime_factors` support standardized business classifications.

---

## 8. Downtime Data

Downtime is recorded as individual events.

The primary downtime measure is:

`Downtime Minutes`

The analysis aggregates these events by:

- Downtime factor
- Product
- Operator
- Date

This makes it possible to identify the largest sources of recorded downtime.

---

## 9. Downtime Classification

Downtime factors represent predefined operational categories.

Examples identified in the dataset include:

- Machine Adjustment
- Machine Failure
- Inventory Shortage

These categories should be interpreted as the recorded classification of the downtime event.

They should not automatically be interpreted as confirmed root causes without additional operational investigation.

---

## 10. Operator Performance Limitations

Operator-level analysis should be interpreted carefully.

Differences between operators may be influenced by:

- Product mix
- Number of batches handled
- Product complexity
- Machine condition
- Downtime
- Production circumstances
- Sample size

Therefore, the dashboard identifies **performance patterns for investigation**, rather than proving that an operator is the direct cause of lower productivity.

---

## 11. Product Performance Limitations

Product-level comparisons may also be influenced by differences in:

- Production requirements
- Standard batch times
- Batch volume
- Downtime
- Production conditions

A product with higher average production time is not necessarily inefficient if its standard time is also higher.

For this reason, product analysis uses actual time together with standard time and variance-based KPIs.

---

## 12. Dataset Size

The analytical dataset is relatively small:

| Item | Count |
| ---- | ----- |
| Production batches | 38 |
| Downtime records | 61 |
| Products | 6 |
| Downtime factors | 12 |

The limited dataset size means that results should be treated as an analytical case study rather than a statistically representative model of long-term manufacturing performance.

The dashboard is designed to demonstrate analytical methodology and decision-support capabilities.

---

## 13. Analytical Limitations

The project has several important limitations.

### Short Observation Period

The dataset covers only a limited number of production days.

Longer-term trends cannot be established from this dataset alone.

### Limited Production Volume

Only 38 production batches are available for the production analysis.

Some operator or product comparisons may therefore have limited statistical significance.

### Recorded Downtime Only

The analysis is based on downtime recorded in the source data.

Unrecorded or incorrectly classified downtime cannot be detected through the dataset alone.

### No External Production Context

The dataset does not provide all potentially relevant operational variables, such as:

- Shift
- Machine condition
- Maintenance history
- Planned production schedule
- Staffing levels
- Material quality
- Environmental conditions

Consequently, the analysis identifies patterns and potential improvement areas rather than establishing definitive causality.

---

## 14. Data Quality Principles

The following principles were applied throughout the project:

### Standardize Before Analyzing

Data types and formats should be normalized before calculating KPIs.

### Validate Before Visualizing

A dashboard should not be used to validate fundamental data-quality issues.

### Preserve Business Meaning

Transformations should improve analytical usability without changing the meaning of the original information.

### Document Assumptions

Important calculation and interpretation assumptions should be explicitly recorded.

### Cross-Validate Results

Important metrics should be compared between SQL, Python, and Power BI.

---

## 15. Final Data Quality Assessment

The prepared datasets are suitable for the intended portfolio analysis of manufacturing productivity and downtime.

However, the results should be interpreted within the scope of the available data.

The project demonstrates a complete analytical process from:

`Raw Data`
`   ↓`
`Data Quality Review`
`   ↓`
`Data Preparation`
`   ↓`
`Validation`
`   ↓`
`Analysis`
`   ↓`
`Dashboard`
`   ↓`
`Insights`

The documented limitations ensure that the dashboard findings are presented as **evidence-based operational observations**, rather than unsupported causal conclusions.

