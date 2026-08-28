## Section 22 - Pageviews per Session

### Business Objective

Determine how many pages visitors view during each website session.

### SQL Concepts

- COUNT()
- GROUP BY

### Observation

The analysis shows that website sessions can contain different numbers of pageviews. Some sessions contain only one pageview, while others contain multiple pageviews.

For example:

- Session 1: 1 pageview
- Session 6: 6 pageviews
- Session 15: 3 pageviews
- Session 16: 2 pageviews
- Session 20: 7 pageviews

Sessions with exactly one pageview represent potential bounced sessions, while sessions with multiple pageviews indicate that visitors continued navigating through the website.

### Business Insight

Pageviews per session provides the foundation for measuring visitor engagement. Identifying sessions with exactly one pageview allows the business to calculate Bounce Rate and determine which landing pages may have difficulty engaging visitors.

### Future Analysis

- Identify bounced sessions.
- Calculate overall Bounce Rate.
- Calculate Bounce Rate by landing page.
- Compare engagement across landing pages.

## Section 23 - Identifying Bounced Sessions

### Business Objective

Identify website sessions where visitors viewed exactly one page.

### SQL Concepts

- GROUP BY
- COUNT()
- HAVING
- Aggregate filtering

### Observation

(To be completed after running the query.)

### Business Insight

Identifying bounced sessions allows the business to measure how frequently visitors leave after viewing only one page. This is the foundation for calculating Bounce Rate and evaluating landing page engagement.

### Future Analysis

- Calculate total bounced sessions.
- Calculate overall Bounce Rate.
- Calculate Bounce Rate by landing page.

## Section 24 - Overall Bounce Rate

### Business Objective

Calculate the percentage of website sessions that ended after visitors viewed only one page.

### Metric

Bounce Rate = Bounced Sessions / Total Sessions × 100

### Observation

The analysis identified 211,640 bounced sessions out of 472,871 total website sessions.

The resulting Bounce Rate is 44.76%, meaning that approximately 45% of website sessions ended after the visitor viewed only one page.

### Business Insight

A Bounce Rate of 44.76% indicates that a significant portion of website visitors leave without navigating beyond their initial page. This provides an overall measure of website engagement, but it does not show which landing pages are responsible for the highest levels of visitor abandonment.

The next analysis will compare Bounce Rate across landing pages to identify specific pages with higher or lower visitor engagement.

### Future Analysis

- Bounce Rate by landing page.
- Compare Bounce Rate with conversion rate.
- Identify high-traffic pages with high Bounce Rate.
- Identify landing pages with optimization opportunities.

## Section 25 - Bounce Rate by Landing Page

### Business Objective

Determine which landing pages have the highest percentage of visitors leaving after viewing only one page.

### SQL Concepts

- Subqueries
- INNER JOIN
- GROUP BY
- COUNT()
- SUM()
- CASE
- ROUND()

### Observation

Bounce Rate by landing page:

- /lander-1: 53.24% (47,574 sessions, 25,330 bounced sessions)
- /lander-4: 51.69% (9,385 sessions, 4,851 bounced sessions)
- /lander-3: 50.29% (79,000 sessions, 39,733 bounced sessions)
- /lander-2: 45.17% (131,170 sessions, 59,249 bounced sessions)
- /home: 41.68% (137,576 sessions, 57,346 bounced sessions)
- /lander-5: 36.87% (68,166 sessions, 25,131 bounced sessions)

The overall website Bounce Rate is 44.76%. Several landing pages perform worse than the overall average, particularly /lander-1, /lander-4, and /lander-3.

The strongest engagement is observed on /lander-5, which has the lowest Bounce Rate at 36.87%. This is also the landing page with the highest conversion rate at 10.17%.

### Business Insight

Landing page engagement appears to be related to conversion performance. /lander-5 has the lowest Bounce Rate and the highest Conversion Rate, suggesting that visitors who enter through this page are more likely to continue navigating and eventually make a purchase.

In contrast, /lander-3 and /lander-1 have high Bounce Rates and relatively low Conversion Rates. /lander-3 is particularly important because it receives 79,000 sessions, meaning that a large number of visitors are leaving after viewing only one page.

These results suggest that improving visitor engagement on high-traffic pages such as /lander-3 could provide an opportunity to increase conversions without requiring additional website traffic.

### Future Analysis

- Compare Bounce Rate directly with Conversion Rate.
- Investigate pageviews per session by landing page.
- Identify high-traffic pages with high Bounce Rate.
- Analyze the relationship between engagement and revenue.
- Prioritize landing page optimization opportunities.

## Section 26 - Pageviews per Session by Landing Page

### Business Objective

Determine how deeply visitors explore the website after entering through each landing page.

### Metric

Average Pageviews per Session = Total Pageviews / Sessions

### SQL Concepts

- Subqueries
- INNER JOIN
- GROUP BY
- COUNT()
- SUM()
- AVG()
- ROUND()

### Observation

Average Pageviews per Session by landing page:

- /lander-5: 2.90 pageviews per session (68,166 sessions, 197,884 pageviews)
- /home: 2.59 pageviews per session (137,576 sessions, 355,925 pageviews)
- /lander-2: 2.56 pageviews per session (131,170 sessions, 335,780 pageviews)
- /lander-4: 2.43 pageviews per session (9,385 sessions, 22,800 pageviews)
- /lander-1: 2.20 pageviews per session (47,574 sessions, 104,428 pageviews)
- /lander-3: 2.17 pageviews per session (79,000 sessions, 171,307 pageviews)

