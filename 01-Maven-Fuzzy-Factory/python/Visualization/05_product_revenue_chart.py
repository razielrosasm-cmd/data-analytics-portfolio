import pandas as pd
import matplotlib.pyplot as plt

# Load the product performance dataset

products = pd.read_csv("../../data/product_performance_overview.csv")

# Create the chart

plt.bar(
    products["product_name"],
    products["total_revenue"]
)

# Add chart title and labels

plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (USD)")

# Rotate the product labels

plt.xticks(rotation=45)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../05_product_revenue.png")

# Display the chart

plt.show()