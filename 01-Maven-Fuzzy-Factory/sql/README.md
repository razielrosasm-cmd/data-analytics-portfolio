# SQL Analysis — Maven Fuzzy Factory

## Overview

SQL is the **foundation of the Maven Fuzzy Factory analysis**.

The purpose of this phase was to transform the raw e-commerce database into meaningful business metrics and analytical results that could later be validated with Python and presented through Power BI.

The SQL analysis focuses on:

* Website traffic
* Traffic-source performance
* Website engagement
* Conversion performance
* Landing-page performance
* Purchasing funnel progression
* Device performance
* Product performance
* Revenue and order metrics

The SQL phase provides the core analytical results used throughout the remainder of the project.

---

# Database

The analysis uses the SQLite database:

```text
database/maven_fuzzy_factory.db
```

The database contains the following primary tables:

| Table                | Purpose                                         |
| -------------------- | ----------------------------------------------- |
| `website_sessions`   | Website sessions and traffic-source information |
| `website_pageviews`  | Individual pageviews generated during sessions  |
| `orders`             | Customer order information                      |
| `order_items`        | Products included in customer orders            |
| `order_item_refunds` | Refund information                              |
| `products`           | Product catalog information                     |

---

# Main Relationships

The SQL analysis uses the relationships between website activity, orders, products, and refunds.

```text
website_sessions
        │
        │ website_session_id
        ▼
website_pageviews


website_sessions
        │
        │ website_session_id
        ▼
orders
        │
        │ order_id
        ▼
order_items
        │
        │ order_item_id
        ▼
order_item_refunds


products
        │
        │ product_id
        ▼
order_items
```

These relationships allow the analysis to connect:

* Website traffic with pageview behavior
* Sessions with completed orders
* Orders with purchased products
* Products with revenue and units sold
* Order items with refunds

---

# Phase 1 — Foundational Business Analysis

The first SQL phase establishes the core business-performance metrics and evaluates the major dimensions of the e-commerce operation.

The analysis answers questions such as:

### Traffic

* How much website traffic does the business receive?
* Which traffic sources generate the most sessions?
* How does traffic volume differ across acquisition channels?

### Conversion

* How many website sessions result in orders?
* What is the overall conversion rate?
* How does conversion performance differ across traffic sources?

### Revenue & Orders

* How much revenue is generated?
* How many orders are completed?
* What is the Average Order Value (AOV)?
* How do revenue and order performance vary across business segments?

### Product Performance

* Which products generate the most revenue?
* Which products generate the most orders or product-level transactions?
* How many units are sold?
* How does product performance vary over time?

### Traffic-Source Value

* Which traffic sources generate the most revenue?
* Which sources convert most effectively?
* Does the source generating the most traffic also generate the best business performance?

The purpose of Phase 1 is to establish the **baseline business performance** needed for deeper analysis.

---

# Phase 2 — Website Engagement, Landing Pages & Funnel Analysis

The second SQL phase focuses more deeply on what visitors do after arriving at the website.

This phase expands the analysis from traffic volume and conversion into **website behavior and customer journey performance**.

### Website Engagement

The analysis evaluates:

* Pageviews per session
* Bounced sessions
* Overall bounce rate
* Engagement differences across landing pages

### Landing Pages

The analysis answers:

* Which landing pages receive the most sessions?
* Which landing pages convert best?
* Which landing pages have the highest bounce rates?
* How does revenue efficiency differ across landing pages?
* Which landing pages should be prioritized for optimization?

### Conversion Depth

The analysis evaluates how conversion changes as visitors view more pages during their sessions.

This helps identify the relationship between **website engagement and purchase behavior**.

### Purchasing Funnel

The analysis tracks progression through the major purchasing stages:

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

This answers:

* How many sessions reach each stage?
* Where does the customer journey lose the most potential customers?
* Which funnel stages deserve further investigation?
* Could device behavior help explain differences in conversion?

Phase 2 therefore moves the analysis from:

> **How much traffic and revenue does the business have?**

toward:

> **How do visitors behave, where do they drop off, and where are the strongest optimization opportunities?**

---

# Core KPIs Calculated

The SQL analysis produces the core metrics used throughout the project.

### Website Performance

* Sessions
* Pageviews
* Pageviews per Session
* Bounced Sessions
* Bounce Rate

### Conversion

* Orders
* Conversion Rate
* Conversion by Traffic Source
* Conversion by Device
* Conversion by Landing Page
* Conversion by Pageview Depth

### Revenue

* Revenue
* Average Order Value (AOV)
* Revenue per Session
* Revenue per Order

### Product Performance

* Product Orders / Items
* Units Sold
* Product Revenue
* Revenue per Product Order
* Product Revenue Over Time

### Funnel Performance