The highest average engagement occurs on /lander-5, where visitors view an average of 2.90 pages per session. This is consistent with its low Bounce Rate of 36.87% and high Conversion Rate of 10.17%.

In contrast, /lander-3 has the lowest average pageviews per session at 2.17. This is consistent with its high Bounce Rate of 50.29% and low Conversion Rate of 3.39%.

### Business Insight

Average Pageviews per Session provides additional evidence that visitor engagement is strongly associated with landing page performance. /lander-5 not only generates the highest conversion rate and Revenue per Session, but also encourages visitors to explore more pages.

The lower engagement observed on /lander-3 is particularly important because the page receives 79,000 sessions. Improving visitor engagement on this page could create an opportunity to increase conversions and revenue without requiring additional traffic.

### Future Analysis

- Compare page engagement with conversion rate.
- Analyze the relationship between pageviews and purchases.
- Identify pages that contribute to the customer journey.
- Investigate high-traffic pages with low engagement.

## Section 27 - Customer Journey of Ordered Sessions

### Business Objective

Investigate the pageview sequence of sessions that resulted in a completed order.

### Business Question

What pages do visitors typically navigate through before completing a purchase?

### Observation

Validation of ordered sessions showed that all 32,313 ordered sessions contain exactly seven pageviews.

The observed customer journey follows a consistent sequence:

1. /home
2. /products
3. /the-original-mr-fuzzy
4. /cart
5. /shipping
6. /billing
7. /thank-you-for-your-order

The final page represents the completed purchase confirmation.

### Business Insight

The dataset shows a highly structured customer journey from website entry to purchase. Visitors who complete an order progress through the main product, cart, shipping, billing, and order confirmation stages.

This provides a clear representation of the e-commerce purchase funnel:

Visitor → Product Discovery → Product → Cart → Shipping → Billing → Purchase

The analysis also explains why all recorded orders appear in the 5+ pageview engagement category: completed orders contain exactly seven pageviews.

This finding should be interpreted as a characteristic of the dataset's recorded customer journey rather than a general rule that customers must view seven pages before purchasing.

### Future Analysis

- Analyze abandonment at each stage of the purchase funnel.
- Calculate conversion rates between funnel stages.
- Identify where visitors leave before completing an order.
- Analyze product-level purchase behavior.

## Section 28 - Purchase Funnel Pages

### Business Objective

Identify the main pages involved in the customer purchasing journey and determine how many website sessions reached each stage.

### SQL Concepts

- CASE
- COUNT(DISTINCT)
- GROUP BY
- ORDER BY
- Data normalization
- Funnel analysis

### Observation

The analysis identified the following number of sessions reaching each funnel stage:

- /home: 137,576 sessions
- /products: 261,231 sessions
- /the-original-mr-fuzzy: 162,525 sessions
- /cart: 94,953 sessions
- /shipping: 64,484 sessions
- /billing: 52,058 sessions
- /thank-you-for-your-order: 32,313 sessions

The billing stage required additional investigation because the database contains two billing-related URLs: /billing and /billing-2. These URLs were grouped together because they represent the same business stage of the checkout process.

Initial analysis using only /billing identified only 3,617 sessions. After including /billing-2, the billing stage increased to 52,058 sessions.

The analysis also showed that the /home page should not be interpreted as a mandatory first step of the purchase funnel because visitors can enter the website through other landing pages such as /lander-1, /lander-2, /lander-3, /lander-4, and /lander-5.

### Business Insight

The customer journey contains several important stages between website entry and completed purchase:

Landing Page → Products → Product Detail → Cart → Shipping → Billing → Order Confirmation

The number of sessions decreases substantially as visitors progress through the purchasing process.

The final purchase confirmation page contains 32,313 sessions, matching the total number of orders identified earlier in the project.

This indicates that the /thank-you-for-your-order page is strongly associated with completed purchases and can be used as the final stage of the purchase funnel.

The analysis also demonstrates the importance of understanding the data structure before calculating business metrics. The initial billing analysis would have underestimated the number of sessions reaching the billing stage because it considered only one of the two billing URLs.

### Important Data Observation

The database contains multiple URLs representing the billing stage:

- /billing
- /billing-2

For business analysis, these URLs should be treated as one logical funnel stage.

### Business Questions

- At which funnel stage do the most visitors drop out?
- What percentage of visitors continue from one stage to the next?
- Which stage represents the largest conversion opportunity?
- How much revenue could potentially be recovered by improving funnel performance?

### Future Analysis

- Calculate stage-to-stage conversion rates.
- Calculate funnel drop-off rates.
- Identify the largest abandonment point.
- Compare funnel performance by device.
- Compare funnel performance by traffic source.

## Section 29 - Funnel Stage Conversion and Drop-Off

### Business Objective

Measure how effectively website sessions move from one purchasing stage to the next and identify where the largest drop-offs occur.

### Funnel Stages

- /products
- /the-original-mr-fuzzy
- /cart
- /shipping
- /billing
- /thank-you-for-your-order

### Query Results

| Funnel Stage | Sessions | Conversion Rate |
|---|---:|---:|
| /products | 261231 | - |
| /the-original-mr-fuzzy | 162525 | 62.22% |
| /cart | 94953 | 58.42% |
| /shipping | 64484 | 67.91% |
| /billing | 52058 | 80.73% |
| /thank-you-for-your-order | 32313 | 62.07% |

