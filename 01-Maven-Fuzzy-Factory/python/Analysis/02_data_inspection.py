import pandas as pd


# Load the orders dataset
orders = pd.read_csv("../data/orders.csv")


# Display the number of rows and columns
print(orders.shape)


# Display the column names
print(orders.columns)


# Display the data types
print(orders.dtypes)