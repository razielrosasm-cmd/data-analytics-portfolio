"""
Stage 1 — Data Intake & Raw Inspection
--------------------------------------
Purpose:
    Inspect every raw file in the HR Analytics project BEFORE any cleaning.
    This script does not modify data. It only reports what exists.

Outputs:
    - Console: structured inspection report
    - docs/data_inventory.md: saved copy of the report
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Locate project root and raw data folder
# ---------------------------------------------------------------------------
# We use a relative path from the script's location so this works
# regardless of where the project is cloned on any machine.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DOCS_DIR = PROJECT_ROOT / "docs"
DOCS_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# 2. Files to inspect
# ---------------------------------------------------------------------------
CSV_FILES = [
    "general_data.csv",
    "employee_survey_data.csv",
    "manager_survey_data.csv",
    "in_time.csv",
    "out_time.csv",
]
EXCEL_FILES = ["data_dictionary.xlsx"]


# ---------------------------------------------------------------------------
# 3. Helper: inspect one CSV file
# ---------------------------------------------------------------------------
def inspect_csv(file_path: Path) -> dict:
    """
    Read a CSV file with pandas and return a summary dictionary.

    We use `nrows=None` (i.e., read the whole file) because these files
    are small enough. For in_time/out_time this might be slower — if so,
    we can later switch to nrows=5 for the preview only.
    """
    df = pd.read_csv(file_path, low_memory=False)

    summary = {
        "file": file_path.name,
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "null_counts": df.isna().sum().to_dict(),
        "null_percent": (df.isna().mean() * 100).round(2).to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "memory_mb": round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        "preview": df.head(3).to_dict(orient="records"),
    }
    return summary


# ---------------------------------------------------------------------------
# 4. Helper: inspect the Excel data dictionary
# ---------------------------------------------------------------------------
def inspect_excel(file_path: Path) -> dict:
    """Read all sheets from the data dictionary workbook."""
    xls = pd.ExcelFile(file_path)
    result = {"file": file_path.name, "sheets": {}}
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        result["sheets"][sheet] = {
            "rows": len(df),
            "columns": list(df.columns),
        }
    return result


# ---------------------------------------------------------------------------
# 5. Run inspection and build a markdown report
# ---------------------------------------------------------------------------
def main():
    lines = []
    lines.append("# Data Inventory — HR Analytics Attrition Case Study\n")
    lines.append("This report describes the raw data **before any cleaning or transformation**.\n")
    lines.append("---\n")

    # --- CSV files ---
    lines.append("## CSV Files\n")
    for fname in CSV_FILES:
        fpath = RAW_DIR / fname
        if not fpath.exists():
            lines.append(f"### {fname}\n")
            lines.append("**Status:** ❌ NOT FOUND in `data/raw/`\n")
            continue

        s = inspect_csv(fpath)
        lines.append(f"### {fname}\n")
        lines.append(f"- **Rows:** {s['rows']:,}")
        lines.append(f"- **Columns:** {s['columns']}")
        lines.append(f"- **Duplicate rows:** {s['duplicate_rows']}")
        lines.append(f"- **Memory:** {s['memory_mb']} MB\n")

        lines.append("**Column types and null counts:**\n")
        lines.append("| Column | Dtype | Nulls | Null % |")
        lines.append("|---|---|---|---|")
        for col in s["column_names"]:
            lines.append(
                f"| `{col}` | {s['dtypes'][col]} | "
                f"{s['null_counts'][col]} | {s['null_percent'][col]}% |"
            )
        lines.append("")

        lines.append("**First 3 rows (preview):**\n")
        for i, row in enumerate(s["preview"], start=1):
            lines.append(f"- Row {i}: `{row}`")
        lines.append("\n---\n")

    # --- Excel file ---
    lines.append("## Excel File — `data_dictionary.xlsx`\n")
    for fname in EXCEL_FILES:
        fpath = RAW_DIR / fname
        if not fpath.exists():
            lines.append(f"**{fname}:** ❌ NOT FOUND\n")
            continue
        e = inspect_excel(fpath)
        lines.append(f"**Sheets:** {list(e['sheets'].keys())}\n")
        for sheet, info in e["sheets"].items():
            lines.append(f"- Sheet `{sheet}`: {info['rows']} rows, "
                         f"columns = {info['columns']}")

    # --- Write to file ---
    report = "\n".join(lines)
    out_path = DOCS_DIR / "data_inventory.md"
    out_path.write_text(report, encoding="utf-8")

    print(report)
    print(f"\n✅ Report saved to: {out_path}")


if __name__ == "__main__":
    main()