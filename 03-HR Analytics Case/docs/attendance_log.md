# Attendance Data Log — HR Analytics Attrition Case Study

**Stage:** 4 — Attendance Data Pipeline  
**Input:** `in_time.csv`, `out_time.csv` (wide, 4,410 × 262)  
**Output:** `attendance_daily.csv`, `attendance_employee_summary.csv`  
**Script:** `python/analysis/04_process_attendance.py`

---

## 1. Why Attendance Is Processed Separately

The attendance files are structurally different from the master HR data. Each is a **wide table** with one row per employee and ~261 date columns. To use this data, we need to reshape it into a **long** format (one row per employee-day), compute daily hours, then aggregate back to employee level. This is a data-engineering task — Python is the right tool, not SQL.

---

## 2. Pipeline Steps

| Step | Action |
|---|---|
| 4.1 | Loaded both wide CSVs (4,410 × 262) |
| 4.1 | Renamed first column `Unnamed: 0` → `employee_id` |
| 4.1 | Melted wide → long (1 row per employee-date) |
| 4.2 | Inner-joined `in_time` and `out_time` on `(employee_id, date)` |
| 4.3 | Computed `hours_worked = out − in` (overnight correction if negative) |
| 4.4 | Flagged anomalies (≤ 0 hours, > 16 hours) |
| 4.5 | Aggregated to employee level (mean, median, std, etc.) |
| 4.6 | Validated against master (4,410 employees present) |
| 4.7 | Exported two CSVs |

---

## 3. Edge Cases Handled

### 3.1 Overnight shifts
If `out_time < in_time`, the shift crossed midnight. Example: in `22:55`, out `01:05` → naive delta is negative, corrected to +24 hours. This was flagged with the `was_overnight` column.

**Overnight records found:** 0

### 3.2 Anomalous durations
Two anomaly flags were applied:

- `anomaly_negative`: `hours_worked <= 0.0`
- `anomaly_too_long`: `hours_worked > 16.0`

Anomalous rows are **kept** in `attendance_daily.csv` (for auditability) but **excluded** from the employee-level summary statistics (mean, median, std).

**Negative-hour rows:** 0  
**Too-long rows:** 0

### 3.3 Missing days
Weekends and holidays are stored as `NaN` in the raw files and were dropped during the long-format reshape (they cannot be meaningful rows). Leave and sick days also appear as `NaN` and were dropped. The resulting `days_worked` count per employee reflects actual attended days.

---

## 4. Output Shapes

- `attendance_daily.csv`: **1,041,930 rows** × 8 columns
- `attendance_employee_summary.csv`: **4,410 rows** × 8 columns

---

## 5. Employee Summary Schema

| Column | Description |
|---|---|
| `employee_id` | 1–4410 |
| `days_worked` | Count of days with valid in+out |
| `avg_hours` | Mean daily hours (anomalies excluded) |
| `median_hours` | Median daily hours |
| `std_hours` | Std-dev of daily hours |
| `min_hours` | Minimum daily hours |
| `max_hours` | Maximum daily hours |
| `overnight_days` | Count of shifts that crossed midnight |

---

## 6. Join Key to Master

`attendance_employee_summary.employee_id` joins 1:1 to `hr_master_clean.employee_id`. All 4,410 IDs are present in both.

---

## 7. Limitations

- Timestamps are recorded but no break/leave information
- No reason codes for missing days
- Overnight shifts are corrected but the *reason* is unknown
- All times assumed in same local timezone

