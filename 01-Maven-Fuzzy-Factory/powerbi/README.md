# Power BI Dashboard — Maven Fuzzy Factory

## Overview

The **Power BI report** is the primary business intelligence and reporting layer of the Maven Fuzzy Factory project.

The dashboard transforms the analytical results developed during the SQL and Python phases into an interactive reporting solution designed to help stakeholders understand:

* Overall business performance
* Marketing and traffic-source performance
* Website conversion
* Purchasing funnel behavior
* Product performance
* Device differences
* Website engagement
* Landing-page performance
* Key business opportunities and recommendations

The report is designed to move from **high-level business performance to detailed analysis and finally to actionable recommendations**.

---

# Dashboard Structure

The final Power BI report contains **8 pages**.

| Page                                          | Business Purpose                                                                                                |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **01 — Executive Overview**                   | Provides a high-level view of business performance, including key revenue, order, conversion, and trend metrics |
| **02 — Marketing & Traffic**                  | Evaluates traffic sources using sessions, conversion, revenue, AOV, and other performance indicators            |
| **03 — Conversion Funnel**                    | Analyzes visitor progression through the purchasing journey and identifies major drop-off points                |
| **04 — Product Performance**                  | Evaluates product revenue, orders, units sold, and product contribution                                         |
| **05 — Device Performance**                   | Compares desktop and mobile traffic, conversion, revenue, and order value                                       |
| **06 — Engagement & Bounce**                  | Examines website engagement, pageview behavior, and bounce performance                                          |
| **07 — Landing Page Performance**             | Compares landing pages using traffic, conversion, bounce rate, and revenue efficiency                           |
| **08 — Executive Insights & Recommendations** | Summarizes the most important findings and translates them into business priorities                             |

---

# 01 — Executive Overview

The Executive Overview provides the high-level business perspective of the e-commerce operation.

It is designed to answer:

> **How is the business performing overall?**

The page brings together the most important performance indicators and trends so that a stakeholder can understand the overall situation before moving into more detailed analysis.

The page acts as the primary entry point into the dashboard.

---

# 02 — Marketing & Traffic

This page evaluates the performance of the website's acquisition sources.

The analysis considers multiple dimensions of channel performance rather than traffic volume alone.

Key measures include:

* Sessions
* Conversion Rate
* Revenue
* Average Order Value
* Revenue per Session
* Traffic-source contribution

The page supports the business question:

> **Which traffic sources generate the greatest business value?**

A key finding from the analysis is that **traffic volume and traffic quality are not the same thing**.

For example, gsearch generated the largest amount of traffic and revenue, while Direct / NULL achieved a higher conversion rate.

This demonstrates why acquisition channels should be evaluated using multiple KPIs.

---

# 03 — Conversion Funnel

The Conversion Funnel page analyzes visitor progression through the purchasing journey.

The funnel follows the major website stages:

```text id="gxxm99"
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

The analysis is designed to identify where potential customers are lost before completing a purchase.

Key questions include:

* How many sessions reach each stage?
* Where are the largest drop-offs?
* Which stages require further investigation?
* Could device behavior help explain funnel differences?

The funnel analysis is particularly important when combined with the device analysis because mobile users have substantially lower conversion than desktop users.

---

# 04 — Product Performance

The Product Performance page evaluates the contribution of individual products to the business.

The analysis includes measures such as:

* Product revenue
* Product orders / items
* Units sold
* Revenue per product order
* Product performance over time

A major finding is the strong contribution of **The Original Mr. Fuzzy**, which generated approximately **62% of total product revenue**.

This indicates strong performance from the leading product while also highlighting potential concentration within the product portfolio.

The page helps answer:

> **Which products drive revenue, and where are there opportunities to strengthen the broader product portfolio?**

---

# 05 — Device Performance

The Device Performance page compares customer behavior between desktop and mobile.

The analysis includes:

* Sessions
* Orders
* Conversion Rate
* Revenue
* Average Order Value
* Revenue efficiency

The primary finding is the significant conversion gap:

| Device  | Sessions | Orders | Conversion Rate |    AOV |
| ------- | -------: | -----: | --------------: | -----: |
| Desktop |  327,027 | 27,805 |       **8.50%** | $59.91 |
| Mobile  |  145,844 |  4,508 |       **3.09%** | $60.50 |

The similar AOV values indicate that the main difference is not the value of completed orders, but the probability of completing a purchase.

This makes mobile conversion one of the project's most important optimization opportunities.

---

# 06 — Engagement & Bounce

The Engagement & Bounce page evaluates how visitors interact with the website before purchasing.

The analysis includes metrics related to:

* Pageviews
* Pageviews per Session
* Bounced Sessions
* Bounce Rate
* Engagement behavior

The purpose is to understand whether differences in website engagement may help explain differences in conversion performance.

This analysis provides additional context for the landing-page and funnel findings.

---

# 07 — Landing Page Performance

The Landing Page Performance page evaluates the effectiveness of the pages where visitors begin their website sessions.

The analysis considers:

* Sessions
* Conversion Rate
* Bounce Rate
* Revenue per Session
* Relative landing-page performance

Two pages provide particularly strong contrasts.

### `/lander-5`

* Conversion Rate: **10.17%**
* Bounce Rate: **36.87%**
* Revenue per Session: **$6.43**

This makes `/lander-5` the strongest landing page identified in the analysis.

### `/lander-3`

* Conversion Rate: **3.39%**
* Bounce Rate: **50.29%**

This makes `/lander-3` a clear optimization opportunity.

The dashboard allows these differences to be evaluated alongside other performance indicators rather than relying on conversion rate alone.

---

# 08 — Executive Insights & Recommendations

The final page translates the dashboard findings into business priorities.

The main recommendations are:

### Priority 1 — Investigate Mobile Conversion

Mobile conversion is substantially below desktop conversion.

Investigate the mobile purchasing journey, especially checkout and other potential friction points.

### Priority 2 — Optimize Underperforming Landing Pages

Use `/lander-5` as a benchmark and prioritize `/lander-3` for further investigation and testing.

### Priority 3 — Investigate Funnel Drop-Off

Identify the largest stage-to-stage losses, particularly during checkout.

### Priority 4 — Evaluate Traffic Sources by Business Value

Compare acquisition channels using:

**Sessions + Conversion Rate + Revenue + AOV + Revenue per Session**

### Priority 5 — Strengthen Product Portfolio Performance

Continue supporting The Original Mr. Fuzzy while identifying opportunities to increase the contribution of the remaining products.

---

# Interactivity

The dashboard is designed as an interactive Power BI report rather than a collection of static charts.

Users can interact with the report through available filters and slicers to investigate the data from different perspectives.

The report includes filtering functionality designed to help users:

* Narrow the analysis to relevant periods
* Compare business segments
* Investigate specific traffic sources
* Examine device performance
* Explore landing-page performance
* Analyze product-level results

A **Clear All Slicers** function is also available to make it easier to return the analysis to its default state after applying filters.

---

# Analytical Foundation

The Power BI report is built on the analytical work completed during the earlier project phases.

The overall workflow is:

```text id="w7u1t6"
Raw E-Commerce Data
        ↓
