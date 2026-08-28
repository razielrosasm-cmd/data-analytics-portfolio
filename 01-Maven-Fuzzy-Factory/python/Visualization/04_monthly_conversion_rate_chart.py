import pandas as pd
import matplotlib.pyplot as plt

# Load the monthly conversion rate dataset

conversion = pd.read_csv("../../data/monthly_conversion_rate.csv")

# Create the chart

plt.plot(
    conversion["month"],
    conversion["conversion_rate_percent"]
)

# Add chart title and labels

plt.title("Monthly Conversion Rate")
plt.xlabel("Month")
plt.ylabel("Conversion Rate (%)")

# Rotate the month labels

plt.xticks(rotation=90)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../04_monthly_conversion_rate.png")

# Display the chart

plt.show()