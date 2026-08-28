import pandas as pd
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "Manufacturing_Line_Productivity.xlsx"

# Load Excel workbook
excel_file = pd.ExcelFile(RAW_DATA)

print("Available sheets:")
print(excel_file.sheet_names)

# Load tables
line_productivity = pd.read_excel(
    RAW_DATA,
    sheet_name="Line productivity"
)

products = pd.read_excel(
    RAW_DATA,
    sheet_name="Products"
)

line_downtime = pd.read_excel(
    RAW_DATA,
    sheet_name="Line downtime"
)

downtime_factors = pd.read_excel(
    RAW_DATA,
    sheet_name="Downtime factors"
)

# Table dimensions validation

print("\n--- TABLE SHAPES ---")

print("Line productivity:", line_productivity.shape)
print("Products:", products.shape)
print("Line downtime:", line_downtime.shape)
print("Downtime factors:", downtime_factors.shape)

# Column names validation

print("\n--- COLUMN NAMES ---")

print("\nLine productivity:")
print(line_productivity.columns.tolist())

print("\nProducts:")
print(products.columns.tolist())

print("\nLine downtime:")
print(line_downtime.columns.tolist())

print("\nDowntime factors:")
print(downtime_factors.columns.tolist())

# Batch count validation

print("\n--- BATCH VALIDATION ---")

total_batches = len(line_productivity)
unique_batches = line_productivity["Batch"].nunique()
duplicate_batches = line_productivity["Batch"].duplicated().sum()

print("Total batches:", total_batches)
print("Unique batches:", unique_batches)
print("Duplicate batch rows:", duplicate_batches)

# Batch range validation

min_batch = line_productivity["Batch"].min()
max_batch = line_productivity["Batch"].max()

print("Minimum batch:", min_batch)
print("Maximum batch:", max_batch)

# products validation

print("\n--- PRODUCT VALIDATION ---")

print("Unique products:")
print(line_productivity["Product"].unique())

print("Number of products:", line_productivity["Product"].nunique())

# Validate that all products in the production data exist in the Products table

product_ids = set(line_productivity["Product"])
dimension_products = set(products["Product"])

missing_products = product_ids - dimension_products

print("Products missing from Products table:", missing_products)

# Operators validation

print("\n--- OPERATOR VALIDATION ---")

print("Operators:")
print(line_productivity["Operator"].unique())

print("Number of operators:", line_productivity["Operator"].nunique())

# Date validation

print("\n--- DATE VALIDATION ---")

line_productivity["Date"] = pd.to_datetime(
    line_productivity["Date"]
)

print("Minimum date:", line_productivity["Date"].min().date())
print("Maximum date:", line_productivity["Date"].max().date())

print("\nProduction dates:")
print(
    line_productivity["Date"]
    .dt.date
    .drop_duplicates()
    .sort_values()
    .tolist()
)

print("\n--- MISSING VALUES ---")

print("\nLine productivity:")
print(line_productivity.isna().sum())

print("\nProducts:")
print(products.isna().sum())

print("\nLine downtime:")
print(line_downtime.isna().sum())

print("\nDowntime factors:")
print(downtime_factors.isna().sum())

# Downtime factor structure validation

print("\n--- DOWNTIME FACTOR VALIDATION ---")

factor_columns = list(line_downtime.columns[1:])

print("Number of downtime factors:", len(factor_columns))
print("Downtime factor IDs:", factor_columns)

print(
    "Number of factor definitions:",
    downtime_factors["Factor"].nunique()
)

downtime_columns = set(line_downtime.columns[1:])
defined_factors = set(downtime_factors["Factor"])

missing_factor_definitions = downtime_columns - defined_factors

print(
    "Downtime columns without factor definition:",
    missing_factor_definitions
)

# Downtime batches validation

print("\n--- DOWNTIME BATCH VALIDATION ---")

production_batches = set(line_productivity["Batch"])
downtime_batches = set(line_downtime["Batch"])

missing_downtime_batches = production_batches - downtime_batches
extra_downtime_batches = downtime_batches - production_batches

print(
    "Production batches missing from downtime:",
    missing_downtime_batches
)

print(
    "Downtime batches missing from production:",
    extra_downtime_batches
)

# Numeric downtime values validation

print("\n--- DOWNTIME VALUE VALIDATION ---")

downtime_values = line_downtime.iloc[:, 1:]

negative_downtime = (downtime_values < 0).sum().sum()

print("Negative downtime values:", negative_downtime)


# ==== Convert Start Time and End Time to time durations ====

# Convert times

start_time = pd.to_timedelta(
    line_productivity["Start Time"].astype(str)
)

end_time = pd.to_timedelta(
    line_productivity["End Time"].astype(str)
)

# Correct midnight crossing
for i in range(len(line_productivity)):
    if end_time[i] < start_time[i]:
        end_time[i] = end_time[i] + pd.Timedelta(days=1)

# Calculate elapsed time

elapsed_time = end_time - start_time

print("\n--- ELAPSED TIME ---")
print(elapsed_time)

# negative durations validation

invalid_durations = []

for i in range(len(elapsed_time)):
    if elapsed_time[i] <= pd.Timedelta(0):
        invalid_durations.append(elapsed_time[i])

print("\n--- PRODUCTION TIME VALIDATION ---")

print(
    "Zero or negative durations:",
    len(invalid_durations)
)

# Validate minimum batch time

minimum_time = pd.Timedelta(hours=1)

short_batches = []

for i in range(len(elapsed_time)):
    if elapsed_time[i] < minimum_time:
        short_batches.append(elapsed_time[i])

print("\n--- MINIMUM BATCH TIME VALIDATION ---")
print("Batches below minimum time:", len(short_batches))

# Validation summary

# Validation summary

print("\n========================================")
print("         VALIDATION SUMMARY")
print("========================================")

print("Total batches:", total_batches)
print("Unique batches:", unique_batches)
print("Duplicate batch rows:", duplicate_batches)

print("Unique products:", line_productivity["Product"].nunique())
print("Unique operators:", line_productivity["Operator"].nunique())

print("Downtime records:", line_downtime.shape[0])
print("Downtime factors:", len(factor_columns))

print("Products missing from Products table:", len(missing_products))

print(
    "Downtime columns without factor definition:",
    len(missing_factor_definitions)
)

print(
    "Production batches missing from downtime:",
    len(missing_downtime_batches)
)

print(
    "Downtime batches missing from production:",
    len(extra_downtime_batches)
)

print("Negative downtime values:", negative_downtime)

print(
    "Zero or negative production durations:",
    len(invalid_durations)
)

print(
    "Batches below minimum time:",
    len(short_batches)
)
