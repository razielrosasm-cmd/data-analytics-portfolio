"""
Stage 3 — Data Cleaning & Preprocessing
=======================================
Purpose:
    Produce a single analysis-ready master table from the three raw
    master files (general, employee_survey, manager_survey).

Inputs:
    data/raw/general_data.csv
    data/raw/employee_survey_data.csv
    data/raw/manager_survey_data.csv

Outputs:
    data/processed/hr_master_clean.csv      ← cleaned, merged dataset
    docs/cleaning_log.md                     ← transformation log

Design principles:
    - Preserve every row (4,410). No dropping. No imputation.
    - Drop only constant columns (zero analytical value).
    - Standardize names to snake_case for SQL/Python/Power BI portability.
    - Derive attrition_flag (0/1) alongside the original Attrition string.
    - Derive tenure_band for HR-standard tenure segmentation.
    - Validate every decision against Stage 2 audit numbers.
"""

from pathlib import Path
import re
import pandas as pd
import numpy as np


# ===========================================================================
# CONFIGURATION
# ===========================================================================
PROJECT_ROOT  = Path(__file__).resolve().parents[2]
RAW_DIR       = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DOCS_DIR      = PROJECT_ROOT / "docs"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

MASTER_FILES = {
    "general":         "general_data.csv",
    "employee_survey": "employee_survey_data.csv",
    "manager_survey":  "manager_survey_data.csv",
}

# Columns to drop (constants from Stage 2 audit)
CONSTANT_COLUMNS = ["EmployeeCount", "Over18", "StandardHours"]

# Expected values from Stage 2 (used as guardrails)
EXPECTED_ROWS = 4410
EXPECTED_NULLS_SNAKE = {
    "work_life_balance":        38,
    "environment_satisfaction": 25,
    "job_satisfaction":         20,
    "num_companies_worked":     19,
    "total_working_years":       9,
}


# ===========================================================================
# HELPERS
# ===========================================================================
def to_snake_case(name: str) -> str:
    """Convert CamelCase or mixedCase to snake_case."""
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.lower()


# ===========================================================================
# 3.1 — LOAD RAW FILES
# ===========================================================================
def load_raw() -> dict:
    print("[3.1] LOADING RAW FILES")
    print("-" * 72)
    frames = {}
    for name, fname in MASTER_FILES.items():
        path = RAW_DIR / fname
        df = pd.read_csv(path)
        frames[name] = df
        print(f"  {name:16s}  rows={len(df):5d}  cols={df.shape[1]:3d}  "
              f"file={fname}")
    print()
    return frames


# ===========================================================================
# 3.2 — DROP CONSTANT COLUMNS
# ===========================================================================
def drop_constants(frames: dict) -> dict:
    print("[3.2] DROPPING CONSTANT COLUMNS")
    print("-" * 72)
    general  = frames["general"].copy()
    existing = [c for c in CONSTANT_COLUMNS if c in general.columns]
    missing  = [c for c in CONSTANT_COLUMNS if c not in general.columns]

    if missing:
        print(f"  ⚠ Columns not found (skipping): {missing}")

    general.drop(columns=existing, inplace=True)
    frames["general"] = general

    print(f"  Dropped from 'general': {existing}")
    print(f"  Remaining columns in 'general': {general.shape[1]}")
    print()
    return frames


# ===========================================================================
# 3.3 — MERGE MASTER FILES (1:1 INNER JOIN ON EmployeeID)
# ===========================================================================
def merge_masters(frames: dict) -> pd.DataFrame:
    print("[3.3] MERGING MASTER FILES (1:1 INNER JOIN)")
    print("-" * 72)

    general = frames["general"]
    survey  = frames["employee_survey"]
    manager = frames["manager_survey"]

    merged = (
        general
        .merge(survey,  on="EmployeeID", how="inner")
        .merge(manager, on="EmployeeID", how="inner")
    )

    print(f"  general rows:         {len(general)}")
    print(f"  employee_survey rows: {len(survey)}")
    print(f"  manager_survey rows:  {len(manager)}")
    print(f"  merged rows:          {len(merged)}")
    print(f"  merged columns:       {merged.shape[1]}")
    print()
    return merged