SQLite Database
        ↓
SQL Analysis
        ↓
Selected Results / Validation
        ↓
Python Exploration
        ↓
Power BI Data Model
        ↓
Interactive Dashboard
        ↓
Business Insights
```

### SQL

SQL provides the core analytical calculations and business metrics.

### Python

Python provides supporting validation, exploration, and visualization.

### Power BI

Power BI transforms the analytical results into the final interactive business intelligence solution.

---

# Key Business Metrics

The dashboard evaluates a combination of performance, conversion, engagement, and product metrics.

These include:

* Sessions
* Pageviews
* Orders
* Revenue
* Average Order Value
* Conversion Rate
* Bounce Rate
* Pageviews per Session
* Revenue per Session
* Product Revenue
* Units Sold
* Traffic-source performance
* Device conversion
* Landing-page performance
* Funnel progression

Using multiple metrics prevents individual KPIs from being interpreted without the necessary business context.

---

# Dashboard Design Approach

The report was designed around a simple analytical progression:

```text id="9d2bwl"
Understand Performance
        ↓
Identify Differences
        ↓
Locate Performance Gaps
        ↓
Investigate Possible Causes
        ↓
Prioritize Opportunities
        ↓
Recommend Next Actions
```

The dashboard therefore focuses on **business questions rather than simply displaying charts**.

Each page has a specific analytical purpose and contributes to the overall business story.

---

# Key Findings Communicated by the Dashboard

The final dashboard highlights several important findings:

### Mobile Conversion Gap

**8.50% desktop vs. 3.09% mobile conversion**

### Strongest Landing Page

`/lander-5`

**10.17% conversion rate**

### Weakest Landing Page

`/lander-3`

**3.39% conversion rate**

### Traffic-Source Difference

gsearch generated the most traffic and revenue, while Direct / NULL achieved the highest conversion rate among the analyzed sources.

### Product Concentration

The Original Mr. Fuzzy generated approximately **62% of total product revenue**.

### Funnel Drop-Off

A substantial number of sessions are lost as visitors progress through the purchasing journey.

---

# How to Use the Dashboard

1. Open the final Power BI report.
2. Begin with **Executive Overview** for the high-level business picture.
3. Use **Marketing & Traffic** to investigate acquisition performance.
4. Review **Conversion Funnel** to identify customer journey drop-offs.
5. Explore **Product Performance** to understand product contribution.
6. Compare **Device Performance** to investigate desktop and mobile behavior.
7. Review **Engagement & Bounce** for website behavior.
8. Use **Landing Page Performance** to compare landing-page effectiveness.
9. Finish with **Executive Insights & Recommendations** for the main business conclusions.

Use the available slicers and filters to investigate specific segments and return to the default report state using **Clear All Slicers** when needed.

---

# Final Outcome

The Power BI report transforms the project's analytical results into an interactive business intelligence solution.

It allows a stakeholder to move from:

> **What is happening?**

to:

> **Where is the performance gap?**

and finally:

> **What should the business investigate or improve?**

The dashboard demonstrates the ability to combine analytical results, data modeling, visualization, KPI design, interactive reporting, and business interpretation into a single BI solution.

> **SQL → Python → Power BI → Business Insights → Recommendations**
