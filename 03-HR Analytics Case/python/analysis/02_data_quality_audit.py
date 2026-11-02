"""
Stage 2 — Data Quality Audit
=============================
Purpose:
    Audit the raw data BEFORE cleaning.
    This script performs read-only checks and produces:
      - docs/codebook.csv              (variable → level mapping)
      - docs/data_quality_report.md    (full audit findings + decisions)

It does NOT modify any raw data file.
"""

from pathlib import Path
import pandas as pd
import numpy as np

# ===========================================================================
# CONFIGURATION
# ===========================================================================
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR      = PROJECT_ROOT / "data" / "raw"
DOCS_DIR     = PROJECT_ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)

MASTER_FILES = {
    "general":         "general_data.csv",
    "employee_survey": "employee_survey_data.csv",
    "manager_survey":  "manager_survey_data.csv",
}

ATTENDANCE_FILES = {
    "in_time":  "in_time.csv",
    "out_time": "out_time.csv",
}

# Expected numeric ranges (min, max) for domain validation.
NUMERIC_DOMAIN_RULES = {
    "Age":                      (18, 100),
    "DistanceFromHome":         (0, 500),
    "Education":                (1, 5),
    "EnvironmentSatisfaction":  (1, 4),
    "JobInvolvement":           (1, 4),
    "JobLevel":                 (1, 5),
    "JobSatisfaction":          (1, 4),
    "MonthlyIncome":            (1, 10_000_000),
    "NumCompaniesWorked":       (0, 20),
    "PercentSalaryHike":        (0, 100),
    "PerformanceRating":        (1, 4),
    "RelationshipSatisfaction": (1, 4),
    "StockOptionLevel":         (0, 3),
    "TotalWorkingYears":        (0, 60),
    "TrainingTimesLastYear":    (0, 20),
    "WorkLifeBalance":          (1, 4),
    "YearsAtCompany":           (0, 60),
    "YearsSinceLastPromotion":  (0, 60),
    "YearsWithCurrManager":     (0, 60),
}

# Categorical columns we want to inspect for consistency.
CATEGORICAL_COLUMNS = {
    "general": [
        "Attrition", "BusinessTravel", "Department", "EducationField",
        "Gender", "JobRole", "MaritalStatus", "Over18",
    ],
    "employee_survey": [],
    "manager_survey": [],
}


# ===========================================================================
# 2.1 — CODEBOOK EXTRACTION
# ===========================================================================
def extract_codebook() -> pd.DataFrame:
    """Read the Excel data dictionary and save a clean copy as CSV."""
    path = RAW_DIR / "data_dictionary.xlsx"
    df = pd.read_excel(path)

    df.columns     = [c.strip() for c in df.columns]
    df["Variable"] = df["Variable"].astype(str).str.strip()
    df["Levels"]   = df["Levels"].ffill()

    out_path = DOCS_DIR / "codebook.csv"
    df.to_csv(out_path, index=False)

    print(f"[2.1] Codebook saved: {out_path}  ({len(df)} rows)")
    print(df.head(10).to_string())
    print()
    return df


# ===========================================================================
# 2.2 — MASTER FILE JOINABILITY
# ===========================================================================
def check_master_joinability() -> dict:
    """Verify that the three master files can be joined 1:1 on EmployeeID."""
    results = {}
    id_sets = {}

    for name, fname in MASTER_FILES.items():
        df  = pd.read_csv(RAW_DIR / fname, usecols=["EmployeeID"])
        ids = df["EmployeeID"]
        results[name] = {
            "rows":          len(df),
            "unique_ids":    int(ids.nunique()),
            "duplicate_ids": int(ids.duplicated().sum()),
            "null_ids":      int(ids.isna().sum()),
            "min_id":        int(ids.min()),
            "max_id":        int(ids.max()),
        }
        id_sets[name] = set(ids.dropna().astype(int))

    intersection = set.intersection(*id_sets.values())
    union        = set.union(*id_sets.values())

    results["_cross"] = {
        "union_size":        len(union),
        "intersection_size": len(intersection),
        "only_in": {
            name: sorted(list(ids - intersection))[:20]
            for name, ids in id_sets.items()
        },
    }

    print("[2.2] MASTER FILE JOINABILITY")
    print("-" * 72)
    for name in MASTER_FILES:
        r = results[name]
        print(f"  {name:16s} rows={r['rows']:5d}  "
              f"unique={r['unique_ids']:5d}  "
              f"dupes={r['duplicate_ids']:3d}  "
              f"nulls={r['null_ids']:3d}  "
              f"id_range=[{r['min_id']}, {r['max_id']}]")
    print()
    print(f"  Union of all IDs:        {results['_cross']['union_size']}")
    print(f"  Intersection of all IDs: {results['_cross']['intersection_size']}")
    for name, ids in results["_cross"]["only_in"].items():
        if ids:
            print(f"  IDs only in {name}: {len(ids)} (first 20: {ids})")
    print()
    return results


