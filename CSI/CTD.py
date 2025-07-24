# Author: Sameen, Chance, and Dr.Manda
# Date: July 11 2025 
# FS3 Summer Camp 

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Load the CSV files
site2_data = pd.read_csv('Site 2 CTD.csv', delimiter=';')
site4_data = pd.read_csv('Site 4 CTD.csv', delimiter=';')

# Convert timestamp to datetime for both datasets
site2_data['Timestamp'] = pd.to_datetime(site2_data['Timestamp'])
site4_data['Timestamp'] = pd.to_datetime(site4_data['Timestamp'])

# Create the plot
plt.figure(figsize=(12, 8))

# Plot both lines
plt.plot(site2_data['Timestamp'], site2_data['Electrical Conductivity'], 
         label='Site 2', linewidth=2, marker='o', markersize=3)
plt.plot(site4_data['Timestamp'], site4_data['Electrical Conductivity'], 
         label='Site 4', linewidth=2, marker='s', markersize=3)

# Customize the plot
plt.title('Electrical Conductivity vs Time for CTD Sites', fontsize=16, fontweight='bold')
plt.xlabel('Time', fontsize=12)
plt.ylabel('Electrical Conductivity (µS/cm)', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Adjust layout to prevent label cutoff
plt.tight_layout()

# Display the plot
plt.show()

# Optional: Save the plot
plt.savefig('conductivity_vs_time.png', dpi=300, bbox_inches='tight')
