import pandas as pd


# Load the products dataset
products = pd.read_csv("../data/products.csv")


# Convert product launch date to datetime
products["created_at"] = pd.to_datetime(products["created_at"])


# Display product launch information
print(products[["product_id", "product_name", "created_at"]])