### Interpretation

The percentage of sessions continuing to the next funnel stage varies significantly across the purchasing process.

The largest stage-to-stage drop-off occurs between the product-detail page and the cart.

The conversion rate from /the-original-mr-fuzzy to /cart is 58.42%, meaning that 41.58% of sessions reaching the product-detail page do not reach the cart.

The second major drop-off occurs between the billing stage and the purchase confirmation page.

The conversion rate from /billing to /thank-you-for-your-order is 62.07%, representing a 37.93% drop-off.

The strongest transition occurs between /shipping and /billing, with an 80.73% conversion rate.

### Business Insight

The product-detail-to-cart stage represents the largest immediate conversion opportunity in the purchasing funnel.

Visitors are reaching the product page, but a significant percentage do not continue to the cart. This could indicate opportunities to improve the product page, product presentation, pricing communication, calls to action, or other elements that influence the decision to add a product to the cart.

The billing-to-purchase stage is another important area because a substantial percentage of visitors who reach billing do not complete the purchase.

The shipping-to-billing stage performs comparatively well, suggesting that the largest problems are not evenly distributed throughout the checkout process.

### Important Data Observation

The billing stage combines two URLs:

- /billing
- /billing-2

These URLs were treated as one logical business stage because both represent the billing step of the checkout process.

### Business Questions

- Why do many visitors leave the product page before reaching the cart?
- Are there differences in product-page performance by product?
- Why do some visitors reach billing but fail to complete the purchase?
- Does funnel performance differ between desktop and mobile users?
- Does funnel performance differ by traffic source?

### Conclusion

The funnel analysis shows that customer drop-off is concentrated at specific stages rather than being evenly distributed across the purchasing process.

The product-detail-to-cart transition has the lowest stage conversion rate at 58.42%, making it the first area that should be investigated for potential improvement.

The billing-to-purchase transition is the second major opportunity, with a 62.07% conversion rate.

Future analysis should investigate whether these funnel differences are related to device type, traffic source, landing page, or product.

## Section 30 - Funnel Performance by Device

### Business Objective

Compare the purchasing funnel between desktop and mobile users to determine whether customers using different devices experience different conversion rates at each funnel stage.

### Funnel Stages

- /products
- /the-original-mr-fuzzy
- /cart
- /shipping
- /billing
- /thank-you-for-your-order

### Query Results

| Device | Funnel Stage | Sessions | Conversion Rate |
|---|---|---:|---:|
| Desktop | /products | 192325 | - |
| Desktop | /the-original-mr-fuzzy | 127296 | 66.19% |
| Desktop | /cart | 75155 | 59.04% |
| Desktop | /shipping | 52692 | 70.11% |
| Desktop | /billing | 43722 | 82.98% |
| Desktop | /thank-you-for-your-order | 27805 | 63.59% |
| Mobile | /products | 68906 | - |
| Mobile | /the-original-mr-fuzzy | 35229 | 51.13% |
| Mobile | /cart | 19798 | 56.20% |
| Mobile | /shipping | 11792 | 59.56% |
| Mobile | /billing | 8336 | 70.69% |
| Mobile | /thank-you-for-your-order | 4508 | 54.08% |

### Interpretation

The purchasing funnel performs differently between desktop and mobile users.

The largest difference occurs between /products and /the-original-mr-fuzzy.

Desktop users have a conversion rate of 66.19%, while mobile users have a conversion rate of 51.13%.

This represents a difference of 15.06 percentage points.

Mobile users also have lower conversion rates at the cart-to-shipping, shipping-to-billing, and billing-to-purchase stages.

The product-detail-to-cart transition has a smaller difference between desktop and mobile users, with conversion rates of 59.04% and 56.20%, respectively.

### Business Insight

Mobile users consistently convert at lower rates throughout the purchasing funnel.

The largest device difference occurs during the transition from the products page to the product-detail page.

This suggests that the mobile customer experience may have an important opportunity for improvement, particularly during product discovery and navigation.

However, the analysis identifies an association rather than a specific cause. Additional analysis is required to determine why mobile users perform worse.

### Management Questions

- Why do fewer mobile visitors move from /products to the product-detail page?
- Is the mobile product-navigation experience different from desktop?
- Are mobile users experiencing more difficulty during checkout?
- Does mobile funnel performance differ by traffic source?
- Does mobile funnel performance differ by landing page?

### Conclusion

Desktop users consistently move through the purchasing funnel at higher rates than mobile users.

The largest difference occurs at the transition from /products to /the-original-mr-fuzzy, where mobile conversion is 15.06 percentage points lower than desktop.

The difference continues through later stages of the funnel, including checkout and purchase completion.

Mobile funnel performance should therefore be investigated further to identify the underlying causes and potential opportunities for improvement.

## Section 31 - Funnel Performance by Traffic Source and Device

### Business Objective

Determine whether the lower mobile funnel performance identified in the device analysis is consistent across different traffic sources.

Traffic sources analyzed:

- Direct / Untagged
- bsearch
- gsearch
- socialbook

### Query Results

The analysis compared funnel conversion rates for desktop and mobile users within each traffic source.

#### Products → Product Detail

