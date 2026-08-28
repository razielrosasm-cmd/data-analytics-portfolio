# Python Analysis — Maven Fuzzy Factory

## Overview

Python was used as a **supporting analytical, validation, and visualization tool** within the Maven Fuzzy Factory project.

The primary analytical work was performed in **SQL**, where the core business metrics and analytical results were calculated from the e-commerce database.

Python was then used to work with selected SQL results exported to CSV, validate analytical outputs, explore trends, and create supporting visualizations.

The **Power BI dashboard remains the primary business intelligence and reporting layer** of the project.

---

## Purpose of the Python Phase

The Python phase was designed to complement the SQL analysis rather than duplicate the complete SQL workflow.

The main objectives were:

* Validate selected SQL results
* Work with exported analytical CSV files
* Explore trends and patterns
* Create supporting visualizations
* Provide an additional validation layer for selected metrics
* Generate visual assets used during project development and documentation

Python therefore serves as a **supporting analytical layer** between the SQL analysis and the final Power BI reporting solution.

---

## Python Workflow

The Python workflow follows this process:

```text
SQL Analysis
     ↓
Selected SQL Results
     ↓
CSV Export
     ↓
Python Analysis
     ↓
Validation & Visualization
     ↓
Supporting Charts
     ↓
Power BI / Project Documentation
```

This approach keeps each technology focused on a specific role:

| Tool         | Primary Role                                          |
| ------------ | ----------------------------------------------------- |
| **SQL**      | Core data analysis and KPI calculations               |
| **Python**   | Validation, exploration, and supporting visualization |
| **Power BI** | Interactive business intelligence and reporting       |

---

# Python Visualizations

The project contains the following Python visualization scripts.

## 1. Monthly Revenue

```text
01_monthly_revenue_chart.py
```

Creates a visualization of monthly revenue performance and supports the analysis of revenue trends over time.

---

## 2. Monthly Orders

```text
02_monthly_orders_chart.py
```

Visualizes the number of orders over time and supports the analysis of changes in monthly order volume.

---

## 3. Monthly Average Order Value

```text
03_monthly_aov_chart.py
```

Visualizes Average Order Value (AOV) over time.

This helps evaluate whether changes in revenue are accompanied by changes in the average value of completed orders.

---

## 4. Monthly Conversion Rate

```text
04_monthly_conversion_rate_chart.py
```

Visualizes conversion-rate performance over time.

This supports the analysis of changes in website conversion and provides an additional way to validate selected SQL results.

---

## 5. Product Revenue

```text
05_product_revenue_chart.py
```

Visualizes revenue contribution by product.

This supports the product-performance analysis and helps identify the products contributing the most revenue.

---

## 6. Product Revenue per Order

```text
06_product_revenue_per_order_chart.py
```

Visualizes revenue per order at the product level.

This provides an additional perspective on product value beyond total revenue alone.

---

## 7. Product Revenue Over Time

```text
07_product_revenue_over_time_chart.py
```

Visualizes product revenue performance over time.

This supports the analysis of how individual products contribute to revenue across the observed period.

---

## 8. Bounce Rate by Landing Page

```text
08_bounce_rate_by_landing_page_chart.py
```

Visualizes bounce-rate performance across landing pages.

This supports the landing-page analysis and helps identify pages requiring further investigation.

---

# Relationship to the SQL Analysis

Python does not replace the SQL analysis.

The SQL phase is responsible for calculating the core analytical results used throughout the project.

Python uses selected outputs from that analysis to provide:

* Independent visual validation
* Trend exploration
* Supporting charts
* Additional analytical context

This separation helps maintain a clear analytical workflow while avoiding unnecessary duplication between tools.

---

# Relationship to Power BI

The Python visualizations are **supporting analytical assets**, not the final reporting solution.

The final Power BI dashboard is responsible for presenting the project's main business analysis through an interactive reporting environment.

The overall workflow is therefore:

```text
Raw E-Commerce Data
        ↓
SQL Analysis
        ↓
Python Validation & Exploration
        ↓
Power BI Dashboard
        ↓
Business Insights
        ↓
Recommendations
```

---

# Reproducibility

To reproduce the Python analysis:

1. Complete the relevant SQL analysis.
2. Export the required analytical results to CSV.
3. Use the corresponding CSV results as inputs for the Python scripts.
4. Run the Python visualization scripts.
5. Review the generated charts and compare them with the SQL results.
6. Use the validated analytical results in the final Power BI reporting workflow.

The Python phase is therefore dependent on selected analytical outputs produced during the SQL phase rather than directly querying the original SQLite database.

---

# Python Skills Demonstrated

The Python phase demonstrates practical use of Python for data analysis, including:

* Reading CSV data
* Working with tabular analytical results
* Data processing
* Basic analytical validation
* Trend analysis
* Data visualization
* Generating reusable analytical charts

The Python implementation intentionally focuses on practical, explainable techniques appropriate for an entry-level Data Analyst workflow.

---

# Python Resources

The Python visualization scripts are:

```text
01_monthly_revenue_chart.py
02_monthly_orders_chart.py
03_monthly_aov_chart.py
04_monthly_conversion_rate_chart.py
05_product_revenue_chart.py
06_product_revenue_per_order_chart.py
07_product_revenue_over_time_chart.py
08_bounce_rate_by_landing_page_chart.py
```

These scripts support the broader Maven Fuzzy Factory analytical workflow but are not intended to replace the SQL analysis or the final Power BI dashboard.

---

## Final Takeaway

Python plays a supporting role in the Maven Fuzzy Factory project by providing an additional layer of **validation, exploration, and visualization**.

The complete analytical workflow demonstrates the ability to use different tools for different stages of a business analytics project:

> **SQL for analysis → Python for validation and exploration → Power BI for business intelligence → Insights for decision-making**
