import pandas as pd
import matplotlib.pyplot as plt

# Load the orders dataset

orders = pd.read_csv("../data/orders.csv")

# Convert created_at to datetime

orders["created_at"] = pd.to_datetime(orders["created_at"])

# Create a month column

orders["month"] = orders["created_at"].dt.to_period("M")

# Calculate monthly orders

monthly_orders = orders.groupby("month")["order_id"].count()

# Create the chart

plt.plot(monthly_orders.index.astype(str), monthly_orders.values)

# Add chart title and labels

plt.title("Monthly Orders")
plt.xlabel("Month")
plt.ylabel("Number of Orders")

# Rotate the month labels

plt.xticks(rotation=90)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../dashboard_images/02_monthly_orders.png")

# Display the chart

plt.show()