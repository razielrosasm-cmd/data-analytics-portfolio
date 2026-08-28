# Executive Summary

## Manufacturing Line Productivity & Downtime Analysis

### Overview

This analysis evaluated production volume, batch-time performance, production efficiency, product performance, operator variation, and downtime across the manufacturing line.

The dataset contains **38 production batches** and **61 recorded downtime events** across **6 products** and **12 downtime factors**, covering the period from **August 29 to September 3, 2024**.

---

### Key Findings

#### 1. Production Time Is Significantly Above Standard

The average actual batch time was **101.53 minutes**, compared with an average standard time of **65.00 minutes**.

This represents an average time variance of **36.53 minutes**, or **56.17% above the standard production time**.

#### 2. Downtime Is Concentrated in Three Main Factors

The largest recorded downtime contributors were:

- **Machine Adjustment** – 332 minutes
- **Machine Failure** – 254 minutes
- **Inventory Shortage** – 225 minutes

These three factors account for over 58% of all recorded downtime.

#### 3. CO-600 Has the Highest Product-Level Downtime

- **CO-600** – 494 minutes
- **CO-2L** – 277 minutes
- **RB-600** – 258 minutes

Downtime is not evenly distributed across the product portfolio.

---

### Conclusion

The primary opportunity identified is to **reduce production-time losses by addressing the main sources of downtime and the gap between actual and standard batch time**.

The recommended priority order for investigation is:

1. **Machine Adjustment** – largest single downtime factor
2. **Machine Failure** – second-largest downtime factor
3. **Inventory Shortage** – third-largest downtime factor
4. **CO-600** – highest product-level downtime
5. **Production-Time Variance** – 56% above standard

### Next Step

The Power BI dashboard provides the operational detail required to investigate these areas by product, operator, downtime factor, and individual batch.