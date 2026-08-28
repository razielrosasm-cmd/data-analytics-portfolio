import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")


# Calculate orders by product
product_orders = orders.groupby("primary_product_id")["order_id"].count()


# Calculate units sold by product
product_units = orders.groupby("primary_product_id")["items_purchased"].sum()


# Calculate revenue by product
product_revenue = orders.groupby("primary_product_id")["price_usd"].sum()


# Calculate revenue per order
product_aov = product_revenue / product_orders


# Calculate units per order
product_units_per_order = product_units / product_orders


# Display the results
print("Revenue per order:")
print(product_aov)

print("\nUnits per order:")
print(product_units_per_order)