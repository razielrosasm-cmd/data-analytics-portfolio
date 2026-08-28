import pandas as pd

# Load the orders dataset

orders = pd.read_csv("../data/orders.csv")

# Convert created_at to datetime

orders["created_at"] = pd.to_datetime(orders["created_at"])

# Create a month column

orders["month"] = orders["created_at"].dt.to_period("M")

# Calculate monthly orders

monthly_orders = orders.groupby("month")["order_id"].count()

# Calculate monthly revenue

monthly_revenue = orders.groupby("month")["price_usd"].sum()

# Calculate average order value

monthly_aov = monthly_revenue / monthly_orders

# Display the results

print(monthly_orders)
print(monthly_revenue)
print(monthly_aov)