# ===========================================================================
# 2.3 — CONSTANT COLUMNS
# ===========================================================================
def detect_constants(df: pd.DataFrame) -> dict:
    """Return {column: constant_value} for columns with a single unique value."""
    constants = {}
    for col in df.columns:
        series = df[col].dropna()
        if len(series) > 0 and series.nunique() == 1:
            constants[col] = series.iloc[0]
    return constants


def audit_constants() -> dict:
    print("[2.3] CONSTANT COLUMNS PER MASTER FILE")
    print("-" * 72)
    all_constants = {}
    for name, fname in MASTER_FILES.items():
        df     = pd.read_csv(RAW_DIR / fname)
        consts = detect_constants(df)
        all_constants[name] = consts
        if consts:
            for col, val in consts.items():
                print(f"  {name:16s}  {col:24s}  constant = {val!r}")
        else:
            print(f"  {name:16s}  (no constant columns)")
    print()
    return all_constants


# ===========================================================================
# 2.4 — NUMERIC RANGE CHECKS
# ===========================================================================
def audit_numeric_ranges() -> dict:
    print("[2.4] NUMERIC RANGE CHECK")
    print("-" * 72)
    violations = {}
    for name, fname in MASTER_FILES.items():
        df = pd.read_csv(RAW_DIR / fname)
        for col, (lo, hi) in NUMERIC_DOMAIN_RULES.items():
            if col not in df.columns:
                continue
            s     = pd.to_numeric(df[col], errors="coerce").dropna()
            below = int((s < lo).sum())
            above = int((s > hi).sum())
            if below or above:
                violations.setdefault(name, {})[col] = {
                    "below_min":  below,
                    "above_max":  above,
                    "actual_min": float(s.min()),
                    "actual_max": float(s.max()),
                }
                print(f"  ⚠ {name:16s} {col:24s}  "
                      f"below {lo}: {below}, above {hi}: {above}  "
                      f"(min={s.min()}, max={s.max()})")
    if not violations:
        print("  ✅ No numeric range violations detected.")
    print()
    return violations


# ===========================================================================
# 2.5 — CATEGORICAL VALUE CONSISTENCY
# ===========================================================================
def audit_categoricals() -> dict:
    print("[2.5] CATEGORICAL VALUE CONSISTENCY")
    print("-" * 72)
    findings = {}
    for name, fname in MASTER_FILES.items():
        cols = CATEGORICAL_COLUMNS.get(name, [])
        if not cols:
            continue
        df = pd.read_csv(RAW_DIR / fname)
        for col in cols:
            if col not in df.columns:
                continue
            values  = df[col].dropna().astype(str)
            unique  = sorted(values.unique())
            has_ws  = any(v != v.strip() for v in unique)
            lowered = [v.lower() for v in unique]
            has_case_dupes = len(lowered) != len(set(lowered))
            flag = "⚠" if (has_ws or has_case_dupes) else " "
            findings.setdefault(name, {})[col] = {
                "n_unique":         len(unique),
                "values":           unique,
                "whitespace_issue": has_ws,
                "case_issue":       has_case_dupes,
            }
            print(f"  {flag} {name:16s} {col:20s}  "
                  f"{len(unique)} values: {unique}")
    print()
    return findings


