# Logistics Operations Database — Fleet Maintenance, Driver Attrition, and On-Time Delivery

A three-page Power BI dashboard and full analytical pipeline built on three years of fleet operations data. The project answers one question for a Logistics Supervisor: **where does the fleet actually lose money, and what should we do about it?**

The short answer: **maintenance**. Two other tracks — driver turnover and on-time delivery — came back flat across every test. The dashboard says so honestly, and turns the one real signal into **$950K–$1.27M in annual savings recommendations**.

---

## The Headline Finding

Of three analytical tracks, **one is actionable**:

| Track | Question | Result | Status |
|---|---|---|---|
| **A — Driver Attrition** | Can we predict which drivers will leave? | Flat across experience, terminal, hire year. All 26 leavers have no behavioural records. | ❌ Not actionable |
| **B — On-Time Delivery** | Which segments run late? | Late rate is **54–57% in all 28 independent tests**. No segment stands out. | ❌ Not actionable |
| **C — Maintenance** | What drives high-cost months? | Two factors dominate: **preventive shop visits (12.5x higher odds)** and **downtime hours (7.6% higher odds per hour)**. | ✅ Actionable |

The counterintuitive finding: **adding 10% more preventive visits would increase cost by $387K per year**, not reduce it. Preventive visits are the footprint of cost, not its remedy. The lever is **scope discipline at each visit**, not more visits.

---

## The Three Recommendations (Page 3 of the Dashboard)

| # | Recommendation | Estimated Annual Impact |
|---|---|---|
| **1** | Control the scope of shop visits — review every work order, defer discretionary repairs | **$650K – $870K saved** |
| **2** | Reduce truck downtime — target 16.6h → 12h average turnaround | **$300K – $400K saved** |
| **3** | Do not simply add more preventive visits — they increase cost | **$387K avoided** |

**Total: $950K – $1.27M in savings, plus $387K protected from being spent in the wrong direction.**

---

## The Dashboard

A three-page Power BI report tells the story in sequence:

| Page | Purpose | File |
|---|---|---|
| **1 — Overview** | What is happening: headline numbers, flat patterns, discovery | `powerbi/screenshots/Overview.png` |
| **2 — Segments** | Where the signal lives: Track C vivid vs Tracks A/B flat | `powerbi/screenshots/Segments.png` |
| **3 — Action Plan** | What to do: three quantified recommendations | `powerbi/screenshots/Action Plan.png` |

Open the dashboard: **`powerbi/Logistics Operations.pbix`**

Full page-by-page documentation: [`powerbi/README.md`](powerbi/README.md)

---

## Project Structure

- **`data/`**
  - **`raw/`** — 16 original source CSVs (unmodified)
  - **`processed/`** — 3 cleaned master files ready for analysis

- **`docs/`** — codebook, data inventory, logs, model notes

- **`powerbi/`** — the dashboard (.pbix), screenshots, README

- **`python/`** — 4 analysis scripts + 4 output reports
  - **`analysis/`**
  - **`outputs/`**

- **`sql/`** — database, loader, 28 analysis queries
  - **`analysis/`** — queries organised by track (A, B, C)
  - **`results/`** — CSV output of each query
  - **`db/`** — the SQLite database

---

## How the Analysis Was Built

The project ran in five stages:

1. **Data inspection** — 16 raw CSVs loaded, profiled, and validated against a schema

2. **Data cleaning** — built three clean master files (driver, trip, truck-month) with documented transformations

3. **SQL analysis** — 28 independent queries across three tracks, every result saved to CSV

4. **Statistical modelling** — logistic regression on Track C, with what-if simulation

5. **Dashboard** — three-page Power BI report translating findings into decisions

Each stage has its own README with detail:

- **Python pipeline:** [`python/README.md`](python/README.md)

- **SQL analysis:** [`sql/README.md`](sql/README.md)

- **Dashboard build:** [`powerbi/README.md`](powerbi/README.md)

---

## The Data

Three years of fleet operations data across **16 source tables**:

| Domain | Tables |
|---|---|
| **Drivers** | `drivers`, `driver_monthly_metrics` |
| **Trips** | `trips`, `loads`, `delivery_events`, `routes` |
| **Vehicles** | `trucks`, `trailers`, `truck_utilization_metrics` |
| **Maintenance** | `maintenance_records` |
| **Operations** | `facilities`, `fuel_purchases`, `safety_incidents`, `customers` |

After cleaning, these reduce to three analytical masters:

- `master_driver_clean.csv` — one row per driver

- `master_trip_clean.csv` — one row per trip

- `master_truck_month_clean.csv` — one row per truck per month (**3,312 rows** — the core of the maintenance analysis)

Data dictionary and field definitions: [`docs/codebook.csv`](docs/codebook.csv)

Data inventory and source notes: [`docs/data_inventory.md`](docs/data_inventory.md)

---

## Key Numbers at a Glance

| Metric | Value |
|---|---|
| Total fleet spend analysed | **$4.33 million** over 3 years |
| Shop-visit months carrying that spend | **1,628** |
| Truck-months in the maintenance model | **3,312** |
| Late-delivery rate (flat across all segments) | **54–57%** |
| Driver leavers in dataset | **26** (none with behavioural records) |
| Model accuracy at top risk decile | **83% high-cost rate** |

---

## Reproducing the Analysis

To rebuild from raw data:

1. **Clean the data:**
   `cd python/analysis`
   `python 02_clean_data.py`

2. **Load to SQL:**
   `cd sql`
   `python load_data.py`

3. **Validate:**
   `cd python/analysis`
   `python 06_validate_sql.py`

4. **Run the Track C model:**
   `cd python/analysis`
   `python 07_track_c_model.py`

5. **Open the dashboard:**
   Launch Power BI Desktop
   Open `powerbi/Logistics Operations.pbix`
   Refresh data connections if source paths have changed

---

## For the Business Reader

If you only have five minutes, read these three files:

1. **`docs/executive_summary.md`** — the one-page findings summary

2. **`powerbi/screenshots/Overview.png`** — the headline numbers

3. **`powerbi/screenshots/Action Plan.png`** — the three recommendations

The dashboard's conclusion is simple: **in three years of fleet data, the clearest path to operational savings runs through the maintenance shop — not through hiring, and not through dispatch.**

---

## For the Technical Reader

If you want to see the working:

- **28 SQL queries** in `sql/analysis/`, organised by track, with results in `sql/results/`

- **Logistic regression** with odds ratios, calibration, and what-if simulation in `python/outputs/07_model_report.txt`

- **Full build narrative** in the Page 2 and Page 3 handoff documentation in `docs/`

The modelling approach, variable selection, and validation are documented in [`docs/model_log.md`](docs/model_log.md).

---

## Data Honesty Note

Two of the three tracks came back flat. Rather than hiding this, the dashboard **leads with it**. The flat results are themselves a finding: the data does not contain the operational variation those analyses need. This is documented openly in `docs/executive_summary.md` and on Page 2 of the dashboard.

Before investing in predictive programmes for attrition or on-time delivery, the recommendation is to **commission data audits** — capture behavioural records for departing drivers, and validate the on-time flag against actual customer service reports.

---

## Project Status

| Component | Status |
|---|---|
| Data pipeline | ✅ Complete |
| SQL analysis (28 queries) | ✅ Complete |
| Python scripts (4 stages) | ✅ Complete |
| Statistical model (Track C) | ✅ Complete |
| Power BI dashboard (3 pages) | ✅ Complete |
| Documentation | ✅ Complete |

**Version:** 1.0
**Last updated:** November 2026