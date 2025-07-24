# Author: Sameen, Chance, and Dr.Manda
# Date: July 11 2025 
# FS3 Summer Camp 

import pandas as pd
import matplotlib.pyplot as plt

# 1. Load data
df1 = pd.read_csv('Site 1-Shallow.csv', sep=';')
df2 = pd.read_csv('Site 2-Shallow.csv', sep=';')
df3 = pd.read_csv('Site 3-Shallow.csv', sep=';')
df5 = pd.read_csv('Site 5-Shallow.csv', sep=';')

# 2. Parse timestamps
for df in (df1, df2, df3, df5):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])

# 3. Create plot
fig, ax = plt.subplots(figsize=(12, 6))

ax.plot(df1['Timestamp'], df1['Electrical Conductivity'],
        color='tab:blue',   label='Site 1')
ax.plot(df2['Timestamp'], df2['Electrical Conductivity'],
        color='tab:orange', label='Site 2')
ax.plot(df3['Timestamp'], df3['Electrical Conductivity'],
        color='tab:green',  label='Site 3')
ax.plot(df5['Timestamp'], df5['Electrical Conductivity'],
        color='tab:red',    label='Site 5')

# 4. Formatting
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Electrical Conductivity (µS/cm)', fontsize=12)
ax.set_title('Shallow Depth Conductivity Over Time\n(Site 1, 2, 3, and 5)', fontsize=14)
ax.grid(True)

# 5. Legend outside
ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), borderaxespad=0)

# Improve x-axis date formatting
fig.autofmt_xdate()

# 6. Layout and display
plt.tight_layout(rect=[0, 0, 0.85, 1])  # leave space on right for legend
plt.show()
