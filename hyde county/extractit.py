#to extract salinity and just time stamp from the pre-installation csv file

import pandas as pd

# Read the CSV file
df = pd.read_csv('Preinstallation.csv')

# Select the relevant columns (ensure the column names match exactly, including spaces)
relevant_cols = ['DateTime', 'Salinity (PSU)']

# Extract only those columns
df_selected = df[relevant_cols]

# Save to a new CSV
df_selected.to_csv('salinity_timestamp.csv', index=False)

print("Extracted data saved to salinity_timestamp.csv")
