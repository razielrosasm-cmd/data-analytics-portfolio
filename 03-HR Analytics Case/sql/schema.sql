-- ============================================================
-- HR Analytics Attrition Case Study
-- SQLite Schema
-- Author: <your name>
-- Purpose: Star-schema-style layout for attrition analysis
-- ============================================================
-- Design notes:
--   * fact_employee holds one row per employee (grain = employee).
--   * attendance_summary holds one row per employee (aggregated attendance).
--   * Dimension tables provide human-readable labels for coded categoricals.
--   * We use FOREIGN KEY constraints for integrity; SQLite requires
--     PRAGMA foreign_keys = ON at connection time to enforce them.
-- ============================================================

PRAGMA foreign_keys = ON;

-- ---------- DIMENSION TABLES ----------

CREATE TABLE dim_education (
    education_code INTEGER PRIMARY KEY,
    education_label TEXT NOT NULL
);

CREATE TABLE dim_environment_satisfaction (
    env_sat_code INTEGER PRIMARY KEY,
    env_sat_label TEXT NOT NULL
);

CREATE TABLE dim_job_involvement (
    job_involvement_code INTEGER PRIMARY KEY,
    job_involvement_label TEXT NOT NULL
);

CREATE TABLE dim_job_level (
    job_level_code INTEGER PRIMARY KEY,
    job_level_label TEXT NOT NULL
);

CREATE TABLE dim_job_satisfaction (
    job_sat_code INTEGER PRIMARY KEY,
    job_sat_label TEXT NOT NULL
);

CREATE TABLE dim_performance_rating (
    perf_rating_code INTEGER PRIMARY KEY,
    perf_rating_label TEXT NOT NULL
);

CREATE TABLE dim_stock_option_level (
    stock_option_code INTEGER PRIMARY KEY,
    stock_option_label TEXT NOT NULL
);

CREATE TABLE dim_work_life_balance (
    wlb_code INTEGER PRIMARY KEY,
    wlb_label TEXT NOT NULL
);

-- ---------- FACT TABLE: EMPLOYEE ----------

CREATE TABLE fact_employee (
    employee_id                 INTEGER PRIMARY KEY,
    age                         INTEGER,
    attrition                   TEXT,
    attrition_flag              INTEGER NOT NULL,
    business_travel             TEXT,
    department                  TEXT,
    distance_from_home          INTEGER,
    education                   INTEGER,
    education_field             TEXT,
    gender                      TEXT,
    job_level                   INTEGER,
    job_role                    TEXT,
    marital_status              TEXT,
    monthly_income              INTEGER,
    num_companies_worked        INTEGER,
    percent_salary_hike         INTEGER,
    stock_option_level          INTEGER,
    total_working_years         INTEGER,
    training_times_last_year    INTEGER,
    years_at_company            INTEGER,
    years_since_last_promotion  INTEGER,
    years_with_curr_manager     INTEGER,
    environment_satisfaction    INTEGER,
    job_satisfaction            INTEGER,
    work_life_balance           INTEGER,
    job_involvement             INTEGER,
    performance_rating          INTEGER,
    tenure_band                 TEXT,

    FOREIGN KEY (education)                REFERENCES dim_education(education_code),
    FOREIGN KEY (environment_satisfaction) REFERENCES dim_environment_satisfaction(env_sat_code),
    FOREIGN KEY (job_involvement)          REFERENCES dim_job_involvement(job_involvement_code),
    FOREIGN KEY (job_level)                REFERENCES dim_job_level(job_level_code),
    FOREIGN KEY (job_satisfaction)         REFERENCES dim_job_satisfaction(job_sat_code),
    FOREIGN KEY (performance_rating)       REFERENCES dim_performance_rating(perf_rating_code),
    FOREIGN KEY (stock_option_level)       REFERENCES dim_stock_option_level(stock_option_code),
    FOREIGN KEY (work_life_balance)        REFERENCES dim_work_life_balance(wlb_code)
);

-- ---------- FACT TABLE: ATTENDANCE SUMMARY ----------

CREATE TABLE attendance_summary (
    employee_id     INTEGER PRIMARY KEY,
    days_worked     INTEGER,
    avg_hours       REAL,
    median_hours    REAL,
    std_hours       REAL,
    min_hours       REAL,
    max_hours       REAL,
    overnight_days  INTEGER,

    FOREIGN KEY (employee_id) REFERENCES fact_employee(employee_id)
);