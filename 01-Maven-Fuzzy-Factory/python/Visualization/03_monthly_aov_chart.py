import pandas as pd
import matplotlib.pyplot as plt

# Load the orders dataset

orders = pd.read_csv("../data/orders.csv")

# Convert created_at to datetime

orders["created_at"] = pd.to_datetime(orders["created_at"])

# Create a month column

orders["month"] = orders["created_at"].dt.to_period("M")

# Calculate monthly revenue

monthly_revenue = orders.groupby("month")["price_usd"].sum()

# Calculate monthly orders

monthly_orders = orders.groupby("month")["order_id"].count()

# Calculate monthly AOV

monthly_aov = monthly_revenue / monthly_orders

# Create the chart

plt.plot(monthly_aov.index.astype(str), monthly_aov.values)

# Add chart title and labels

plt.title("Monthly Average Order Value")
plt.xlabel("Month")
plt.ylabel("Average Order Value (USD)")

# Rotate the month labels

plt.xticks(rotation=90)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../dashboard_images/03_monthly_aov.png")

# Display the chart

plt.show()