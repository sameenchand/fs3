import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gsw

# --- LOAD DATA ---
downstream = pd.read_csv('downstream.csv', sep=';')
upstream = pd.read_csv('upstream.csv', sep=';')

downstream = downstream.dropna(subset=['Electrical Conductivity', 'Temperature']).copy()
upstream = upstream.dropna(subset=['Electrical Conductivity', 'Temperature']).copy()

downstream['Timestamp'] = pd.to_datetime(downstream['Timestamp'])
upstream['Timestamp'] = pd.to_datetime(upstream['Timestamp'])

# --- SALINITY CONVERSION ---
def conductivity_to_salinity(cond_us_cm, temp_c, pressure=0):
    cond_ms_cm = cond_us_cm / 1000
    return gsw.SP_from_C(cond_ms_cm, temp_c, pressure)

downstream['Salinity'] = conductivity_to_salinity(downstream['Electrical Conductivity'], downstream['Temperature'])
upstream['Salinity']   = conductivity_to_salinity(upstream['Electrical Conductivity'],   upstream['Temperature'])

# --- ALIGN BY TIMESTAMP ---
combined = pd.merge_asof(
    downstream.sort_values('Timestamp')[['Timestamp', 'Salinity']],
    upstream.sort_values('Timestamp')[['Timestamp', 'Salinity']],
    on='Timestamp',
    direction='nearest',
    tolerance=pd.Timedelta("10min"),
    suffixes=('_downstream', '_upstream')
)

'''# --- STATUS LOGIC (YOUR RULE) ---
# System is WORKING if downstream > upstream, else NOT WORKING
combined['Status'] = np.where(
    combined['Salinity_downstream'] > combined['Salinity_upstream'],
    'WORKING','NOT WORKING'
)'''

# --- PLOT & STATUS ON GRAPH ---
fig, ax = plt.subplots(figsize=(14,7))
ax.plot(combined['Timestamp'], combined['Salinity_downstream'], label='Downstream', color='red', linewidth=2)
ax.plot(combined['Timestamp'], combined['Salinity_upstream'], label='Upstream', color='blue', linewidth=2)

'''# highlight status as colored points
working = combined['Status'] == 'WORKING'
not_working = ~working
ax.scatter(combined.loc[working, 'Timestamp'],    combined.loc[working,    'Salinity_downstream'], color='green',  label='WORKING', s=16, marker='o', alpha=0.8)
ax.scatter(combined.loc[not_working, 'Timestamp'],combined.loc[not_working,'Salinity_downstream'], color='orange', label='NOT WORKING', s=16, marker='x', alpha=0.8)
'''
'''# Calculate differences and add status to plot
mean_down = combined['Salinity_downstream'].mean()
mean_up = combined['Salinity_upstream'].mean()
diff = mean_down - mean_up
pct_diff = 100 * diff / mean_up

if diff > 0:
    status_text = f"Status: SYSTEM WORKING (Downstream > Upstream)\nDifference: {diff:.4f} PSU\nPercent diff: {pct_diff:.2f}%"
    box_color = "green"
else:
    status_text = f"Status: SYSTEM NOT WORKING (Downstream <= Upstream)\nDifference: {diff:.4f} PSU\nPercent diff: {pct_diff:.2f}%"
    box_color = "red"
'''
'''ax.text(0.01, 0.98, status_text, transform=ax.transAxes, fontsize=13, 
        verticalalignment="top", bbox=dict(facecolor=box_color, alpha=0.2, edgecolor='k'))
'''
ax.set_xlabel('Timestamp', fontsize=13)
ax.set_ylabel('Practical Salinity (PSU)', fontsize=13)
ax.set_title('Upstream/Downstream Salinity & System Working Status', fontsize=15, fontweight='bold')
ax.legend(fontsize=12)
ax.grid(True, alpha=0.3)
plt.xticks(rotation=30)
plt.tight_layout()
plt.show()
