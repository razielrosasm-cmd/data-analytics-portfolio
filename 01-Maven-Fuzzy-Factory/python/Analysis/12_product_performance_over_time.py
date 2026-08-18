import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")


# Convert created_at to datetime
orders["created_at"] = pd.to_datetime(orders["created_at"])


# Create a month column
orders["month"] = orders["created_at"].dt.to_period("M")


# Calculate orders by product and month
product_orders = orders.groupby(
    ["primary_product_id", "month"]
)["order_id"].count()


# Calculate revenue by product and month
product_revenue = orders.groupby(
    ["primary_product_id", "month"]
)["price_usd"].sum()


# Display the results
print("Orders by product and month:")
print(product_orders)

print("\nRevenue by product and month:")
print(product_revenue)