* Sessions reaching each funnel stage
* Stage-to-stage progression
* Funnel drop-off

---

# SQL Concepts Demonstrated

The SQL analysis demonstrates practical SQL skills used in business analytics.

The main concepts include:

* `SELECT`
* `FROM`
* `WHERE`
* `GROUP BY`
* `ORDER BY`
* `HAVING`
* `DISTINCT`
* `COUNT`
* `COUNT(DISTINCT ...)`
* `SUM`
* `AVG`
* `ROUND`
* `CASE`
* `IN`
* `IFNULL`
* `JOIN`
* `LEFT JOIN`
* Simple subqueries

These techniques are applied to real business questions rather than isolated syntax exercises.

The emphasis is on producing **clear, explainable analytical queries** that connect database records to business KPIs.

---

# Analytical Workflow

The SQL phase follows this general process:

```text
SQLite Database
      ↓
Business Question
      ↓
SQL Query
      ↓
Aggregated Analytical Result
      ↓
Business Interpretation
      ↓
CSV Export / Supporting Analysis
      ↓
Power BI Dashboard
```

Each query was developed around a specific analytical question and contributes to the broader business analysis.

---

# SQL Outputs Used in the Project

Selected SQL results are exported to CSV files for use in later stages of the project.

These outputs support:

### Python

Python uses selected SQL outputs for:

* Validation
* Trend exploration
* Supporting visualizations

### Power BI

The SQL analysis provides the analytical foundation for the final Power BI report, including metrics and findings related to:

* Executive performance
* Marketing and traffic
* Conversion funnel
* Product performance
* Device performance
* Website engagement
* Landing-page performance
* Executive insights and recommendations

The SQL phase therefore acts as the **analytical foundation** for the final business intelligence solution.

---

# Analysis Feeding the Power BI Dashboard

The final Power BI dashboard is based on the business questions and analytical results developed during the SQL phase.

The main SQL analysis areas supporting the dashboard include:

| SQL Analysis Area                     | Power BI Business Area                 |
| ------------------------------------- | -------------------------------------- |
| Traffic-source analysis               | Marketing & Traffic                    |
| Revenue and order analysis            | Executive Overview                     |
| Conversion analysis                   | Executive Overview / Conversion Funnel |
| Funnel analysis                       | Conversion Funnel                      |
| Device analysis                       | Device Performance                     |
| Bounce and engagement analysis        | Engagement & Bounce                    |
| Landing-page analysis                 | Landing Page Performance               |
| Product analysis                      | Product Performance                    |
| Business findings and KPI comparisons | Executive Insights & Recommendations   |

This connection ensures that the Power BI dashboard is not an isolated visualization exercise; it is the reporting layer built on top of the underlying analytical work.

---

# Reproducibility

The SQL analysis can be reproduced using the SQLite database included in the repository.

## 1. Open the Database

Open:

```text
database/maven_fuzzy_factory.db
```

using **DB Browser for SQLite** or another SQLite-compatible client.

## 2. Inspect the Tables

Review the available tables and their relationships before running the analytical queries.

## 3. Run the SQL Scripts

Run the SQL analysis scripts in sequence.

The scripts are organized around the project's analytical questions and progressively build the business analysis.

## 4. Review the Results

Compare the query results with the documented observations and business interpretations.

## 5. Export Selected Results

Export the required analytical results to CSV for use in the Python and Power BI stages where applicable.

---

# SQL Resources

The SQL folder contains the analysis scripts used throughout the project.

The scripts are organized sequentially so that the analytical workflow can be followed from foundational business metrics through deeper website engagement, landing-page, and funnel analysis.

The numbering also makes it possible to trace individual analytical questions back to their corresponding SQL query.

---

# Business Value of the SQL Analysis

The SQL phase converts raw relational data into business information that can answer questions such as:

> Which acquisition channels perform best?

> Which devices convert most effectively?

> Which landing pages should be optimized?

> Where does the purchasing funnel lose potential customers?

> Which products drive revenue?

> How does website engagement relate to conversion?

These results provide the evidence used to identify the project's main business opportunities.

---

# SQL Phase Outcome

The SQL analysis established the analytical foundation for the complete Maven Fuzzy Factory project.

It transformed the raw database into measurable business performance indicators and identified several important findings, including:

* A significant difference between desktop and mobile conversion
* Strong and weak landing-page performance
* Differences between traffic volume and traffic quality
* Significant purchasing-funnel drop-off
* Strong revenue concentration around The Original Mr. Fuzzy
* Opportunities for website and conversion optimization

The SQL phase therefore serves as the bridge between the **raw database** and the project's final **Python validation, Power BI dashboard, and business recommendations**.

> **Raw Data → SQL Analysis → Validated Results → Power BI → Business Insights**
