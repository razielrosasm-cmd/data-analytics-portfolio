import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")


# Convert created_at to datetime
orders["created_at"] = pd.to_datetime(orders["created_at"])


# Calculate profit for each order
orders["profit_usd"] = orders["price_usd"] - orders["cogs_usd"]


# Create a month column
orders["month"] = orders["created_at"].dt.to_period("M")


# Calculate monthly revenue, cost and profit
monthly_results = orders.groupby("month")[[
    "price_usd",
    "cogs_usd",
    "profit_usd"
]].sum()


# Display the results
print(monthly_results)