| Traffic Source | Desktop | Mobile | Difference |
|---|---:|---:|---:|
| Direct / Untagged | 65.50% | 50.69% | 14.81 pp |
| bsearch | 65.49% | 50.84% | 14.65 pp |
| gsearch | 66.57% | 51.32% | 15.25 pp |
| socialbook | 64.35% | 47.61% | 16.74 pp |

#### Product Detail → Cart

| Traffic Source | Desktop | Mobile |
|---|---:|---:|
| Direct / Untagged | 60.48% | 56.57% |
| bsearch | 59.36% | 57.27% |
| gsearch | 58.50% | 55.89% |
| socialbook | 64.69% | 68.62% |

#### Cart → Shipping

| Traffic Source | Desktop | Mobile |
|---|---:|---:|
| Direct / Untagged | 70.05% | 60.21% |
| bsearch | 70.52% | 60.92% |
| gsearch | 70.02% | 59.27% |
| socialbook | 70.74% | 58.54% |

#### Shipping → Billing

| Traffic Source | Desktop | Mobile |
|---|---:|---:|
| Direct / Untagged | 82.64% | 70.97% |
| bsearch | 82.58% | 73.43% |
| gsearch | 83.15% | 70.38% |
| socialbook | 83.81% | 71.88% |

#### Billing → Purchase

| Traffic Source | Desktop | Mobile |
|---|---:|---:|
| Direct / Untagged | 64.20% | 53.76% |
| bsearch | 64.00% | 55.25% |
| gsearch | 63.30% | 54.08% |
| socialbook | 65.45% | 55.07% |

### Interpretation

Mobile users generally have lower funnel conversion rates than desktop users across the major traffic sources.

The largest and most consistent difference occurs between /products and /the-original-mr-fuzzy.

The mobile conversion rate is approximately 15 to 17 percentage points lower than desktop across the four traffic sources.

Mobile users also have lower conversion rates during the cart-to-shipping, shipping-to-billing, and billing-to-purchase stages.

One exception occurs for socialbook during the product-detail-to-cart transition, where mobile conversion is higher than desktop.

Because socialbook has relatively low traffic volume, this result should be interpreted cautiously.

### Business Insight

The mobile conversion disadvantage does not appear to be isolated to a single traffic source.

The consistency of the difference across multiple acquisition channels suggests that the issue may be related to the mobile customer experience rather than one specific marketing channel.

The strongest and most consistent difference occurs when users move from the products page to the product-detail page.

However, the analysis identifies where the performance difference exists but does not establish the specific cause.

### Management Questions

- Why is mobile product-detail conversion consistently lower across traffic sources?
- Is the mobile website experience different from desktop?
- Are mobile users experiencing more difficulty navigating from /products to the product page?
- Does the mobile checkout experience create additional friction?
- Are certain landing pages particularly problematic for mobile users?
- Does mobile performance vary by product?

### Conclusion

The analysis demonstrates that the mobile conversion disadvantage is consistent across the major traffic sources.

The largest difference occurs between /products and /the-original-mr-fuzzy, where mobile conversion is approximately 15 to 17 percentage points lower than desktop depending on the traffic source.

Mobile users also show lower conversion rates during later checkout stages across almost every traffic source.

The data therefore suggests that mobile performance should be investigated as a broader customer-experience issue rather than as a problem associated with a single acquisition channel.

Further analysis should examine landing pages and products to determine which areas contribute most to the mobile conversion gap.

## Section 32 - Landing Page Performance by Device

### Business Objective

After discovering that mobile users have lower conversion rates across traffic sources, the next objective was to determine whether certain landing pages contribute more strongly to the mobile conversion gap.

The analysis compares landing pages by device type using sessions, orders, and conversion rate.

### SQL Files

- `32_1_landing_page_by_device.sql`
- `32_2_landing_page_conversion_by_device.sql`

### Query Results

#### Landing Page Sessions by Device

| Device | Landing Page | Sessions |
|---|---|---:|
| Desktop | /home | 87263 |
| Desktop | /lander-1 | 37460 |
| Desktop | /lander-2 | 124753 |
| Desktop | /lander-4 | 9385 |
| Desktop | /lander-5 | 68166 |
| Mobile | /home | 50313 |
| Mobile | /lander-1 | 10114 |
| Mobile | /lander-2 | 6417 |
| Mobile | /lander-3 | 79000 |

The landing page session totals reconcile with the previously established device totals.

Desktop:

327027 sessions

Mobile:

145844 sessions

#### Landing Page Conversion by Device

| Device | Landing Page | Sessions | Orders | Conversion Rate |
|---|---|---:|---:|---:|
| Desktop | /home | 87263 | 8222 | 9.42% |
| Desktop | /lander-1 | 37460 | 1997 | 5.33% |
| Desktop | /lander-2 | 124753 | 9948 | 7.97% |
| Desktop | /lander-4 | 9385 | 708 | 7.54% |
| Desktop | /lander-5 | 68166 | 6930 | 10.17% |
| Mobile | /home | 50313 | 1489 | 2.96% |
| Mobile | /lander-1 | 10114 | 160 | 1.58% |
| Mobile | /lander-2 | 6417 | 180 | 2.81% |
| Mobile | /lander-3 | 79000 | 2679 | 3.39% |

### Interpretation

Landing page performance varies substantially by device.

For desktop users, /lander-5 has the highest conversion rate at 10.17%, followed by /home at 9.42%.

For mobile users, /lander-3 has the highest conversion rate in the available data at 3.39%, followed by /home at 2.96%.

