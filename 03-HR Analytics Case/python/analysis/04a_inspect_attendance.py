"""
Stage 4a — Inspect raw attendance files (read-only)
====================================================
Purpose:
    Before writing the full pipeline, understand the exact structure of
    in_time.csv and out_time.csv. Print shape, dtypes, sample values,
    and NA counts. NO transformation.
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR      = PROJECT_ROOT / "data" / "raw"

ATTENDANCE_FILES = {
    "in_time":  "in_time.csv",
    "out_time": "out_time.csv",
}


def inspect(name: str, path: Path) -> None:
    print("=" * 72)
    print(f"INSPECTING: {name}  ({path.name})")
    print("=" * 72)

    # Read just the header first to see column structure
    with open(path, "r", encoding="utf-8") as f:
        header = f.readline().strip()

    header_cols = header.split(",")
    print(f"\nRaw header: {header_cols[:5]} ... "
          f"{header_cols[-3:]}  (total {len(header_cols)} cols)")

    # Full read (may take a few seconds)
    df = pd.read_csv(path)
    print(f"\nShape: {df.shape}")
    print(f"First column name: {df.columns[0]!r}")
    print(f"Second column name: {df.columns[1]!r}")
    print(f"Last column name: {df.columns[-1]!r}")

    print(f"\nFirst 3 rows, first 5 cols:")
    print(df.iloc[:3, :5].to_string())

    print(f"\nDtypes (first 5):")
    print(df.dtypes.head(5).to_string())

    # Employee ID column — check
    id_col = df.columns[0]
    print(f"\nID column: {id_col!r}")
    print(f"  unique IDs: {df[id_col].nunique()}")
    print(f"  min/max:    {df[id_col].min()} / {df[id_col].max()}")
    print(f"  null IDs:   {df[id_col].isna().sum()}")

    # Data columns — how many, and what's inside
    data_cols = df.columns[1:]
    print(f"\nData columns: {len(data_cols)}")

    # NA rate across data columns
    na_cells = int(df[data_cols].isna().sum().sum())
    total_cells = len(df) * len(data_cols)
    print(f"NA cells: {na_cells:,} / {total_cells:,} "
          f"({100 * na_cells / total_cells:.2f}%)")

    # Sample a non-null value to see the timestamp format
    sample_found = False
    for col in data_cols:
        non_null = df[col].dropna()
        if len(non_null) > 0:
            print(f"\nSample non-null value from {col!r}:")
            print(f"  {non_null.iloc[0]!r}")
            sample_found = True
            break
    if not sample_found:
        print("\n⚠ No non-null values found in data columns")

    print()


def main():
    for name, fname in ATTENDANCE_FILES.items():
        path = RAW_DIR / fname
        if not path.exists():
            print(f"⚠ MISSING: {path}")
            continue
        inspect(name, path)

    print("=" * 72)
    print("INSPECTION COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()