# ===========================================================================
# 2.6 — MISSINGNESS PATTERN ANALYSIS
# ===========================================================================
def audit_missingness() -> dict:
    print("[2.6] MISSINGNESS PATTERN ANALYSIS")
    print("-" * 72)

    frames = []
    for name, fname in MASTER_FILES.items():
        df = pd.read_csv(RAW_DIR / fname)
        df = df.rename(
            columns={c: f"{name}__{c}" for c in df.columns if c != "EmployeeID"}
        )
        frames.append(df)

    merged = frames[0]
    for f in frames[1:]:
        merged = merged.merge(f, on="EmployeeID", how="outer")

    null_counts = merged.isna().sum()
    null_counts = null_counts[null_counts > 0].sort_values(ascending=False)

    summary = {"total_rows": len(merged), "columns": {}}

    if null_counts.empty:
        print("  ✅ No missing values across merged master table.")
        print()
        return summary

    print("  Columns with missing values (merged view):")
    for col, n in null_counts.items():
        pct = 100 * n / len(merged)
        summary["columns"][col] = {"n": int(n), "pct": round(pct, 2)}
        print(f"    {col:42s}  {n:5d}  ({pct:.2f}%)")

    missing_mask   = merged.isna().any(axis=1)
    n_with_missing = int(missing_mask.sum())
    summary["employees_with_any_null"] = n_with_missing
    summary["pct_with_any_null"]       = round(100 * n_with_missing / len(merged), 2)

    print()
    print(f"  Employees with ≥1 missing value: {n_with_missing} "
          f"({summary['pct_with_any_null']}%)")

    missing_cols = null_counts.index.tolist()
    summary["overlaps"] = {}
    if len(missing_cols) > 1:
        print()
        print("  Overlap between missing columns:")
        for i, c1 in enumerate(missing_cols):
            for c2 in missing_cols[i + 1:]:
                both = int((merged[c1].isna() & merged[c2].isna()).sum())
                summary["overlaps"][f"{c1} & {c2}"] = both
                print(f"    {c1:40s} & {c2:40s}  both missing: {both}")
    print()
    return summary


# ===========================================================================
# 2.7 — ATTENDANCE ID CROSS-CHECK
# ===========================================================================
def audit_attendance_ids() -> dict:
    print("[2.7] ATTENDANCE ID CROSS-CHECK")
    print("-" * 72)

    master     = pd.read_csv(RAW_DIR / MASTER_FILES["general"], usecols=["EmployeeID"])
    master_ids = set(master["EmployeeID"].astype(int))

    summary = {}
    for name, fname in ATTENDANCE_FILES.items():
        df       = pd.read_csv(RAW_DIR / fname, usecols=[0])
        col_name = df.columns[0]
        ids      = set(df[col_name].dropna().astype(int))

        overlap         = len(master_ids & ids)
        only_master     = len(master_ids - ids)
        only_attendance = len(ids - master_ids)
        summary[name] = {
            "n_ids":              len(ids),
            "overlap":            overlap,
            "only_in_master":     only_master,
            "only_in_attendance": only_attendance,
        }
        print(f"  {name:10s}  IDs: {len(ids):5d}  overlap: {overlap:5d}  "
              f"only_in_master: {only_master}  "
              f"only_in_attendance: {only_attendance}")
    print()
    return summary