# ===========================================================================
# 3.4 — STANDARDIZE COLUMN NAMES
# ===========================================================================
def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    print("[3.4] STANDARDIZING COLUMN NAMES")
    print("-" * 72)
    mapping = {c: to_snake_case(c) for c in df.columns}
    df = df.rename(columns=mapping)

    changed = {k: v for k, v in mapping.items() if k != v}
    print(f"  Renamed {len(changed)} columns to snake_case")
    for old, new in list(changed.items())[:10]:
        print(f"    {old:28s} → {new}")
    if len(changed) > 10:
        print(f"    ... and {len(changed) - 10} more")
    print()
    return df


# ===========================================================================
# 3.5 — DERIVE ATTRITION FLAG
# ===========================================================================
def derive_attrition_flag(df: pd.DataFrame) -> pd.DataFrame:
    print("[3.5] DERIVING ATTRITION FLAG")
    print("-" * 72)

    df["attrition_flag"] = (df["attrition"] == "Yes").astype(int)

    n_yes = int(df["attrition_flag"].sum())
    n_no  = int((df["attrition_flag"] == 0).sum())
    rate  = n_yes / len(df) * 100

    print(f"  Yes: {n_yes} ({rate:.2f}%)")
    print(f"  No:  {n_no} ({100 - rate:.2f}%)")
    print(f"  Total: {len(df)}")
    print()
    return df


# ===========================================================================
# 3.6 — DERIVE TENURE BAND
# ===========================================================================
def derive_tenure_band(df: pd.DataFrame) -> pd.DataFrame:
    print("[3.6] DERIVING TENURE BAND")
    print("-" * 72)

    bins   = [-1, 1, 3, 5, 10, 100]
    labels = ["0-1 years", "2-3 years", "4-5 years", "6-10 years", "10+ years"]

    df["tenure_band"] = pd.cut(
        df["years_at_company"],
        bins=bins,
        labels=labels,
        right=True,
    )

    counts = df["tenure_band"].value_counts().sort_index()
    print("  Distribution of tenure_band:")
    for band, n in counts.items():
        print(f"    {band:12s}  {n:5d}  ({n / len(df) * 100:5.2f}%)")
    n_na = df["tenure_band"].isna().sum()
    if n_na:
        print(f"    ⚠ {n_na} rows could not be banded")
    print()
    return df


# ===========================================================================
# 3.7 — VALIDATE CLEANED DATA
# ===========================================================================
def validate(df: pd.DataFrame) -> None:
    print("[3.7] VALIDATING CLEANED DATA")
    print("-" * 72)

    errors = []

    # Row count
    if len(df) != EXPECTED_ROWS:
        errors.append(f"Row count {len(df)} != expected {EXPECTED_ROWS}")
    else:
        print(f"  ✅ Row count: {len(df)}")

    # No duplicate EmployeeIDs
    dupes = int(df["employee_id"].duplicated().sum())
    if dupes:
        errors.append(f"{dupes} duplicate employee_ids")
    else:
        print(f"  ✅ No duplicate employee_ids")

    # No nulls in employee_id
    null_ids = int(df["employee_id"].isna().sum())
    if null_ids:
        errors.append(f"{null_ids} null employee_ids")
    else:
        print(f"  ✅ No null employee_ids")

    # Null counts match Stage 2 — snake_case column names
    for col, expected in EXPECTED_NULLS_SNAKE.items():
        if col not in df.columns:
            errors.append(f"column {col} not found in cleaned data")
            continue
        actual = int(df[col].isna().sum())
        if actual != expected:
            errors.append(f"{col}: {actual} nulls != expected {expected}")
        else:
            print(f"  ✅ {col:28s}  nulls = {actual}")

    # Constant columns are gone
    constant_remnants = [c for c in ["employee_count", "over18", "standard_hours"]
                         if c in df.columns]
    if constant_remnants:
        errors.append(f"constant columns still present: {constant_remnants}")
    else:
        print(f"  ✅ Constant columns removed")

    # attrition_flag consistency
    mismatches = int(
        ((df["attrition"] == "Yes") & (df["attrition_flag"] != 1)).sum()
        + ((df["attrition"] == "No") & (df["attrition_flag"] != 0)).sum()
    )
    if mismatches:
        errors.append(f"{mismatches} attrition_flag mismatches")
    else:
        print(f"  ✅ attrition_flag consistent with attrition")

    # tenure_band coverage
    n_na_band = int(df["tenure_band"].isna().sum())
    if n_na_band:
        errors.append(f"{n_na_band} rows without a tenure_band")
    else:
        print(f"  ✅ tenure_band assigned to all rows")

    print()

    if errors:
        print("  ❌ VALIDATION FAILED:")
        for e in errors:
            print(f"     - {e}")
        raise SystemExit("Cleaning validation failed. See errors above.")

    print("  ✅ All validation checks passed.")
    print()


