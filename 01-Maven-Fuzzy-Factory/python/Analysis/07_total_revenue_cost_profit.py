import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")

# Calculate profit for each order
orders["profit_usd"] = orders["price_usd"] - orders["cogs_usd"]


# Calculate total revenue
total_revenue = orders["price_usd"].sum()


# Calculate total cost
total_cost = orders["cogs_usd"].sum()


# Calculate total profit
total_profit = orders["profit_usd"].sum()


# Display the results
print("Total Revenue:", total_revenue)
print("Total Cost:", total_cost)
print("Total Profit:", total_profit)