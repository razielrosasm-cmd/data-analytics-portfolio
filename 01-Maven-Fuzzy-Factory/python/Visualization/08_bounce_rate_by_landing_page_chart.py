import pandas as pd
import matplotlib.pyplot as plt

# Load the bounce rate dataset

bounce_rate = pd.read_csv("../../data/bounce_rate_by_landing_page.csv")

# Create the chart

plt.bar(
    bounce_rate["landing_page"],
    bounce_rate["bounce_rate_percent"]
)

# Add chart title and labels

plt.title("Bounce Rate by Landing Page")
plt.xlabel("Landing Page")
plt.ylabel("Bounce Rate (%)")

# Rotate the landing page labels

plt.xticks(rotation=45)

# Adjust the layout

plt.tight_layout()

# Save the chart

plt.savefig("../08_bounce_rate_by_landing_page.png")

# Display the chart

plt.show()