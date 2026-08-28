# Analytical Methodology

## Manufacturing Line Productivity & Downtime Analysis

This document describes the analytical methodology used to transform raw manufacturing data into actionable production and downtime insights.

The project follows an end-to-end analytical workflow using **data preparation, SQL, Python, and Power BI**.

---

## 1. Business Problem

The analysis focuses on understanding manufacturing-line productivity and identifying the main sources of production losses.

The project was designed to answer four primary business questions:

1. How efficiently is the production line operating?
2. Which operators or production conditions are associated with lower performance?
3. What are the leading causes of downtime?
4. Are particular operator errors associated with specific downtime factors?

The objective is not only to calculate KPIs, but to translate operational data into findings that can support continuous-improvement decisions.

---

## 2. Analytical Workflow

The project follows this process:

`RAW DATA`
`   │`
`   ▼`
`1. Data Understanding`
`   │`
`   ▼`
`2. Data Validation`
`   │`
`   ▼`
`3. Data Preparation`
`   │`
`   ▼`
`4. SQLite Database`
`   │`
`   ▼`
`5. SQL Analysis`
`   │`
`   ▼`
`6. Python Validation`
`   │`
`   ▼`
`7. Power BI Data Model`
`   │`
`   ▼`
`8. KPI Development`
`   │`
`   ▼`
`9. Insight Generation`
`   │`
`   ▼`
`10. Business Recommendations`

Each stage has a specific purpose and contributes to the final analysis.

---

## 3. Raw Data Inspection

The first stage consisted of understanding the structure and business meaning of the original datasets.

The following areas were reviewed:

- Available tables
- Column names
- Data types
- Production fields
- Product information
- Downtime information
- Time fields
- Potential relationships
- Missing values
- Duplicate records
- Inconsistent formats

The purpose of this stage was to understand the data before performing calculations.

---

## 4. Data Validation

The source data was reviewed for common data-quality issues that could affect the analysis.

Validation included:

- Checking column names
- Reviewing data types
- Identifying missing values
- Checking duplicate records
- Reviewing categorical values
- Validating time fields
- Checking production-duration logic
- Comparing related product and production information

Particular attention was given to production start and end times because production shifts may cross midnight.

---

## 5. Data Preparation

The raw datasets were transformed into analytical datasets suitable for SQL, Python, and Power BI.

The prepared datasets include:

`line_productivity_prepared.csv`
`line_downtime_prepared.csv`
`products.csv`
`downtime_factors.csv`

Preparation focused on:

- Standardizing column names
- Standardizing data types
- Cleaning time fields
- Preparing production duration fields
- Preserving business relationships
- Creating consistent analytical tables

The goal was to create a reliable common dataset that could be used consistently across the project.

---

## 6. SQL Analysis

SQL was used as the primary analytical language for calculating and validating business metrics.

The analysis was organized into two phases:

### Phase 1: Core Analysis

- Production volume by product
- Production efficiency by product
- Downtime analysis by factor and product

### Phase 2: Validation and Business Insights

- Overall production efficiency
- Downtime concentration analysis
- Product downtime factor analysis
- Highest batch time overruns
- High-overrun batch downtime analysis
- Operator production variance

The SQL implementation intentionally uses fundamental SQL concepts appropriate for a Junior Data Analyst portfolio project.

The primary SQL concepts used include:

`SELECT`
`FROM`
`WHERE`
`GROUP BY`
`ORDER BY`
`HAVING`
`DISTINCT`
`COUNT`
`SUM`
`AVG`
`ROUND`
`CASE`
`JOIN`
`LEFT JOIN`

Advanced SQL techniques such as window functions and CTEs were intentionally avoided.

---

## 7. Python Validation

Python was used as a supporting analytical and validation tool.

The main library used was:

- `pandas`

Python was used to:

- Load prepared datasets
- Validate calculations
- Explore distributions
- Check data consistency
- Compare analytical results

Python was not used for machine learning or predictive modeling.

The purpose of Python in this project was primarily **validation and exploratory analysis**, while SQL remained the primary structured analytical layer.

---

## 8. Power BI Modeling

Power BI was used as the final business intelligence and reporting layer.

The prepared analytical datasets were loaded into Power BI and organized into a semantic model.

The model supports analysis across:

- Production
- Products
- Operators
- Downtime
- Downtime factors
- Dates

DAX measures were created for the primary business KPIs.

The Power BI dashboard was designed to allow users to move from high-level performance into detailed operational analysis.

---

## 9. KPI Development

KPIs were defined before being implemented in the final dashboard.

The main KPI categories are:

### Production KPIs

- Total Batches
- Total Production Time
- Average Batch Time
- Average Standard Time

### Efficiency KPIs

- Time Variance
- Time Variance %
- Production Efficiency

### Downtime KPIs

- Total Downtime
- Average Downtime per Batch
- Downtime %
- Downtime by Factor
- Downtime by Product

### Performance KPIs

- Operator Performance
- Product Performance
- Batch Performance

The KPI definitions are documented separately in:

`documentation/kpi_definitions.md`

---

## 10. Cross-Validation

A key project requirement was consistency between the analytical tools.

The general validation approach was:

`SQL Result`
`   │`
`   ├──► Python Validation`
`   │`
`   └──► Power BI KPI`

Important calculations were compared across the analytical layers.

This helps reduce the possibility of presenting different numbers in SQL, Python, and Power BI.

---

## 11. Insight Generation

The analysis was used to identify meaningful operational patterns rather than simply report numbers.

Examples of analytical questions include:

- Which downtime factors contribute the most total downtime?
- Which products experience the greatest downtime?
- Which products show the largest production-time variance?
- Which operators show lower utilization?
- Are operator-related errors concentrated in particular activities?
- Where should improvement efforts be prioritized?

The interpretation of operator-level results is treated carefully because performance differences may be influenced by product mix, process conditions, equipment, or other operational factors.

---

## 12. Business Recommendations

The final stage converts analytical findings into practical improvement opportunities.

Recommendations focus on areas such as:

- Reducing machine adjustment time
- Investigating recurring machine failures
- Reducing inventory-related interruptions
- Reviewing high-variance products
- Standardizing operating practices
- Evaluating operator training opportunities
- Monitoring improvement results through KPIs

The recommendations are intended to support continuous-improvement activities rather than serve as definitive root-cause conclusions.

---

## 13. Final Deliverable

The final Power BI report provides an interactive view of the analysis through:

1. Executive Overview
2. Downtime Analysis
3. Operator & Product Performance
4. Batch Detail
5. Final Recommendations

The dashboard connects operational metrics with detailed analysis and recommended actions.

---

## 14. Methodology Principles

The project follows five main analytical principles:

### Accuracy

Calculations should be reproducible and consistent.

### Consistency

SQL, Python, and Power BI should use the same business definitions.

### Traceability

Important dashboard metrics should be traceable back to prepared source data and analytical calculations.

### Business Relevance

KPIs should answer meaningful manufacturing questions.

### Actionability

Insights should lead to practical areas for investigation or improvement.

---

# Conclusion

The methodology demonstrates an end-to-end approach to manufacturing analytics:

`Understand the Data`
`       ↓`
`Validate the Data`
`       ↓`
`Prepare the Data`
`       ↓`
`Analyze with SQL`
`       ↓`
`Validate with Python`
`       ↓`
`Model in Power BI`
`       ↓`
`Develop KPIs`
`       ↓`
`Identify Insights`
`       ↓`
`Recommend Actions`

The result is a reproducible analytical workflow that combines technical data-analysis skills with manufacturing and continuous-improvement knowledge.

