import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent / "hr_attrition.db"
conn = sqlite3.connect(DB)
conn.execute("PRAGMA foreign_keys = ON;")

def show(title, sql):
    print(f"\n--- {title} ---")
    for row in conn.execute(sql):
        print(row)

# 1. Row counts
show("Row counts", """
    SELECT 'fact_employee', COUNT(*) FROM fact_employee
    UNION ALL
    SELECT 'attendance_summary', COUNT(*) FROM attendance_summary
""")

# 2. Overall attrition
show("Attrition overall", """
    SELECT
        COUNT(*)                              AS total,
        SUM(attrition_flag)                   AS leavers,
        ROUND(100.0 * SUM(attrition_flag) / COUNT(*), 2) AS rate_pct
    FROM fact_employee
""")

# 3. FK integrity — every non-null FK must resolve to a dimension row
show("Orphan education codes", """
    SELECT COUNT(*) FROM fact_employee f
    LEFT JOIN dim_education d ON f.education = d.education_code
    WHERE f.education IS NOT NULL AND d.education_code IS NULL
""")
show("Orphan env_sat codes", """
    SELECT COUNT(*) FROM fact_employee f
    LEFT JOIN dim_environment_satisfaction d
      ON f.environment_satisfaction = d.env_sat_code
    WHERE f.environment_satisfaction IS NOT NULL AND d.env_sat_code IS NULL
""")

# 4. Null counts preserved (must match Stage 2 exactly)
show("Null counts in fact_employee", """
    SELECT
      SUM(work_life_balance       IS NULL) AS wlb_nulls,
      SUM(environment_satisfaction IS NULL) AS env_nulls,
      SUM(job_satisfaction        IS NULL) AS js_nulls,
      SUM(num_companies_worked    IS NULL) AS ncomp_nulls,
      SUM(total_working_years     IS NULL) AS twy_nulls
    FROM fact_employee
""")

# 5. Sanity: every attendance employee_id exists in fact_employee
show("Attendance orphans", """
    SELECT COUNT(*) FROM attendance_summary a
    LEFT JOIN fact_employee f ON a.employee_id = f.employee_id
    WHERE f.employee_id IS NULL
""")

conn.close()