The lowest-performing landing page in the available data is /lander-1, with a conversion rate of 5.33% on desktop and 1.58% on mobile.

The difference between desktop and mobile conversion for /lander-1 is 3.75 percentage points.

Not every landing page appears for both devices in the dataset. Therefore, comparisons between different landing pages across devices should be made carefully.

### Business Insight

Landing page performance is strongly associated with conversion performance and varies by device.

The most concerning result is /lander-1, which has a particularly low mobile conversion rate of 1.58%.

This suggests that /lander-1 should be investigated further, especially from a mobile user-experience perspective.

However, the analysis identifies an association and does not establish that the landing page itself is the cause of the lower conversion rate.

Traffic source, campaign, and customer intent may also influence the results.

### Management Questions

- Why does /lander-1 have such a low conversion rate?
- Why is /lander-1 particularly weak for mobile users?
- What traffic sources and campaigns send users to each landing page?
- Are different customer segments being directed to different landing pages?
- Was /lander-3 specifically designed for mobile traffic?
- Why does /lander-5 perform so well for desktop users?
- Should underperforming landing pages be redesigned or tested?

### Conclusion

Landing page performance varies substantially by device.

Desktop users show their highest conversion rate on /lander-5 at 10.17%, while mobile users show their highest conversion rate in the available data on /lander-3 at 3.39%.

The most concerning result is /lander-1, which converts at 1.58% on mobile and 5.33% on desktop.

This suggests that landing page performance should be considered when investigating the broader mobile conversion problem.

Because some landing pages appear only for certain devices in this dataset, comparisons should be made carefully.

The next analysis should investigate landing page performance by traffic source and device to determine whether the performance differences are related to the type of traffic received by each landing page.

## STEP 33 — Conversion Rate by Traffic Source, Device & Landing Page

### Objective

Determine how effectively different combinations of traffic source, device type, and landing page convert website sessions into orders.

This analysis builds on the previous landing-page and device analyses.

The objective is to identify whether the mobile conversion problem is consistent across traffic sources and landing pages, and to identify landing pages that perform particularly well or poorly.

---

### Business Question

Which combinations of traffic source, device, and landing page generate the strongest and weakest conversion rates?

---

### SQL File

`sql/phase_2/33_2_landing_page_source_device_conversion.sql`

---

### SQL Approach

The analysis:

1. Identifies the first pageview for each website session.
2. Uses the first pageview URL as the landing page.
3. Groups sessions by traffic source, device type, and landing page.
4. Counts unique sessions.
5. Counts unique orders associated with those sessions.
6. Calculates conversion rate.

Traffic source NULL values are displayed as `Direct / Untagged` using `IFNULL()`.

The conversion rate is calculated as:

Conversion Rate = Orders / Sessions × 100

---

### Key Results

#### Direct / Untagged

| Device | Landing Page | Sessions | Orders | Conversion Rate |
|---|---|---:|---:|---:|
| Desktop | /home | 51,576 | 5,102 | 9.89% |
| Mobile | /home | 31,752 | 1,016 | 3.20% |

#### bsearch

| Device | Landing Page | Sessions | Orders | Conversion Rate |
|---|---|---:|---:|---:|
| Desktop | /home | 6,867 | 677 | 9.86% |
| Desktop | /lander-1 | 8,611 | 467 | 5.42% |
| Desktop | /lander-2 | 23,588 | 1,745 | 7.40% |
| Desktop | /lander-4 | 1,903 | 130 | 6.83% |
| Desktop | /lander-5 | 13,293 | 1,242 | 9.34% |
| Mobile | /home | 1,047 | 24 | 2.29% |
| Mobile | /lander-1 | 848 | 11 | 1.30% |
| Mobile | /lander-2 | 488 | 18 | 3.69% |
| Mobile | /lander-3 | 6,178 | 205 | 3.32% |

#### gsearch

| Device | Landing Page | Sessions | Orders | Conversion Rate |
|---|---|---:|---:|---:|
| Desktop | /home | 28,820 | 2,443 | 8.48% |
| Desktop | /lander-1 | 28,849 | 1,530 | 5.30% |
| Desktop | /lander-2 | 95,053 | 7,898 | 8.31% |
| Desktop | /lander-4 | 7,482 | 578 | 7.73% |
| Desktop | /lander-5 | 54,873 | 5,688 | 10.37% |
| Mobile | /home | 17,514 | 449 | 2.56% |
| Mobile | /lander-1 | 9,266 | 149 | 1.61% |
| Mobile | /lander-2 | 5,929 | 162 | 2.73% |
| Mobile | /lander-3 | 68,249 | 2,436 | 3.57% |

#### socialbook

| Device | Landing Page | Sessions | Orders | Conversion Rate |
|---|---|---:|---:|---:|
| Desktop | /lander-2 | 6,112 | 305 | 4.99% |
| Mobile | /lander-3 | 4,573 | 38 | 0.83% |

---

### Key Findings

#### 1. Mobile conversion is consistently lower

The mobile conversion rate is substantially lower than desktop across multiple traffic sources and landing pages.

Examples:

- Direct / Untagged /home:
  - Desktop: 9.89%
  - Mobile: 3.20%

- bsearch /lander-1:
  - Desktop: 5.42%
  - Mobile: 1.30%

- gsearch /lander-2:
  - Desktop: 8.31%
  - Mobile: 2.73%

This indicates that the mobile conversion gap is not isolated to one traffic source.

