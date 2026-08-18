import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")


# Convert created_at to datetime
orders["created_at"] = pd.to_datetime(orders["created_at"])


# Display the data types
print(orders.dtypes)