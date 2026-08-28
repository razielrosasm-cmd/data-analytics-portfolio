import pandas as pd


# Load the datasets
orders = pd.read_csv("../data/orders.csv")
products = pd.read_csv("../data/products.csv")


# Calculate orders by product
product_orders = orders.groupby("primary_product_id")["order_id"].count()


# Calculate units sold by product
product_units = orders.groupby("primary_product_id")["items_purchased"].sum()


# Calculate revenue by product
product_revenue = orders.groupby("primary_product_id")["price_usd"].sum()


# Display the results
print("Orders by product:")
print(product_orders)

print("\nUnits sold by product:")
print(product_units)

print("\nRevenue by product:")
print(product_revenue)