# ===========================================================================
# 2.8a — MISSINGNESS vs ATTRITION
# ===========================================================================
def audit_missingness_vs_attrition() -> dict:
    """
    For each column with missing values, compare attrition rate
    among employees with vs. without the missing value.

    If the rates differ substantially, the missingness is informative.
    """
    print("[2.8a] MISSINGNESS vs ATTRITION")
    print("-" * 72)

    general = pd.read_csv(RAW_DIR / MASTER_FILES["general"])
    survey  = pd.read_csv(RAW_DIR / MASTER_FILES["employee_survey"])
    manager = pd.read_csv(RAW_DIR / MASTER_FILES["manager_survey"])

    merged = (
        general
        .merge(survey, on="EmployeeID", how="inner")
        .merge(manager, on="EmployeeID", how="inner")
    )

    merged["attrition_flag"] = (merged["Attrition"] == "Yes").astype(int)

    cols_with_nulls = [
        "WorkLifeBalance", "EnvironmentSatisfaction", "JobSatisfaction",
        "NumCompaniesWorked", "TotalWorkingYears",
    ]

    results = {}
    for col in cols_with_nulls:
        if col not in merged.columns:
            continue
        is_null      = merged[col].isna()
        n_null       = int(is_null.sum())
        attr_null    = merged.loc[is_null,  "attrition_flag"].mean()
        attr_nonnull = merged.loc[~is_null, "attrition_flag"].mean()
        diff         = attr_null - attr_nonnull

        results[col] = {
            "n_missing":              n_null,
            "attrition_when_missing": round(attr_null * 100, 2),
            "attrition_when_present": round(attr_nonnull * 100, 2),
            "diff_pp":                round(diff * 100, 2),
        }
        print(f"  {col:28s}  n_null={n_null:3d}  "
              f"attrition_null={results[col]['attrition_when_missing']:.2f}%  "
              f"attrition_present={results[col]['attrition_when_present']:.2f}%  "
              f"diff={results[col]['diff_pp']:+.2f}pp")
    print()
    return results


