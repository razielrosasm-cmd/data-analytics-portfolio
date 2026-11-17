# Executive Summary — Logistics Operations Database

**Project:** Fleet Maintenance, Driver Attrition, and On-Time Delivery Analysis
**Audience:** Logistics Supervisor / Operations Director
**Prepared by:** Data Analytics Team

---

## The Bottom Line

In three years of fleet data, the clearest path to operational savings runs through the **maintenance shop** — not through hiring, and not through dispatch.

The analysis tested three areas. Two came back completely flat. One revealed a major, addressable cost driver. By implementing the three recommendations on the dashboard, the business can save an estimated **$950,000 to $1.27 million annually**, and prevent an additional **$387,000** from being spent in the wrong direction.

---

## What We Found

### Track A: Driver Attrition (Not Actionable)
We tried to predict which drivers would leave. It is not possible with the current data. Turnover is flat across experience levels, terminals, and hire years. Furthermore, departing drivers have no behavioural records in the system. Predictive modelling cannot add value here without a data audit.

### Track B: On-Time Delivery (Not Actionable)
We tested 28 independent operational segments to find out why trips run late. The late-delivery rate is a uniform **54–57% everywhere**. Long trips are just as likely to be late as short ones. The vendor's claim of 85-95% on-time delivery is not supported by the data. Before launching any improvement programme, the business must audit the on-time flag against actual customer service reports to see if the metric itself is broken.

### Track C: Maintenance (Highly Actionable)
This is where the money is. The maintenance budget is concentrated in **1,628 shop-visit months** that carry the entire **$4.33 million** spend. We built a logistic regression model to find out what makes a month expensive. 

Two factors dominate:
1. **Preventive Shop Visits** (12.5x higher odds of a high-cost month)
2. **Downtime Hours** (Every hour adds 7.6% to the risk)

The counterintuitive finding: **Adding 10% more preventive visits increases cost by $387,000**. Preventive visits are the footprint of cost, not its remedy. 

---

## The Recommendations

To capture the savings, the Logistics Supervisor should focus on what happens *during* a shop visit, not how many visits happen.

### 1. Control the Scope of Shop Visits
Review every work order. Defer discretionary repairs unless the truck is unfit for the road. 
- **Savings: $650,000 – $870,000 per year.**

### 2. Reduce Truck Downtime
Focus on turnaround time. Pre-order parts. Schedule maintenance around peak delivery windows. Target a reduction from the current 16.6 hours average to 12 hours.
- **Savings: $300,000 – $400,000 per year.**

### 3. Do Not Adopt a Blanket "More Visits" Policy
If a truck is running without problems, extending its preventive interval is the better decision. Invest saved capacity into scope discipline instead.
- **Avoided Cost: $387,000 per year.**

---

## Next Steps for the Business

1. **Immediate:** Implement scope reviews at the start of every preventive visit.

2. **Immediate:** Flag any truck-month scoring 8 or higher on the risk model for a cost audit.

3. **Data Audit:** Start capturing behavioural records for drivers (exit interviews) and validate the on-time delivery flag against customer complaints.