# ===========================================================================
# 3.8 — EXPORT CLEANED DATA
# ===========================================================================
def export_clean(df: pd.DataFrame) -> Path:
    print("[3.8] EXPORTING CLEANED DATA")
    print("-" * 72)
    out_path = PROCESSED_DIR / "hr_master_clean.csv"
    df.to_csv(out_path, index=False)
    print(f"  ✅ Saved: {out_path}")
    print(f"  Rows: {len(df)}   Columns: {df.shape[1]}")
    print()
    return out_path


# ===========================================================================
# 3.9 — WRITE CLEANING LOG
# ===========================================================================
def write_cleaning_log(
    frames_before: dict,
    df_after: pd.DataFrame,
    output_path: Path,
) -> None:
    print("[3.9] WRITING CLEANING LOG")
    print("-" * 72)

    lines = []
    lines.append("# Cleaning Log — HR Analytics Attrition Case Study\n\n")
    lines.append("**Stage:** 3 — Data Cleaning & Preprocessing  \n")
    lines.append("**Input:** `general_data.csv`, `employee_survey_data.csv`, "
                 "`manager_survey_data.csv`  \n")
    lines.append("**Output:** `data/processed/hr_master_clean.csv`  \n")
    lines.append("**Script:** `python/analysis/03_clean_master.py`\n\n")

    lines.append("---\n\n")
    lines.append("## 1. Summary of Transformations\n\n")
    lines.append("| Step | Transformation | Rows affected | Columns affected |\n")
    lines.append("|---|---|---|---|\n")
    lines.append("| 3.1 | Loaded 3 raw master files | 4,410 each | — |\n")
    lines.append("| 3.2 | Dropped constant columns | 0 | −3 (`EmployeeCount`, `Over18`, `StandardHours`) |\n")
    lines.append("| 3.3 | Merged 3 files (1:1 inner join on `EmployeeID`) | 0 | combined |\n")
    lines.append("| 3.4 | Renamed columns to snake_case | 0 | all |\n")
    lines.append("| 3.5 | Derived `attrition_flag` (0/1) | 0 | +1 |\n")
    lines.append("| 3.6 | Derived `tenure_band` | 0 | +1 |\n")
    lines.append("| 3.7 | Validated row count, null counts, no dupes | 0 | — |\n")
    lines.append("| 3.8 | Exported to CSV | — | — |\n\n")

    lines.append("---\n\n")
    lines.append("## 2. Row Count Preservation\n\n")
    lines.append("| Stage | Rows |\n")
    lines.append("|---|---|\n")
    for name, df in frames_before.items():
        lines.append(f"| {name} (raw) | {len(df)} |\n")
    lines.append(f"| **merged + cleaned** | **{len(df_after)}** |\n\n")
    lines.append("No rows were added or removed at any step. "
                 "Every one of the 4,410 employees is present in the output.\n\n")

    lines.append("---\n\n")
    lines.append("## 3. Columns Dropped\n\n")
    lines.append("| Column | Reason |\n")
    lines.append("|---|---|\n")
    lines.append("| `EmployeeCount` | Constant = 1 (Stage 2 §3) |\n")
    lines.append("| `Over18` | Constant = 'Y' (Stage 2 §3) |\n")
    lines.append("| `StandardHours` | Constant = 8 (Stage 2 §3) |\n\n")
    lines.append("Constant columns cannot differentiate, segment, or predict "
                 "anything. Their removal is a documented decision, not a default.\n\n")

    lines.append("---\n\n")
    lines.append("## 4. Null Values Preserved\n\n")
    lines.append("| Column | Nulls in output |\n")
    lines.append("|---|---|\n")
    for col, n in EXPECTED_NULLS_SNAKE.items():
        actual = int(df_after[col].isna().sum()) if col in df_after.columns else -1
        status = "✅" if actual == n else "❌"
        lines.append(f"| `{col}` | {actual} {status} |\n")
    lines.append("\nNo nulls were imputed or removed. This decision was made in "
                 "Stage 2 §6 based on the discovery that missingness in "
                 "`job_satisfaction` is informative (associated with a 11.17pp "
                 "lower attrition rate). Imputing would erase that signal.\n\n")

    lines.append("---\n\n")
    lines.append("## 5. Derived Columns\n\n")
    lines.append("### `attrition_flag`\n\n")
    lines.append("- Type: integer (0 or 1)\n")
    lines.append("- Derivation: `1` if `attrition == 'Yes'`, else `0`\n")
    lines.append("- Purpose: numeric aggregation in SQL / Python / Power BI\n")
    lines.append("- The original string column `attrition` is preserved for readability\n\n")

    lines.append("### `tenure_band`\n\n")
    lines.append("- Type: categorical (ordered)\n")
    lines.append("- Bands: `0-1 years`, `2-3 years`, `4-5 years`, "
                 "`6-10 years`, `10+ years`\n")
    lines.append("- Derivation: `pd.cut(years_at_company, [-1, 1, 3, 5, 10, 100])`\n")
    lines.append("- Purpose: HR-standard tenure segmentation; simplifies "
                 "grouping in SQL and enables a clean Power BI slicer\n\n")

    lines.append("---\n\n")
    lines.append("## 6. Column Name Standardization\n\n")
    lines.append("All column names converted to `snake_case` for portability across "
                 "SQL, Python, and Power BI. Examples:\n\n")
    lines.append("| Original | Standardized |\n")
    lines.append("|---|---|\n")
    lines.append("| `EmployeeID` | `employee_id` |\n")
    lines.append("| `DistanceFromHome` | `distance_from_home` |\n")
    lines.append("| `MonthlyIncome` | `monthly_income` |\n")
    lines.append("| `NumCompaniesWorked` | `num_companies_worked` |\n")
    lines.append("| `YearsWithCurrManager` | `years_with_curr_manager` |\n\n")

    lines.append("---\n\n")
    lines.append("## 7. Final Schema\n\n")
    lines.append(f"**Rows:** {len(df_after)}  \n")
    lines.append(f"**Columns:** {df_after.shape[1]}\n\n")
    lines.append("| # | Column | Dtype |\n")
    lines.append("|---|---|---|\n")
    for i, (col, dtype) in enumerate(df_after.dtypes.items(), start=1):
        lines.append(f"| {i} | `{col}` | `{dtype}` |\n")
    lines.append("\n")

    lines.append("---\n\n")
    lines.append("## 8. Decisions Deferred to Later Stages\n\n")
    lines.append("| Decision | Stage |\n")
    lines.append("|---|---|\n")
    lines.append("| Build dimension tables for coded categoricals "
                 "(`education`, `job_satisfaction`, etc.) | Stage 5 |\n")
    lines.append("| Process attendance data (`in_time.csv`, `out_time.csv`) | Stage 4 |\n")
    lines.append("| Handle nulls per-analysis (never impute) | Stages 6–7 |\n\n")

    lines.append("---\n\n")
    lines.append("## 9. Validation Results\n\n")
    lines.append("All Stage 3 validation checks passed:\n\n")
    lines.append(f"- Row count = {len(df_after)} (unchanged from raw)\n")
    lines.append("- No duplicate `employee_id`\n")
    lines.append("- No null `employee_id`\n")
    lines.append("- Null counts in affected columns match Stage 2 audit exactly\n")
    lines.append("- Constant columns successfully removed\n")
    lines.append("- `attrition_flag` consistent with `attrition` string\n")
    lines.append("- `tenure_band` assigned to all rows\n\n")

    output_path.write_text("".join(lines), encoding="utf-8")
    print(f"  ✅ Saved: {output_path}")
    print()


# ===========================================================================
# MAIN
# ===========================================================================
def main():
    print("=" * 72)
    print("STAGE 3 — DATA CLEANING & PREPROCESSING")
    print("=" * 72)
    print()

    frames = load_raw()
    frames = drop_constants(frames)
    df     = merge_masters(frames)
    df     = rename_columns(df)
    df     = derive_attrition_flag(df)
    df     = derive_tenure_band(df)

    validate(df)
    export_clean(df)

    write_cleaning_log(
        frames_before=frames,
        df_after=df,
        output_path=DOCS_DIR / "cleaning_log.md",
    )

    print("=" * 72)
    print("STAGE 3 COMPLETE")
    print("=" * 72)
    print("→ Next: Stage 4 — Attendance data pipeline")
    print()


if __name__ == "__main__":
    main()