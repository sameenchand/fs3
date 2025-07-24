import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import gsw
from scipy.stats import mannwhitneyu

# ------------------- Load Data -------------------
# Load pre-installation salinity data (hourly, comma-separated)
pre = pd.read_csv('salinity_timestamp.csv')
pre['Timestamp'] = pd.to_datetime(pre['DateTime'])
pre['Salinity'] = pd.to_numeric(pre['Salinity (PSU)'], errors='coerce')
pre = pre[['Timestamp', 'Salinity']].dropna(subset=['Salinity'])

# Load post-installation data (5-min, semicolon-separated)
post = pd.read_csv('usethis.csv', sep=';')
post = post[['Timestamp', 'Electrical Conductivity', 'Temperature']].dropna(subset=['Timestamp', 'Electrical Conductivity', 'Temperature'])
post['Timestamp'] = pd.to_datetime(post['Timestamp'])
post['EC'] = pd.to_numeric(post['Electrical Conductivity'], errors='coerce')
post['Temp'] = pd.to_numeric(post['Temperature'], errors='coerce')

# -------------- Conductivity to Salinity --------------
def conductivity_to_salinity(conductivity_us_cm, temperature_c, pressure_dbar=0):
    conductivity_ms_cm = conductivity_us_cm / 1000
    return gsw.SP_from_C(conductivity_ms_cm, temperature_c, pressure_dbar)

post['Salinity'] = conductivity_to_salinity(post['EC'].values, post['Temp'].values, 0)
post = post.dropna(subset=['Salinity'])  # in case any salinity is nan

# ------------------- Data Cleaning (Drop NaNs) -------------------
pre_clean = pre['Salinity'].dropna()
post_clean = post['Salinity'].dropna()  # 5-min frequency

# ------------------- Plot Salinity Over Time -------------------
plt.figure(figsize=(14,6))
plt.plot(pre['Timestamp'], pre['Salinity'], color='red', label='Pre-Installation (hourly)')
plt.plot(post['Timestamp'], post['Salinity'], color='blue', label='Post-Installation (5-min)')
plt.xlabel('Time')
plt.ylabel('Salinity (PSU)')
plt.title('Upstream Salinity: Before (hourly) vs After (5-min) System Installation')
plt.legend()
plt.grid(alpha=0.4)
plt.tight_layout()
plt.show()

# ------------------- Medians & Mann-Whitney U Test -------------------
median_pre = pre_clean.median()
median_post = post_clean.median()
percent_change = 100 * (median_post - median_pre) / median_pre

u_stat, p_value = mannwhitneyu(pre_clean, post_clean, alternative='two-sided')
effect_size = u_stat / (len(pre_clean) * len(post_clean))

# ------------------- Output Results to Console -------------------
print("========= Median Salinity Values =========")
print(f"PRE-installation median:  {median_pre:.2f} PSU")
print(f"POST-installation median: {median_post:.2f} PSU")
print(f"Percentage change:         {percent_change:+.2f}%")
print()
print("========= Mann-Whitney U Test =========")
print(f"U statistic: {u_stat:,.0f}")
print(f"p-value:     {p_value:.4g}")
if p_value < 0.05:
    print("Result:      Statistically significant difference (p < 0.05)")
else:
    print("Result:      No statistically significant difference (p >= 0.05)")
print()
print("========= Effect Size (Rank-biserial) =========")
print(f"Effect size: {effect_size:.3f}")
print()

# ------------------- Effectiveness Interpretation -------------------
print("========= System Effectiveness Statement =========")
if median_post < median_pre and p_value < 0.05:
    print(f"The median salinity decreased from {median_pre:.2f} to {median_post:.2f} PSU after system installation "
          f"({percent_change:+.2f}%), which is a statistically significant reduction (p={p_value:.4g}).\n"
          ">>> The water control system IS effective at reducing salinity upstream.")
elif median_post > median_pre and p_value < 0.05:
    print(f"The median salinity increased from {median_pre:.2f} to {median_post:.2f} PSU after system installation "
          f"({percent_change:+.2f}%), and this rise is statistically significant (p={p_value:.4g}).\n"
          ">>> The water control system is NOT working: salinity is higher after installation.")
else:
    print(f"No statistically significant change in upstream salinity (median changed by {percent_change:+.2f}%, p={p_value:.4g}).\n"
          ">>> The water control system's impact on salinity is inconclusive.")
print()

# ------------------- Outlier and Data Quality (Extra) -------------------
pre_outliers = pre_clean[np.abs(pre_clean - pre_clean.median()) > 3 * pre_clean.std()]
post_outliers = post_clean[np.abs(post_clean - post_clean.median()) > 3 * post_clean.std()]
print("========= Data Quality Report =========")
print(f"Pre:  {pre['Salinity'].isna().sum()} missing, {len(pre_outliers)} outliers")
print(f"Post: {post['Salinity'].isna().sum()} missing, {len(post_outliers)} outliers")
print()
