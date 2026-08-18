import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")

# Calculate profit for each order
orders["profit_usd"] = orders["price_usd"] - orders["cogs_usd"]


# Display the first 5 orders
print(orders[["order_id", "price_usd", "cogs_usd", "profit_usd"]].head())