---

#### 2. gsearch desktop + /lander-5 is a strong combination

This combination generated:

- 54,873 sessions
- 5,688 orders
- 10.37% conversion rate

It is one of the strongest high-volume combinations in the analysis.

---

#### 3. /lander-1 shows relatively weak conversion

For gsearch:

- Desktop: 5.30%
- Mobile: 1.61%

For bsearch:

- Desktop: 5.42%
- Mobile: 1.30%

The landing page performs relatively poorly across both traffic sources and both device types.

This suggests that /lander-1 should be considered for further investigation.

---

#### 4. socialbook mobile has the lowest observed conversion rate

socialbook + mobile + /lander-3:

- 4,573 sessions
- 38 orders
- 0.83% conversion rate

However, this segment has substantially less traffic than the major gsearch segments, so the result should be interpreted with volume in mind.

---

### Business Interpretation

The analysis provides evidence that the mobile conversion problem is consistent across multiple traffic sources and landing pages.

Desktop users generally convert at substantially higher rates than mobile users, even when comparing the same traffic source and landing page.

The results also identify /lander-5 as a strong desktop landing page, particularly for gsearch traffic, while /lander-1 shows relatively weak conversion performance across multiple traffic sources.

The analysis does not establish the cause of the mobile conversion gap or the poor performance of /lander-1. Possible explanations would require additional analysis and should not be treated as conclusions at this stage.

---

### Analyst Notes

This analysis combines three dimensions:

Traffic Source → Device → Landing Page

The analysis helps identify specific combinations that may require optimization rather than treating all traffic or all mobile users as one group.

The next analysis should investigate the customer journey after the landing page to determine where users are being lost in the purchase funnel.

## STEP 34 — Funnel Performance by Traffic Source & Device

### Objective

Analyze the purchase funnel by traffic source and device type to determine whether desktop and mobile users behave differently throughout the purchase process.

This step builds on the previous funnel analysis by combining:

- Traffic source (`utm_source`)
- Device type (`device_type`)
- Funnel stage
- Stage-to-stage conversion rate

---

### Business Question

Does funnel performance differ between desktop and mobile users across different traffic sources, and where are the largest differences occurring?

---

### SQL Files

`sql/phase_2/34_0_funnel_source_device_sessions.sql`

`sql/phase_2/34_1_funnel_conversion_source_device.sql`

---

### Funnel Structure

The purchase funnel analyzed was:

Products
→ Product Detail
→ Cart
→ Shipping
→ Billing
→ Order

The `/billing` and `/billing-2` URLs were treated as the same `/billing` funnel stage.

---

## STEP 34.1 — Funnel Sessions by Traffic Source & Device

### Purpose

Count the number of unique website sessions reaching each funnel stage, grouped by traffic source and device type.

### Main SQL Concepts Used

- SELECT
- FROM
- WHERE
- GROUP BY
- ORDER BY
- COUNT(DISTINCT ...)
- CASE
- IFNULL()
- INNER JOIN
- IN

### Result

| Traffic Source | Device | Products | Product Detail | Cart | Shipping | Billing | Orders |
|---|---|---:|---:|---:|---:|---:|---:|
| Direct / Untagged | Desktop | 34,657 | 22,699 | 13,728 | 9,616 | 7,947 | 5,102 |
| Direct / Untagged | Mobile | 15,425 | 7,819 | 4,423 | 2,663 | 1,890 | 1,016 |
| bsearch | Desktop | 29,411 | 19,260 | 11,432 | 8,062 | 6,658 | 4,261 |
| bsearch | Mobile | 3,586 | 1,823 | 1,044 | 636 | 467 | 258 |
| gsearch | Desktop | 126,369 | 84,122 | 49,209 | 34,458 | 28,651 | 18,137 |
| gsearch | Mobile | 49,393 | 25,348 | 14,167 | 8,397 | 5,910 | 3,196 |
| socialbook | Desktop | 1,888 | 1,215 | 786 | 556 | 466 | 305 |
| socialbook | Mobile | 502 | 239 | 164 | 96 | 69 | 38 |

---

## STEP 34.2 — Funnel Stage Conversion by Traffic Source & Device

### Purpose

Calculate the percentage of sessions progressing from one funnel stage to the next for each traffic source and device type.

### Formula

Stage Conversion Rate:

`Current Stage Sessions / Previous Stage Sessions × 100`

### Result

| Traffic Source | Device | Products → Detail | Detail → Cart | Cart → Shipping | Shipping → Billing | Billing → Order |
|---|---|---:|---:|---:|---:|---:|
| Direct / Untagged | Desktop | 65.50% | 60.48% | 70.05% | 82.64% | 64.20% |
| Direct / Untagged | Mobile | 50.69% | 56.57% | 60.21% | 70.97% | 53.76% |
| bsearch | Desktop | 65.49% | 59.36% | 70.52% | 82.58% | 64.00% |
| bsearch | Mobile | 50.84% | 57.27% | 60.92% | 73.43% | 55.25% |
| gsearch | Desktop | 66.57% | 58.50% | 70.02% | 83.15% | 63.30% |
| gsearch | Mobile | 51.32% | 55.89% | 59.27% | 70.38% | 54.08% |
| socialbook | Desktop | 64.35% | 64.69% | 70.74% | 83.81% | 65.45% |
| socialbook | Mobile | 47.61% | 68.62% | 58.54% | 71.88% | 55.07% |

