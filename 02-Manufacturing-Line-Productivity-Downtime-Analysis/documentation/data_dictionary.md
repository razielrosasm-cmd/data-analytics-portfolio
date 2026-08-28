# Data Dictionary

## Manufacturing Line Productivity & Downtime Analysis

This document describes the analytical datasets used in the **Manufacturing Line Productivity & Downtime Analysis** project.

The datasets were prepared from the original manufacturing data and structured for analysis using **SQLite, SQL, Python, and Power BI**.

The final analytical model is designed to analyze production volume, production time, productivity, downtime, products, and downtime factors.

---

## 1. `line_productivity_prepared`

### Purpose

Contains production batch-level information used to analyze production volume, production duration, operator performance, and production efficiency.

Each row represents one production batch.

### Key Fields

| Column | Data Type | Business Meaning |
| ------ | --------- | ---------------- |
| `Date` | Date | Date on which the production batch was recorded |
| `Product` | Text | Product manufactured during the batch |
| `Batch` | Integer | Unique identifier for the production batch |
| `Operator` | Text | Operator responsible for the production batch |
| `Start Time` | Time | Time when production started |
| `End Time` | Time | Time when production ended |
| `Actual Batch Time` | Time/Text | Actual duration required to complete the batch |

### Business Use

This table is the primary source for production volume and production-time analysis.

### Grain

**One row = one production batch.**

---

## 2. `line_downtime_prepared`

### Purpose

Contains recorded downtime events associated with the manufacturing line.

Each row represents one downtime event recorded during production.

### Key Fields

| Column | Data Type | Business Meaning |
| ------ | --------- | ---------------- |
| `Batch` | Integer | Unique identifier for the production batch |
| `Downtime Factor` | Integer | Identifier for the downtime factor category |
| `Downtime Value` | Numeric | Duration of the downtime event in minutes |

### Business Use

This table is the primary source for downtime analysis.

### Grain

**One row = one downtime event.**

---

## 3. `downtime_factors`

### Purpose

Contains the reference information used to classify downtime events.

This table provides the standardized downtime-factor categories used in the analysis.

### Key Fields

| Column | Data Type | Business Meaning |
| ------ | --------- | ---------------- |
| `Factor` | Integer | Unique identifier for the factor |
| `Description` | Text | Explanation of the downtime category |
| `Operator Error` | Text | Indicates if factor is operator-related (Yes/No) |

### Business Use

The table supports consistent classification and interpretation of downtime causes.

Examples of downtime factors identified in the project include:

- Machine Adjustment (Factor 6)
- Machine Failure (Factor 7)
- Inventory Shortage (Factor 4)

### Grain

**One row = one downtime factor.**

---

## 4. `products`

### Purpose

Contains the product reference data used to identify and categorize manufactured products.

### Key Fields

| Column | Data Type | Business Meaning |
| ------ | --------- | ---------------- |
| `Product` | Text | Product identifier |
| `Flavor` | Text | Product flavor description |
| `Size` | Text | Product volume size |
| `Min batch time` | Numeric | Minimum theoretical production time for the product |

### Business Use

This table supports product classification and standard production-time comparisons.

### Grain

**One row = one product.**

---

# Data Model Relationships

The analytical model connects production, downtime, product, and downtime-factor information.

Conceptually:

┌─────────────────────┐
│ products │
│ │
│ Product │
│ Min batch time │
└──────────┬──────────┘
│
│ Product
▼
┌─────────────────────┐ ┌─────────────────────┐
│ │ │ │
│ line_productivity │ │ line_downtime │
│ _prepared │ │ _prepared │
│ │ │ │
│ Date │ │ Batch │
│ Product │ │ Downtime Factor │
│ Batch │ │ Downtime Value │
│ Operator │ │ │
│ Start Time │ │ │
│ End Time │ │ │
│ Actual Batch Time │ │ │
└─────────────────────┘ └──────────┬──────────┘
│
│ Downtime Factor
▼
┌─────────────────────┐
│ downtime_factors │
│ │
│ Factor │
│ Description │
│ Operator Error │
└─────────────────────┘
text


The exact implementation of relationships may vary between the SQLite analysis and the Power BI semantic model. The business meaning of the fields remains consistent across analytical layers.

---

# Dataset Summary

| Table | Primary Purpose | Grain |
| ----- | --------------- | ----- |
| `line_productivity_prepared` | Production and batch performance | One row per batch |
| `line_downtime_prepared` | Downtime analysis | One row per downtime event |
| `products` | Product reference and standards | One row per product |
| `downtime_factors` | Downtime classification | One row per downtime factor |

---

# Key Relationships

| Relationship | Description |
| ------------ | ----------- |
| `line_productivity_prepared.Batch` → `line_downtime_prepared.Batch` | Links production batches to their downtime events |
| `line_productivity_prepared.Product` → `products.Product` | Links production batches to product standards |
| `line_downtime_prepared.Downtime Factor` → `downtime_factors.Factor` | Links downtime events to their factor descriptions |

---

# Data Scope

The source dataset covers production activity recorded between:

**August 29, 2024 and September 3, 2024.**

The prepared analytical data contains:

- **38 production batches**
- **61 downtime records**
- **6 products**
- **12 downtime factors**

These values describe the project dataset used for the analysis and should not be interpreted as representing a larger production population.

---

# Important Note

The prepared datasets are analytical versions of the original data.

Data preparation was performed before loading the datasets into SQLite and Power BI to standardize fields, resolve time-format issues, and make the data suitable for consistent analysis.

The definitions documented here should be considered the reference for the SQL, Python, and Power BI analytical layers.

