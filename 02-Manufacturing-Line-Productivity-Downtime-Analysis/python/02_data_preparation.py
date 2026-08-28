import pandas as pd
from pathlib import Path

# Project paths

PROJECT_ROOT = Path(__file__).resolve().parent.parent

file_path = PROJECT_ROOT / "data" / "raw" / "Manufacturing_Line_Productivity.xlsx"

# Load each Excel sheet into a separate DataFrame

line_productivity = pd.read_excel(file_path, sheet_name="Line productivity")
products = pd.read_excel(file_path, sheet_name="Products")
line_downtime = pd.read_excel(file_path, sheet_name="Line downtime")
downtime_factors = pd.read_excel(file_path, sheet_name="Downtime factors")


# Check the number of rows and columns in each DataFrame

print(line_productivity.shape)
print(products.shape)
print(line_downtime.shape)
print(downtime_factors.shape)

# Prepare production time fields

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

# Calculate actual batch production time
elapsed_time = end_time - start_time

line_productivity["Actual Batch Time"] = elapsed_time

# Prepare Line Downtime

line_downtime = line_downtime.melt(
    id_vars="Batch",
    var_name="Downtime Factor",
    value_name="Downtime Value"
)

# Keep only actual downtime records

line_downtime = line_downtime[
    line_downtime["Downtime Value"] > 0
]

# Save prepared data

PROCESSED_DATA = PROJECT_ROOT / "data" / "processed"

PROCESSED_DATA.mkdir(exist_ok=True)

line_productivity.to_csv(
    PROCESSED_DATA / "line_productivity_prepared.csv",
    index=False
)

line_downtime.to_csv(
    PROCESSED_DATA / "line_downtime_prepared.csv",
    index=False
)

products.to_csv(
    PROCESSED_DATA / "products.csv",
    index=False
)

downtime_factors.to_csv(
    PROCESSED_DATA / "downtime_factors.csv",
    index=False
)