---

## Key Findings

### 1. Mobile users have lower funnel progression than desktop users

The results show a consistent mobile disadvantage across the purchase funnel.

The largest and most consistent difference occurs at:

`Products → Product Detail`

Examples:

- Direct / Untagged:
  - Desktop: 65.50%
  - Mobile: 50.69%
  - Difference: 14.81 percentage points

- bsearch:
  - Desktop: 65.49%
  - Mobile: 50.84%
  - Difference: 14.65 percentage points

- gsearch:
  - Desktop: 66.57%
  - Mobile: 51.32%
  - Difference: 15.25 percentage points

- socialbook:
  - Desktop: 64.35%
  - Mobile: 47.61%
  - Difference: 16.74 percentage points

---

### 2. The mobile problem is not isolated to one traffic source

The lower mobile progression appears across:

- Direct / Untagged
- bsearch
- gsearch
- socialbook

This suggests that the mobile conversion problem is not limited to a single acquisition channel.

---

### 3. Mobile performance remains lower through most funnel stages

For example, gsearch shows:

| Funnel Transition | Desktop | Mobile |
|---|---:|---:|
| Products → Detail | 66.57% | 51.32% |
| Detail → Cart | 58.50% | 55.89% |
| Cart → Shipping | 70.02% | 59.27% |
| Shipping → Billing | 83.15% | 70.38% |
| Billing → Order | 63.30% | 54.08% |

Mobile conversion is lower at every stage for gsearch traffic.

---

### 4. The largest consistent gap occurs between Products and Product Detail

The strongest pattern identified in this analysis is the difference between:

`/products → /the-original-mr-fuzzy`

The mobile conversion rate is approximately 15–17 percentage points lower than desktop across the analyzed traffic sources.

This makes the transition from product browsing to product-detail engagement an important area for further investigation.

---

## Business Interpretation

The analysis confirms that mobile users progress through the purchase funnel less effectively than desktop users.

The pattern is consistent across multiple traffic sources, which strengthens the evidence that the mobile conversion gap is not caused by a single acquisition channel.

The largest and most consistent difference occurs between the products page and the product-detail page.

However, this analysis does not establish the reason for the lower mobile performance.

Possible explanations such as mobile usability, page design, product presentation, navigation, or traffic quality would require additional analysis.

---

## Analyst Conclusion

Mobile users show consistently lower funnel progression than desktop users across traffic sources.

The most significant and consistent difference occurs between the products page and the product-detail page, where mobile conversion is approximately 15–17 percentage points lower than desktop across the analyzed traffic sources.

This indicates that the mobile experience around the transition from product browsing to product-detail engagement should be investigated further.

---

## Project Learning

This step demonstrates the ability to move from a general conversion KPI to a more detailed funnel analysis.

The analysis progressed from:

Overall Conversion
→ Device Performance
→ Traffic Source + Device
→ Funnel Stage
→ Stage-to-Stage Conversion

This provides a more actionable view of where conversion performance differs and allows specific areas of the customer journey to be investigated.

---

## STEP 34 Status

Completed.

- 34.1 Funnel sessions by traffic source and device — Complete
- 34.2 Funnel stage conversion by traffic source and device — Complete
- Business findings — Complete
- Business interpretation — Complete

No additional query is required for STEP 34.

## STEP 35 — Revenue & Order Trends Over Time

**SQL File:** `35_revenue_order_trends.sql`

### Business Question

How have website sessions, order volume, conversion rate, revenue, average order value, and revenue per session changed over time?

### Analysis Performed

Three monthly analyses were performed:

* **35.1 — Monthly Sessions & Orders**
* **35.2 — Monthly Session-to-Order Conversion Rate**
* **35.3 — Monthly Revenue, Average Order Value & Revenue per Session**

The analysis grouped website sessions by month and connected sessions to orders using `website_session_id`.

### Key Findings

The business shows strong long-term growth between March 2012 and March 2015.

Website sessions increased substantially, growing from 1,879 sessions in March 2012 to more than 29,000 sessions per month by December 2014.

Order volume also increased significantly, from 60 orders in March 2012 to more than 2,300 orders in December 2014.

The session-to-order conversion rate improved considerably. It increased from 3.19% in March 2012 to 8.69% in February 2015. This indicates that the business improved not only its ability to attract website traffic, but also its ability to convert that traffic into customers.

Average Order Value (AOV) increased from approximately $49.99 during 2012 to approximately $62–65 during 2014–2015. This indicates that the average customer order became more valuable over time.

Revenue per session also improved substantially, increasing from $1.60 in March 2012 to $5.43 in February 2015. This indicates that each website session generated considerably more economic value as the business developed.

### Business Interpretation

The analysis indicates that Maven Fuzzy Factory experienced improvement across multiple dimensions:

**Traffic growth → More orders → Higher conversion → Higher order value → Higher revenue per session**

This is stronger evidence of business growth than looking at revenue alone because it shows improvements in both traffic volume and website efficiency.

### Data Quality Note

The dataset ends on March 19, 2015. Therefore, March 2015 is a partial month and should not be directly compared with complete months when evaluating monthly traffic or revenue volume.

### Portfolio Relevance

This analysis directly addresses the original Maven Analytics questions regarding:

* Website session and order trends
* Session-to-order conversion rate
* Revenue per order
* Revenue per session

The resulting monthly metrics will also be useful for the Power BI dashboard and Python analysis.

