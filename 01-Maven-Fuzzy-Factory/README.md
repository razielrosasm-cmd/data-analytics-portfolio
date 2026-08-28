# Maven Fuzzy Factory — E-Commerce Data Analytics

## From Raw E-Commerce Data to Business Recommendations

An end-to-end **Data Analytics & Business Intelligence portfolio project** analyzing website traffic, customer behavior, conversion performance, purchasing funnels, landing pages, device behavior, product sales, and revenue for a fictional e-commerce toy store.

The project demonstrates a complete analytical workflow using **SQL, Python, and Power BI**, transforming raw relational data into business insights and actionable recommendations.

---

## Business Question

> **How can the business improve website conversion and revenue by understanding traffic sources, customer behavior, device performance, landing pages, the purchasing funnel, and product performance?**

The analysis was designed to move beyond reporting metrics and identify **where performance gaps exist, why they matter, and what the business should investigate or improve.**

---

# Power BI Dashboard

The final **Power BI report is the primary business intelligence deliverable** of the project.

### Executive Overview

[![Executive Overview](dashboard_images/01_Executive%20Overview.png)](dashboard_images/01_Executive%20Overview.png)

### Product Performance

[![Product Performance](dashboard_images/04_Product%20Performance.png)](dashboard_images/04_Product%20Performance.png)

It contains **8 analytical pages**:

| Page                                     | Business Focus                                                                        |
| ---------------------------------------- | ------------------------------------------------------------------------------------- |
| **Executive Overview**                   | Overall business performance, revenue, orders, conversion, and trends                 |
| **Marketing & Traffic**                  | Traffic-source volume, conversion, revenue, AOV, and acquisition performance          |
| **Conversion Funnel**                    | Customer progression through the purchasing journey and major drop-off points         |
| **Product Performance**                  | Product revenue, orders, units sold, and product-level performance                    |
| **Device Performance**                   | Desktop vs. mobile sessions, orders, conversion, revenue, AOV, and revenue efficiency |
| **Engagement & Bounce**                  | Website engagement, bounce behavior, and pageview depth                               |
| **Landing Page Performance**             | Landing-page traffic, conversion, bounce behavior, and revenue efficiency             |
| **Executive Insights & Recommendations** | Key findings, business implications, and recommended priorities                       |

The report includes interactive filtering to allow the analysis to be explored across relevant dimensions such as date, traffic source, device, and landing page.

---

# Key Findings

## 1. Desktop Converts Significantly Better Than Mobile

| Device  | Sessions | Orders | Conversion Rate |
| ------- | -------: | -----: | --------------: |
| Desktop |  327,027 | 27,805 |       **8.50%** |
| Mobile  |  145,844 |  4,508 |       **3.09%** |

Desktop conversion is substantially higher than mobile conversion.

However, Average Order Value is very similar:

| Device  |    AOV |
| ------- | -----: |
| Desktop | $59.91 |
| Mobile  | $60.50 |

### Business implication

The primary mobile opportunity appears to be **conversion performance rather than order value**.

### Recommendation

Investigate the mobile purchasing experience, particularly:

* Product browsing
* Cart experience
* Shipping
* Billing
* Checkout usability

The objective is to identify friction points that may prevent mobile visitors from completing purchases.

---

## 2. `/lander-5` Is the Strongest Landing Page

`/lander-5` achieved:

* **10.17% conversion rate**
* **36.87% bounce rate**
* **$6.43 revenue per session**

It represents the strongest landing-page performance identified in the analysis.

### Recommendation

Use `/lander-5` as a performance benchmark and investigate its:

* Page structure
* Messaging
* Calls to action
* User experience
* Content

Successful elements could provide hypotheses for testing on weaker landing pages.

---

## 3. `/lander-3` Is the Weakest Landing Page

`/lander-3` achieved:

* **3.39% conversion rate**
* **50.29% bounce rate**

This makes it a clear optimization opportunity.

### Recommendation

Prioritize `/lander-3` for further investigation and A/B testing.

The objective should be to understand why visitors leave and determine which changes can improve progression toward purchase.

---

## 4. Traffic Volume and Traffic Quality Are Different

| Traffic Source | Sessions | Conversion |       Revenue |
| -------------- | -------: | ---------: | ------------: |
| gsearch        |  316,035 |      6.75% | $1,276,144.89 |
| Direct / NULL  |   83,328 |  **7.34%** |   $371,433.03 |
| bsearch        |   62,823 |      7.19% |   $268,672.50 |
| socialbook     |   10,685 |      3.21% |    $22,259.33 |

gsearch generated the largest amount of traffic and revenue.

However, Direct / NULL achieved the highest conversion rate among the analyzed sources, while socialbook had the weakest conversion performance.

### Business implication

Traffic volume alone does not indicate acquisition quality.

### Recommendation

Evaluate acquisition channels using multiple performance indicators:

**Sessions + Conversion Rate + Revenue + AOV + Revenue per Session**

