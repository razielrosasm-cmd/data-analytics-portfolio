# Power BI Dashboard — Manufacturing Line Productivity & Downtime Analysis

## Overview

This Power BI report is the **final business intelligence layer** of the *Manufacturing Line Productivity & Downtime Analysis* project.

The dashboard transforms validated production and downtime data into an interactive management report designed to help identify:

* Overall production performance
* Line utilization and productivity
* Production time variance
* Downtime drivers
* Operator performance differences
* Product-level performance
* Operator-related downtime
* Priority improvement opportunities

The report was designed from a **manufacturing operations perspective**, with emphasis on turning operational data into actionable insights rather than simply displaying descriptive statistics.

---

## Business Objective

The objective of the dashboard is to answer four primary business questions:

1. **How efficiently is the production line operating?**
2. **Which operators or production conditions are associated with lower performance?**
3. **What are the main causes of downtime?**
4. **Are specific operator errors associated with particular downtime factors?**

The dashboard provides different levels of analysis, moving from an executive overview to detailed operational investigation and finally to improvement recommendations.

---

## Dashboard Structure

The Power BI report contains five main analytical pages:

### 1. Executive Overview

Provides a high-level view of production performance for management and decision-makers.

Key metrics include:

* Total production batches
* Total downtime
* Average downtime per batch
* Line utilization
* Production performance trends
* Downtime by major factor
* Operator-level performance overview

The purpose of this page is to allow a stakeholder to understand the current operational situation quickly before moving into detailed analysis.

---

### 2. Downtime Analysis

Focuses specifically on production downtime and its operational drivers.

The page analyzes:

* Total downtime
* Downtime by factor
* Downtime by product
* Downtime contribution
* Operator-error-related downtime
* Downtime patterns across the production process

This analysis helps identify where the largest losses are occurring and which downtime categories should receive priority during continuous-improvement activities.

The main downtime factors identified in the analysis include:

* Machine adjustment
* Machine failure
* Inventory shortage

The dashboard allows these factors to be evaluated interactively rather than treating total downtime as a single aggregated metric.

---

### 3. Operator & Product Performance

Analyzes productivity from two operational perspectives:

**Operator performance**

* Utilization %
* Time variance %
* Total batches
* Operator comparisons
* Best and worst operator performance

**Product performance**

* Utilization %
* Average time variance
* Time variance %
* Product comparisons
* Best and worst product performance

This page helps distinguish whether performance differences are more strongly associated with the **operator**, the **product being manufactured**, or the interaction between both.

---

### 4. Batch Detail

Provides a more granular operational view of individual production batches.

The page supports detailed investigation using filters such as:

* Date
* Product
* Batch
* Operator

This page is intended for **drill-down and validation**, allowing users to move from aggregated KPIs into the underlying batch-level information.

---

### 5. Final Recommendations

Converts the analytical findings into a prioritized improvement plan.

The recommendations are structured around:

* Priority
* Recommended action
* Operational problem
* Expected improvement focus

The objective is to connect the dashboard findings with practical manufacturing actions instead of ending the analysis at visualization.

---

## Key KPIs

The dashboard uses measures developed specifically for the production and downtime analysis.

### Production KPIs

| KPI                             | Purpose                                                                        |
| ------------------------------- | ------------------------------------------------------------------------------ |
| **Total Batches**               | Measures total production volume                                               |
| **Average Actual Batch Time**   | Measures typical production time                                               |
| **Average Standard Batch Time** | Establishes the expected production benchmark                                  |
| **Average Time Variance**       | Measures the average deviation from standard                                   |
| **Time Variance %**             | Measures production time loss relative to standard                             |
| **Utilization %**               | Measures production performance relative to available/expected production time |

### Downtime KPIs

| KPI                            | Purpose                                                      |
| ------------------------------ | ------------------------------------------------------------ |
| **Total Downtime**             | Measures total recorded production downtime                  |
| **Average Downtime per Batch** | Measures downtime intensity at batch level                   |
| **Downtime by Factor**         | Identifies the largest sources of downtime                   |
| **Downtime by Product**        | Identifies products associated with greater downtime         |
| **Operator Error Downtime**    | Quantifies downtime associated with operator-related factors |

### Performance KPIs

| KPI                            | Purpose                                                     |
| ------------------------------ | ----------------------------------------------------------- |
| **Best Product Utilization**   | Identifies the strongest-performing product                 |
| **Worst Product Utilization**  | Identifies the product requiring investigation              |
| **Best Operator Utilization**  | Identifies the strongest operator performance               |
| **Worst Operator Utilization** | Identifies the operator performance requiring investigation |

---

## Data Model

The Power BI report is based on prepared analytical datasets generated during the earlier stages of the project.

### Main tables

* `line_productivity_prepared`
* `line_downtime_prepared`
* `downtime_factors`
* `products`

The report also contains a dedicated measures structure used to centralize the main business calculations.

### Data Flow