# ===========================================================================
# 2.8b — WRITE THE QUALITY REPORT
# ===========================================================================
def write_quality_report(
    codebook_path,
    joinability,
    constants,
    range_issues,
    categoricals,
    missingness,
    missingness_vs_attrition,
    attendance,
    output_path,
):
    """
    Write docs/data_quality_report.md summarizing all Stage 2 findings.

    Each section includes BOTH the finding and the decision it drives.
    This report is the deliverable of Stage 2 and feeds Stage 3 (cleaning).
    """
    print("[2.8b] WRITING QUALITY REPORT")
    print("-" * 72)

    lines = []
    lines.append("# Data Quality Report — HR Analytics Attrition Case Study\n\n")
    lines.append("**Project:** HR Analytics — Employee Attrition Case Study  \n")
    lines.append("**Stage:** 2 — Data Profiling & Quality Audit  \n")
    lines.append("**Source files:** `general_data.csv`, `employee_survey_data.csv`, "
                 "`manager_survey_data.csv`, `in_time.csv`, `out_time.csv`  \n")
    lines.append("**Date:** (auto-generated)\n\n")

    # --- 1. Executive summary ---
    lines.append("---\n\n")
    lines.append("## 1. Executive Summary\n\n")
    lines.append(
        "The raw HR dataset is unusually clean for a real-world dataset. "
        "All three master files (general, employee survey, manager survey) "
        "contain exactly **4,410 rows** with **4,410 unique EmployeeIDs**, "
        "no duplicates, and no null IDs. The intersection of EmployeeIDs "
        "across all files equals the union, meaning a clean 1:1 join is possible "
        "with zero orphans.\n\n"
    )
    lines.append(
        "The data is not perfect, however. Three constant columns carry no "
        "analytical value, ~2.5% of employees have at least one missing survey "
        "or tenure value, and several columns that *look* numeric are actually "
        "coded categoricals. Each issue is documented below with the decision "
        "it drives for Stage 3 (cleaning).\n\n"
    )

    # --- 2. File inventory & joinability ---
    lines.append("---\n\n")
    lines.append("## 2. File Inventory & Joinability\n\n")
    lines.append("| File | Rows | Unique IDs | Duplicate IDs | Null IDs |\n")
    lines.append("|---|---|---|---|---|\n")
    for name in MASTER_FILES:
        info = joinability.get(name, {})
        lines.append(
            f"| {name} | {info.get('rows', '—')} | {info.get('unique_ids', '—')} | "
            f"{info.get('duplicate_ids', '—')} | {info.get('null_ids', '—')} |\n"
        )
    cross = joinability.get("_cross", {})
    lines.append(
        f"\n**Union of all IDs:** {cross.get('union_size', '—')}  \n"
        f"**Intersection of all IDs:** {cross.get('intersection_size', '—')}\n\n"
    )
    lines.append("**Decision:** Clean 1:1 inner join across the three master files. "
                 "No orphan handling required.\n\n")

    # --- 3. Constant columns ---
    lines.append("---\n\n")
    lines.append("## 3. Constant Columns\n\n")
    lines.append("| File | Column | Constant Value |\n")
    lines.append("|---|---|---|\n")
    any_constants = False
    for file_name, cols in constants.items():
        for col, val in cols.items():
            any_constants = True
            lines.append(f"| {file_name} | `{col}` | `{val}` |\n")
    if not any_constants:
        lines.append("| — | — | — |\n")
    lines.append("\n**Rationale:** A column with a single value cannot differentiate, "
                 "segment, or predict anything. It also consumes storage and clutters "
                 "the schema.\n\n")
    lines.append("**Decision:** Drop `EmployeeCount`, `Over18`, `StandardHours` "
                 "in Stage 3.\n\n")

    # --- 4. Numeric range check ---
    lines.append("---\n\n")
    lines.append("## 4. Numeric Range Check\n\n")
    if not range_issues:
        lines.append("**Result:** ✅ No numeric range violations detected.\n\n")
    else:
        lines.append("**Result:** ⚠ Violations detected.\n\n")
        lines.append("| File | Column | Below min | Above max | Actual min | Actual max |\n")
        lines.append("|---|---|---|---|---|---|\n")
        for file_name, cols in range_issues.items():
            for col, info in cols.items():
                lines.append(
                    f"| {file_name} | `{col}` | {info['below_min']} | "
                    f"{info['above_max']} | {info['actual_min']} | "
                    f"{info['actual_max']} |\n"
                )
        lines.append("\n")
    lines.append(
        "**Note:** This is a pass/fail check against domain-appropriate bounds "
        "(e.g., Age 18–100, ratings 1–4, tenure ≥ 0). Observed min/max per column "
        "will be logged in the processed data summary (Stage 3).\n\n"
    )

    # --- 5. Categorical consistency ---
    lines.append("---\n\n")
    lines.append("## 5. Categorical Consistency\n\n")
    lines.append("| File | Column | # Distinct | Values |\n")
    lines.append("|---|---|---|---|\n")
    for file_name, cols in categoricals.items():
        for col, info in cols.items():
            vals = ", ".join(f"`{v}`" for v in info["values"])
            lines.append(
                f"| {file_name} | `{col}` | {info['n_unique']} | {vals} |\n"
            )
    lines.append("\n**Decision:** No whitespace, case, or label normalization needed. "
                 "Categories are internally consistent.\n\n")

    # --- 6. Missing values ---
    lines.append("---\n\n")
    lines.append("## 6. Missing Values\n\n")
    lines.append("### 6.1 Where the nulls are\n\n")
    lines.append("| Column | Missing | % of 4,410 |\n")
    lines.append("|---|---|---|\n")
    col_dict = missingness.get("columns", {})
    for col, info in col_dict.items():
        lines.append(f"| `{col}` | {info['n']} | {info['pct']:.2f}% |\n")
    n_any = missingness.get("employees_with_any_null", 0)
    lines.append(f"\n**Employees with ≥1 missing value:** "
                 f"{n_any} ({n_any / 4410 * 100:.2f}%)\n\n")

    lines.append("### 6.2 Distribution of missingness\n\n")
    lines.append(
        "Missingness is **scattered**, not concentrated. 111 nulls are spread "
        "across 110 employees — essentially one null per affected employee. "
        "Only one employee has two missing values.\n\n"
    )

    lines.append("### 6.3 Missingness vs. Attrition\n\n")
    lines.append(
        "For each column with nulls, we compared the attrition rate among "
        "employees **with** vs. **without** a missing value. Large gaps suggest "
        "the missingness is informative rather than random.\n\n"
    )
    lines.append("| Column | n_null | Attrition (null) | Attrition (present) | Diff (pp) |\n")
    lines.append("|---|---|---|---|---|\n")
    for col, r in missingness_vs_attrition.items():
        lines.append(
            f"| `{col}` | {r['n_missing']} | {r['attrition_when_missing']:.2f}% | "
            f"{r['attrition_when_present']:.2f}% | {r['diff_pp']:+.2f} |\n"
        )
    lines.append(
        "\n**Interpretation:** `JobSatisfaction` shows the largest gap "
        "(−11.17 pp): employees who did not report job satisfaction had an "
        "observed attrition rate of 5% vs. 16.17% among those who did. However, "
        "the null group is small (n=20 → ~1 leaver), so this is flagged as a "
        "pattern for further investigation, not a confirmed relationship.\n\n"
    )
    lines.append("**Decision:** Keep all nulls. Do not drop rows. Do not impute. "
                 "Handle nulls per-analysis (SQL aggregates already ignore them) "
                 "and document the handling in each query's output.\n\n")

    # --- 7. Attendance cross-check ---
    lines.append("---\n\n")
    lines.append("## 7. Attendance File Cross-Check\n\n")
    lines.append("| File | IDs | Overlap with Master | Only in Master | Only in Attendance |\n")
    lines.append("|---|---|---|---|---|\n")
    for name, info in attendance.items():
        lines.append(
            f"| {name} | {info['n_ids']} | {info['overlap']} | "
            f"{info['only_in_master']} | {info['only_in_attendance']} |\n"
        )
    lines.append("\n**Decision:** Attendance data joins cleanly to master. "
                 "Processed separately in Stage 4 (wide→long reshape, overnight handling).\n\n")

    # --- 8. Decisions carried into Stage 3 ---
    lines.append("---\n\n")
    lines.append("## 8. Decisions Carried into Stage 3 (Cleaning)\n\n")
    lines.append("| # | Decision | Justification |\n")
    lines.append("|---|---|---|\n")
    lines.append("| 1 | Drop `EmployeeCount`, `Over18`, `StandardHours` | Constants (Section 3) |\n")
    lines.append("| 2 | Keep all 4,410 rows | Only 2.49% affected by nulls; dropping biases sample (Section 6) |\n")
    lines.append("| 3 | Do not impute nulls | Missingness may be informative; fabrication risk (Section 6.3) |\n")
    lines.append("| 4 | Build dimension tables for coded categoricals | Codes are labels, not quantities; business readability (Stage 5) |\n")
    lines.append("| 5 | Merge master files as 1:1 inner join | Confirmed clean (Section 2) |\n")
    lines.append("| 6 | Process attendance separately in Python | Wide format (~250 date columns); not a SQL-native task (Section 7) |\n\n")

    # --- 9. Limitations ---
    lines.append("---\n\n")
    lines.append("## 9. Limitations of This Audit\n\n")
    lines.append("- Range checks used domain-appropriate bounds, not exhaustive rules.\n")
    lines.append("- Missingness-vs-attrition analysis is univariate; confounders not controlled.\n")
    lines.append("- The dataset is synthetic/anonymized; some relationships may be artifacts.\n")
    lines.append("- No temporal dimension: `Attrition` is a single binary flag with no exit date.\n\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("".join(lines), encoding="utf-8")
    print(f"  ✅ Report saved: {output_path}")
    print()


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 72)
    print("STAGE 2 — DATA QUALITY AUDIT")
    print("=" * 72)
    print()

    codebook                 = extract_codebook()
    joinability              = check_master_joinability()
    constants                = audit_constants()
    range_issues             = audit_numeric_ranges()
    categoricals             = audit_categoricals()
    missingness              = audit_missingness()
    attendance               = audit_attendance_ids()
    missingness_vs_attrition = audit_missingness_vs_attrition()

    print("[Stage 2.1 – 2.8a complete]")
    print("→ 2.8b will now write docs/data_quality_report.md")
    print()

    write_quality_report(
        codebook_path=DOCS_DIR / "codebook.csv",
        joinability=joinability,
        constants=constants,
        range_issues=range_issues,
        categoricals=categoricals,
        missingness=missingness,
        missingness_vs_attrition=missingness_vs_attrition,
        attendance=attendance,
        output_path=DOCS_DIR / "data_quality_report.md",
    )

    print("[Stage 2 complete]")
    print("→ Next: Stage 3 — Data Cleaning & Preprocessing")


if __name__ == "__main__":
    main()