This provides a more complete view of traffic quality and business value.

---

## 5. The Original Mr. Fuzzy Is the Main Product Revenue Driver

| Product                    | Product Orders / Items | Units Sold |           Revenue |
| -------------------------- | ---------------------: | ---------: | ----------------: |
| The Original Mr. Fuzzy     |                 24,226 |     23,861 | **$1,211,057.74** |
| The Forever Love Bear      |                  5,796 |      4,803 |       $347,702.04 |
| The Birthday Sugar Panda   |                  4,985 |      3,068 |       $229,260.15 |
| The Hudson River Mini bear |                  5,018 |        581 |       $150,489.82 |

The Original Mr. Fuzzy generated approximately **62% of total product revenue**, making it the dominant revenue contributor in the portfolio.

### Business implication

The business benefits significantly from the product's performance but also has meaningful concentration around a single product.

### Recommendation

Continue supporting the performance of The Original Mr. Fuzzy while identifying opportunities to increase the contribution of the remaining products and strengthen the overall product portfolio.

---

## 6. The Purchasing Funnel Shows Significant Drop-Off

The analysis tracks the customer journey through key website stages:

```text
Home
   ↓
Products
   ↓
Product Page
   ↓
Cart
   ↓
Shipping
   ↓
Billing
   ↓
Purchase Confirmation
```

The analysis contains **32,313 completed orders**, compared with substantially larger volumes earlier in the customer journey.

### Business implication

A large number of sessions do not progress through the complete purchasing journey.

### Recommendation

Investigate the largest stage-to-stage drop-offs, particularly during checkout:

* Cart → Shipping
* Shipping → Billing
* Billing → Purchase

These results should also be evaluated alongside device performance to determine whether mobile users experience greater friction during checkout.

---

# Executive Recommendations

Based on the analysis, five priorities emerge.

### Priority 1 — Investigate Mobile Conversion

Mobile conversion is **3.09%**, compared with **8.50%** on desktop.

Investigate the complete mobile purchasing experience to identify barriers preventing visitors from completing purchases.

---

### Priority 2 — Optimize Underperforming Landing Pages

Use `/lander-5` as a performance benchmark and prioritize `/lander-3` for investigation and testing.

---

### Priority 3 — Investigate Funnel Drop-Off

Identify where the largest number of potential customers are lost, with particular attention to the checkout stages.

---

### Priority 4 — Evaluate Traffic Sources by Business Value

Do not evaluate acquisition performance using sessions alone.

Compare channels using conversion rate, revenue, AOV, and revenue per session.

---

### Priority 5 — Strengthen Product Portfolio Performance

The Original Mr. Fuzzy is the dominant product revenue driver.

Continue supporting its performance while identifying opportunities to increase the contribution of the remaining products.

---

# Analytical Workflow

The project follows a structured:

```text
Raw E-Commerce Data
        ↓
SQL Analysis
        ↓
Python Exploration & Validation
        ↓
Power BI Data Model & Dashboard
        ↓
Business Insights
        ↓
Recommendations
```

Each technology serves a different purpose.

---

## SQL — Core Analysis

SQL is used to query the relational e-commerce database and calculate the project's core analytical metrics.

The analysis covers areas including:

* Website sessions
* Pageviews
* Orders
* Revenue
* Average Order Value
* Conversion Rate
* Bounce Rate
* Pageviews per Session
* Traffic-source performance
* Landing-page performance
* Funnel progression
* Product performance

The SQL analysis uses practical relational-data techniques including filtering, aggregation, grouping, joins, conditional logic, distinct counts, and analytical subqueries.

---

## Python — Exploration & Validation

Python is used as a supporting analytical tool.

The Python phase works with selected SQL outputs to:

* Validate analytical results
* Explore trends
* Process exported CSV results
* Create supporting visualizations
* Provide an additional validation layer for selected metrics

Python complements the SQL and Power BI work rather than duplicating the complete analysis.

---

## Power BI — Business Intelligence

Power BI is the **primary reporting and visualization layer**.

The final report transforms the analytical results into an interactive business intelligence dashboard covering:

* Executive performance
* Marketing and traffic
* Conversion funnel
* Product performance
* Device behavior
* Website engagement
* Landing-page performance
* Executive insights and recommendations

The dashboard is designed to allow stakeholders to move from high-level business performance into specific areas requiring investigation.

---

## Business Insights — Decision Support

The final stage connects analytical results with business implications.

The objective is not simply to report:

> **What happened?**

but to answer:

> **What does the data mean for the business, and what should be investigated or improved?**

---

# Dataset

The project uses the Maven Fuzzy Factory e-commerce relational dataset.

The analytical tables include:

| Dataset                  | Description                                     |
| ------------------------ | ----------------------------------------------- |
| `website_sessions.csv`   | Website sessions and traffic-source information |
| `website_pageviews.csv`  | Website pageview activity                       |
| `orders.csv`             | Customer orders                                 |
| `order_items.csv`        | Products included in orders                     |
| `order_item_refunds.csv` | Refunded order items                            |
| `products.csv`           | Product catalog                                 |

