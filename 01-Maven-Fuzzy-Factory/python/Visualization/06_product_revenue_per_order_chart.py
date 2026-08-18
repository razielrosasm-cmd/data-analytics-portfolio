import pandas as pd
import matplotlib.pyplot as plt

# Load the product revenue and order value dataset

products = pd.read_csv("../../data/product_revenue_order_value.csv")

# Create the chart

plt.bar(
    products["product_name"],
    products["revenue_per_order"]
)

# Add chart title and labels

plt.title("Revenue per Order by Product")
plt.xlabel("Product")
plt.ylabel("Revenue per Order (USD)")

# Rotate the product labels

plt.xticks(rotation=45)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../06_product_revenue_per_order.png")

# Display the chart

plt.show()