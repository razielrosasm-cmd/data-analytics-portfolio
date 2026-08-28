import pandas as pd
import matplotlib.pyplot as plt

# Load the product revenue over time dataset

revenue = pd.read_csv("../../data/product_revenue_over_time.csv")

# Create the chart

plt.plot(
    revenue["month"],
    revenue["total_revenue"]
)

# Add chart title and labels

plt.title("Product Revenue Over Time")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")

# Rotate the month labels

plt.xticks(rotation=90)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../07_product_revenue_over_time.png")

# Display the chart

plt.show()