### Dataset Size

The analysis includes approximately:

* **472,871** website sessions
* **1,188,124** website pageviews
* **32,313** orders
* **40,025** order items
* **1,731** refunded order items
* **4** products

---

# Tools Used

| Tool             | Purpose                                                                 |
| ---------------- | ----------------------------------------------------------------------- |
| **SQLite / SQL** | Relational data querying and analytical calculations                    |
| **Python**       | Exploration, validation, data processing, and supporting visualizations |
| **Power BI**     | Data modeling, interactive dashboards, and business reporting           |
| **CSV**          | Exchange of analytical results between workflow stages                  |
| **Git / GitHub** | Version control and portfolio presentation                              |

---

# Project Structure

The repository is organized around the project's analytical workflow:

```text
Maven-Fuzzy-Factory/
│
├── data/
│   └── E-Commerce dataset files
│
├── SQL analysis
│   └── SQL analysis scripts and documentation
│
├── dashboard_images/
│   └── Supporting dashboard and analytical images
│
├── Python resources
│   └── Supporting Python analysis and visualization scripts
│
├── Power BI report
│   └── Final interactive dashboard
│
└── README Project Root.md
```

The repository contains the analytical resources used throughout the project, including SQL analysis, supporting Python work, dashboard assets, dataset files, and the final Power BI deliverable.

---

# Reproducibility

The analytical workflow can be followed from the provided datasets through the SQL analysis, supporting Python outputs, and final Power BI report.

## 1. Prepare the Data

Use the datasets provided in the `data/` folder.

The data follows the relational structure of the Maven Fuzzy Factory e-commerce database.

---

## 2. Run the SQL Analysis

Open the database using a compatible SQLite environment.

Run the SQL analysis scripts to reproduce the core analytical calculations.

The SQL phase produces the primary results used throughout the project.

---

## 3. Export Selected Results

Selected SQL results are exported to CSV files for use in the supporting Python analysis.

---

## 4. Run the Python Analysis

Run the Python scripts included in the project to reproduce the supporting analytical visualizations and validation work.

Examples include:

* Monthly revenue
* Monthly orders
* Monthly AOV
* Monthly conversion rate
* Product revenue
* Product revenue per order
* Product revenue over time
* Bounce rate by landing page

---

## 5. Open the Power BI Report

Open the final Power BI report to explore the interactive dashboard.

The report contains **8 pages** covering the project's main analytical areas.

---

## 6. Review the Executive Insights

The final **Executive Insights & Recommendations** page summarizes the most important findings and translates them into business priorities.

---

# Skills Demonstrated

## Data Analysis

* Business problem definition
* KPI development
* E-commerce analytics
* Website performance analysis
* Conversion analysis
* Funnel analysis
* Landing-page analysis
* Product performance analysis
* Revenue analysis
* Business recommendation development

## SQL

* Data filtering
* Aggregation
* Grouping
* Sorting
* Conditional logic
* Joins
* Distinct counts
* Subqueries
* KPI calculations

## Python

* CSV-based analysis
* Data processing
* Analytical validation
* Trend exploration
* Visualization
* Supporting chart generation

## Power BI

* Data modeling
* Business intelligence reporting
* Interactive dashboards
* KPI visualization
* Cross-filtering
* Performance analysis
* Executive reporting

## Business Intelligence

* Translating data into insights
* Identifying performance gaps
* Comparing business segments
* Prioritizing opportunities
* Connecting findings to recommendations
* Communicating analytical results to business stakeholders

---

# Project Outcome

The project transforms raw e-commerce data into a complete analytical and business intelligence solution.

The analysis identified:

* A significant **mobile conversion gap**
* Strong and weak **landing-page performance**
* Differences between **traffic-source volume and quality**
* Significant **purchasing-funnel drop-off**
* Strong concentration around **The Original Mr. Fuzzy**
* Opportunities for **conversion, website, acquisition, and product-portfolio optimization**

The final Power BI dashboard brings these findings together into an interactive reporting solution designed to support business decision-making.

The project demonstrates the complete analytical lifecycle:

> **Data → Analysis → Visualization → Insight → Recommendation**

---

## Portfolio Objective

This project was developed as a practical demonstration of **Data Analyst and Business Intelligence capabilities**.

It is designed to demonstrate the ability to:

1. Understand a business problem.
2. Work with relational business data.
3. Use SQL to perform analytical investigations.
4. Use Python to explore and validate analytical results.
5. Build an interactive Power BI reporting solution.
6. Identify meaningful performance patterns.
7. Translate findings into business insights.
8. Recommend areas for further investigation or improvement.

The goal is not simply to demonstrate technical tools, but to show the ability to connect **data analysis with business decision-making**.

**Data → Analysis → Visualization → Insight → Recommendation**