## Step 36 — Product Performance

### Step 36.0 — Product Performance Overview

### Business Question

> Which products generate the most orders, units sold, and revenue?

### Analysis

The analysis compares all four products using unique orders, units sold, and total revenue.

### Results

| Product                    | Orders | Units Sold | Total Revenue |
| -------------------------- | -----: | ---------: | ------------: |
| The Original Mr. Fuzzy     | 24,226 |     23,861 | $1,211,057.74 |
| The Forever Love Bear      |  5,796 |      4,803 |   $347,702.04 |
| The Birthday Sugar Panda   |  4,985 |      3,068 |   $229,260.15 |
| The Hudson River Mini bear |  5,018 |        581 |   $150,489.82 |

### Observations

* **The Original Mr. Fuzzy** is the dominant product, generating 24,226 orders and approximately $1.21M in revenue.
* **The Forever Love Bear** is the second-highest revenue-generating product with approximately $347.7K.
* **The Birthday Sugar Panda** generated approximately $229.3K in revenue from 4,985 orders.
* **The Hudson River Mini bear** generated approximately $150.5K in revenue from 5,018 orders but only 581 units sold.
* The Hudson River Mini bear shows an unusual relationship between orders and units sold that should be investigated further before drawing conclusions.
* Overall, the business appears highly dependent on **The Original Mr. Fuzzy**, which accounts for the majority of product revenue.

### Business Interpretation

The product portfolio is not evenly distributed. The Original Mr. Fuzzy is the clear primary revenue driver, while the remaining three products contribute substantially less revenue.

The difference between order volume and units sold for some products also suggests that product-level purchasing behavior should be examined before making conclusions about product demand.

### SQL Concepts Practiced

* `LEFT JOIN`
* `COUNT(DISTINCT ...)`
* `SUM()`
* `ROUND()`
* `GROUP BY`
* `ORDER BY`
* Column aliases

## Step 36.3 — Product Performance Over Time

**SQL file:** `36_3_product_performance_over_time.sql`

### Business Question

> How did each product perform over time after its launch?

### Analysis

This analysis compares monthly orders and revenue for each product, starting from the month in which the product was launched.

The product launch date is taken from the `products` table, while monthly orders and revenue are calculated from the `order_items` table.

The `strftime('%Y-%m', oi.created_at)` function is used to group order items by year and month. SQLite's `strftime()` function supports formatting date/time values into year-month values such as `YYYY-MM`.

### Results

#### The Original Mr. Fuzzy

* Launch date: **March 19, 2012**
* First recorded month: **March 2012**
* Initial orders: **60**
* Highest monthly orders: **1,584 in December 2014**
* Revenue in December 2014: **$79,184.16**
* Orders declined after December 2014:

  * January 2015: **1,392**
  * February 2015: **1,113**
  * March 2015: **864**

The Original Mr. Fuzzy remained the strongest product throughout the available period.

#### The Forever Love Bear

* Launch date: **January 6, 2013**
* Initial orders: **47**
* Highest monthly orders: **644 in February 2015**
* Revenue in February 2015: **$38,633.56**

The product showed substantial growth after launch and reached its highest monthly order volume near the end of the available period.

#### The Birthday Sugar Panda

* Launch date: **December 12, 2013**
* Initial orders: **139**
* Highest monthly orders: **539 in December 2014**
* Revenue in December 2014: **$24,788.61**

The product grew steadily after launch and reached its strongest monthly performance approximately one year after introduction.

#### The Hudson River Mini bear

* Launch date: **February 5, 2014**
* Initial orders: **202**
* Highest monthly orders: **610 in January 2015**
* Revenue in January 2015: **$18,293.90**

The product experienced strong growth after launch, reaching more than three times its initial monthly order volume.

### Observations

* All four products show growth in monthly order volume after their respective launches.
* The **Original Mr. Fuzzy** remains the dominant product and reaches the highest monthly order volume in the dataset.
* The newer products also demonstrate significant growth after launch.
* The **Forever Love Bear** increased from 47 orders in its launch month to 644 orders in February 2015.
* The **Birthday Sugar Panda** increased from 139 orders in its launch month to 539 orders in December 2014.
* The **Hudson River Mini bear** increased from 202 orders in its launch month to 610 orders in January 2015.
* The Original Mr. Fuzzy reached its highest monthly order volume in December 2014 and then declined during the first months of 2015.
* March 2015 should be interpreted carefully because the dataset ends on **March 19, 2015**, making March a partial month.

### Business Interpretation

The product-level time analysis provides evidence that product launches were followed by meaningful increases in order volume.

The Original Mr. Fuzzy established itself as the company's core product and generated the largest sustained volume over the full period.

The newer products also demonstrated the ability to grow after launch, suggesting that product launches contributed additional demand rather than simply replacing the existing product.

The different growth patterns also show that product performance should be evaluated over time rather than using only total revenue. A product introduced later has had less time to accumulate total sales, so monthly performance provides a fairer way to evaluate its development after launch.

### Key Business Finding

> **The company's product launches were followed by significant growth in monthly order volume, while The Original Mr. Fuzzy remained the primary long-term revenue and order driver.**

### SQL Concepts Practiced

* `INNER JOIN`
* `COUNT(DISTINCT ...)`
* `SUM()`
* `ROUND()`
* `strftime()`
* `GROUP BY`
* `ORDER BY`
* Date-based grouping


