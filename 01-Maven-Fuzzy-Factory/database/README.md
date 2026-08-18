# 🗄️ Database

This folder contains the SQLite database used for the **Maven Fuzzy Factory E-Commerce Data Analytics** project.

The database provides the underlying data used throughout the SQL analysis and makes the analytical workflow reproducible.

---

## 📁 Contents

```text
database/
│
├── maven_fuzzy_factory.db
└── 01_database_setup.sql
```

### `maven_fuzzy_factory.db`

The main SQLite database containing the e-commerce data used for the project.

It allows the SQL analysis to be executed against the project's actual dataset rather than relying only on exported results.

### `01_database_setup.sql`

SQL script documenting the database setup process.

---

## ▶️ How to Use the Database

The database can be opened with **DB Browser for SQLite** or another SQLite-compatible database client.

### 1. Open the database

Open:

```text
database/maven_fuzzy_factory.db
```

in your SQLite-compatible application.

### 2. Inspect the tables

The database contains the tables required for the project's e-commerce analysis, including website activity, orders, products, and refunds.

### 3. Run the SQL analysis

Use the SQL scripts in the project's SQL analysis folders to reproduce the analytical queries and business metrics.

---

## 🔄 Reproducibility

Including the `.db` file allows recruiters, reviewers, and technical interviewers to inspect the underlying data and execute the SQL analysis directly against the project database.

This makes the SQL phase more transparent and reproducible.

---

## ℹ️ Database Design

A separate schema export is not included because the database itself contains the table structure and the repository already includes the database setup SQL script.

The database is intentionally kept simple and focused on supporting the project's analytical workflow.