```text
Raw Production Data
        │
        ▼
Data Understanding & Validation
        │
        ▼
Prepared CSV Data
        │
        ▼
SQLite Database
        │
        ▼
SQL Analysis
        │
        ▼
Python Validation
        │
        ▼
Power BI Data Model
        │
        ▼
DAX Measures
        │
        ▼
Interactive Dashboard
        │
        ▼
Insights & Recommendations
```

---

## Analytical Approach

The dashboard follows a structured analytical workflow:

### 1. Production Performance

Production batches are compared against expected production standards to identify time losses and efficiency gaps.

The analysis evaluates the difference between:

```text
Actual Production Time
vs.
Minimum / Standard Production Time
```

This produces the time variance metrics used throughout the report.

### 2. Downtime Analysis

Downtime is aggregated by:

* Downtime factor
* Product
* Batch
* Operator-related classification

This makes it possible to identify the largest contributors to production losses.

### 3. Operator Analysis

Operators are compared using production volume and performance indicators.

The objective is **not to treat individual performance differences as isolated conclusions**, but to identify patterns that may justify further operational investigation, training, standardization, or process review.

### 4. Product Analysis

Products are evaluated based on:

* Utilization
* Production time
* Time variance
* Downtime

This helps identify whether certain products consistently require more production time or experience greater operational losses.

### 5. Recommendations

The final step connects the quantitative findings to potential operational actions.

The recommendations prioritize opportunities according to their potential operational impact.

---

## Data Validation

Consistency between the analytical layers was a key requirement of the project.

The workflow used:

* **SQL** for structured business analysis
* **Python / pandas** for validation and exploratory analysis
* **Power BI / DAX** for the final interactive reporting layer

Important KPIs were cross-checked between SQL and Power BI to reduce the risk of discrepancies between the analytical calculations and the final dashboard.

This approach ensures that Power BI is not treated as an isolated visualization tool, but as the final presentation layer of a broader analytical workflow.

---

## Interactive Features

The report includes interactive filtering and analysis capabilities.

Users can filter the analysis by dimensions including:

* Date
* Product
* Batch
* Operator

These filters allow stakeholders to move from the overall production-line picture into specific products, operators, dates, and batches.

---

## Key Analytical Findings

The underlying analysis identified several important operational patterns.

The dataset contains:

* **38 production batches**
* **65 minutes average standard batch time**
* **101.53 minutes average actual batch time**
* **36.53 minutes average time variance**
* **56.17% average time variance**

The downtime analysis identified the following major contributors:

| Downtime Factor    | Total Downtime |
| ------------------ | -------------: |
| Machine Adjustment |            332 |
| Machine Failure    |            254 |
| Inventory Shortage |            225 |

Downtime concentration was also observed across products, with:

| Product | Total Downtime |
| ------- | -------------: |
| CO-600  |            494 |
| CO-2L   |            277 |
| RB-600  |            258 |

These results provide the basis for the improvement priorities presented in the final dashboard.

---

## Tools & Technologies

| Tool             | Purpose                                            |
| ---------------- | -------------------------------------------------- |
| **Power BI**     | Data modeling, DAX measures, interactive dashboard |
| **DAX**          | KPI and analytical measure development             |
| **SQL / SQLite** | Data analysis and business calculations            |
| **Python**       | Data validation and exploratory analysis           |
| **Pandas**       | Data manipulation and validation                   |
| **Matplotlib**   | Supporting visual analysis                         |
| **Excel / CSV**  | Source and prepared datasets                       |
| **Git / GitHub** | Project version control and portfolio presentation |

---

## Portfolio Value

This Power BI project demonstrates the ability to move beyond dashboard creation and complete an end-to-end analytical workflow:

```text
Business Problem
      ↓
Data Preparation
      ↓
Data Validation
      ↓
SQL Analysis
      ↓
Python Validation
      ↓
Power BI Modeling
      ↓
DAX KPI Development
      ↓
Interactive Dashboard
      ↓
Business Insights
      ↓
Recommendations
```

The primary focus is on demonstrating practical **Data Analyst skills applied to a manufacturing environment**, including:

* KPI development
* Operational performance analysis
* Downtime analysis
* Root-cause-oriented analysis
* Data validation
* Business-oriented visualization
* Interactive reporting
* Translating data into actionable recommendations

---

## Project Context

This dashboard is part of the larger:

**02 — Manufacturing Line Productivity & Downtime Analysis**

project.

Power BI represents the **final reporting and decision-support layer** of the project. The complete project also includes data preparation, SQL analysis, Python validation, documentation, insights, and recommendations.

```text
02-Manufacturing-Line-Productivity-Downtime-Analysis/
│
├── data/
├── database/
├── documentation/
├── insights/
├── powerbi/
│   └── Manufacturing-Line-Productivity-Downtime-Analysis.pbix
├── python/
└── sql/
```

---

## Author

**Raziel Rosas Martinez**

Mechanical Engineer | Data Analyst | Manufacturing & Continuous Improvement

**Focus Areas:**
Data Analysis • Manufacturing Analytics • Power BI • SQL • Python • Operational Performance • Continuous Improvement
