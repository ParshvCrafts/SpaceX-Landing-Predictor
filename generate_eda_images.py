"""
Generate EDA Visualizations for SpaceX Falcon 9 Landing Prediction
Saves all charts from the original EDA notebook to webapp/images/eda/
"""

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set the style for all plots
plt.style.use('dark_background')
sns.set_palette("husl")

# Create output directory
output_dir = 'webapp/images/eda'
os.makedirs(output_dir, exist_ok=True)

# Load the dataset
df = pd.read_csv('Datasets/dataset_part_2.csv')
print(f"Loaded dataset with {len(df)} records")

# Custom color palette matching the website theme
colors = {
    'success': '#00D4AA',
    'failure': '#EF4444',
    'primary': '#0066FF',
    'secondary': '#A855F7',
    'accent': '#FF6B35'
}

# ============================================
# 1. Flight Number vs Payload Mass
# ============================================
fig, ax = plt.subplots(figsize=(14, 6))
scatter = ax.scatter(df['FlightNumber'], df['PayloadMass'],
                     c=df['Class'].map({0: colors['failure'], 1: colors['success']}),
                     s=100, alpha=0.7, edgecolors='white', linewidths=0.5)
ax.set_xlabel('Flight Number', fontsize=14, color='white')
ax.set_ylabel('Payload Mass (kg)', fontsize=14, color='white')
ax.set_title('Flight Number vs Payload Mass', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2)

# Add legend
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['success'], markersize=10, label='Success', linestyle='None'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor=colors['failure'], markersize=10, label='Failure', linestyle='None')
]
ax.legend(handles=legend_elements, loc='upper left', facecolor='#1a1a2e')

plt.tight_layout()
plt.savefig(f'{output_dir}/flight_vs_payload.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: flight_vs_payload.png")

# ============================================
# 2. Flight Number vs Launch Site
# ============================================
fig, ax = plt.subplots(figsize=(14, 6))
for cls, color in [(0, colors['failure']), (1, colors['success'])]:
    mask = df['Class'] == cls
    ax.scatter(df.loc[mask, 'FlightNumber'], df.loc[mask, 'LaunchSite'],
               c=color, s=100, alpha=0.7, edgecolors='white', linewidths=0.5,
               label='Success' if cls == 1 else 'Failure')

ax.set_xlabel('Flight Number', fontsize=14, color='white')
ax.set_ylabel('Launch Site', fontsize=14, color='white')
ax.set_title('Flight Number vs Launch Site', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='x')
ax.legend(loc='upper left', facecolor='#1a1a2e')

plt.tight_layout()
plt.savefig(f'{output_dir}/flight_vs_launchsite.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: flight_vs_launchsite.png")

# ============================================
# 3. Payload Mass vs Launch Site
# ============================================
fig, ax = plt.subplots(figsize=(14, 6))
for cls, color in [(0, colors['failure']), (1, colors['success'])]:
    mask = df['Class'] == cls
    ax.scatter(df.loc[mask, 'PayloadMass'], df.loc[mask, 'LaunchSite'],
               c=color, s=100, alpha=0.7, edgecolors='white', linewidths=0.5,
               label='Success' if cls == 1 else 'Failure')

ax.set_xlabel('Payload Mass (kg)', fontsize=14, color='white')
ax.set_ylabel('Launch Site', fontsize=14, color='white')
ax.set_title('Payload Mass vs Launch Site', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='x')
ax.legend(loc='upper right', facecolor='#1a1a2e')

plt.tight_layout()
plt.savefig(f'{output_dir}/payload_vs_launchsite.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: payload_vs_launchsite.png")

# ============================================
# 4. Success Rate by Orbit Type
# ============================================
orbit_success = df.groupby('Orbit')['Class'].mean().sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(orbit_success.index, orbit_success.values * 100,
              color=[colors['success'] if v > 0.5 else colors['primary'] for v in orbit_success.values],
              edgecolor='white', linewidth=0.5)
ax.set_xlabel('Orbit Type', fontsize=14, color='white')
ax.set_ylabel('Success Rate (%)', fontsize=14, color='white')
ax.set_title('Success Rate by Orbit Type', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='y')
ax.set_ylim(0, 110)

# Add value labels
for bar, val in zip(bars, orbit_success.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{val*100:.0f}%', ha='center', va='bottom', fontsize=10, color='white')

plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/orbit_success_rate.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: orbit_success_rate.png")

# ============================================
# 5. Flight Number vs Orbit Type
# ============================================
fig, ax = plt.subplots(figsize=(14, 8))
for cls, color in [(0, colors['failure']), (1, colors['success'])]:
    mask = df['Class'] == cls
    ax.scatter(df.loc[mask, 'FlightNumber'], df.loc[mask, 'Orbit'],
               c=color, s=100, alpha=0.7, edgecolors='white', linewidths=0.5,
               label='Success' if cls == 1 else 'Failure')

ax.set_xlabel('Flight Number', fontsize=14, color='white')
ax.set_ylabel('Orbit Type', fontsize=14, color='white')
ax.set_title('Flight Number vs Orbit Type', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='x')
ax.legend(loc='upper left', facecolor='#1a1a2e')

plt.tight_layout()
plt.savefig(f'{output_dir}/flight_vs_orbit.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: flight_vs_orbit.png")

# ============================================
# 6. Payload Mass vs Orbit Type
# ============================================
fig, ax = plt.subplots(figsize=(14, 8))
for cls, color in [(0, colors['failure']), (1, colors['success'])]:
    mask = df['Class'] == cls
    ax.scatter(df.loc[mask, 'PayloadMass'], df.loc[mask, 'Orbit'],
               c=color, s=100, alpha=0.7, edgecolors='white', linewidths=0.5,
               label='Success' if cls == 1 else 'Failure')

ax.set_xlabel('Payload Mass (kg)', fontsize=14, color='white')
ax.set_ylabel('Orbit Type', fontsize=14, color='white')
ax.set_title('Payload Mass vs Orbit Type', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='x')
ax.legend(loc='upper right', facecolor='#1a1a2e')

plt.tight_layout()
plt.savefig(f'{output_dir}/payload_vs_orbit.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: payload_vs_orbit.png")

# ============================================
# 7. Yearly Success Rate Trend
# ============================================
# Extract year from date
df_yearly = df.copy()
df_yearly['Year'] = pd.to_datetime(df_yearly['Date']).dt.year
yearly_success = df_yearly.groupby('Year')['Class'].mean()

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(yearly_success.index, yearly_success.values * 100,
        color=colors['success'], linewidth=3, marker='o', markersize=10)
ax.fill_between(yearly_success.index, yearly_success.values * 100,
                alpha=0.2, color=colors['success'])

ax.set_xlabel('Year', fontsize=14, color='white')
ax.set_ylabel('Success Rate (%)', fontsize=14, color='white')
ax.set_title('Yearly Launch Success Rate Trend', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2)
ax.set_ylim(0, 110)

# Add value labels
for x, y in zip(yearly_success.index, yearly_success.values * 100):
    ax.annotate(f'{y:.0f}%', (x, y), textcoords="offset points",
                xytext=(0, 10), ha='center', fontsize=9, color='white')

plt.tight_layout()
plt.savefig(f'{output_dir}/yearly_success_trend.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: yearly_success_trend.png")

# ============================================
# 8. Launch Site Success Rate
# ============================================
site_success = df.groupby('LaunchSite')['Class'].agg(['mean', 'count']).reset_index()
site_success.columns = ['LaunchSite', 'SuccessRate', 'TotalLaunches']
site_success = site_success.sort_values('SuccessRate', ascending=False)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.bar(site_success['LaunchSite'], site_success['SuccessRate'] * 100,
              color=[colors['success'] if v > 0.6 else colors['primary'] for v in site_success['SuccessRate']],
              edgecolor='white', linewidth=0.5)

ax.set_xlabel('Launch Site', fontsize=14, color='white')
ax.set_ylabel('Success Rate (%)', fontsize=14, color='white')
ax.set_title('Success Rate by Launch Site', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='y')
ax.set_ylim(0, 110)

# Add value labels with launch count
for bar, (rate, count) in zip(bars, zip(site_success['SuccessRate'], site_success['TotalLaunches'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{rate*100:.0f}%\n({count} launches)', ha='center', va='bottom', fontsize=10, color='white')

plt.xticks(rotation=15, ha='right')
plt.tight_layout()
plt.savefig(f'{output_dir}/launchsite_success_rate.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: launchsite_success_rate.png")

# ============================================
# 9. Booster Version Success Rate
# ============================================
booster_success = df.groupby('BoosterVersion')['Class'].agg(['mean', 'count']).reset_index()
booster_success.columns = ['BoosterVersion', 'SuccessRate', 'Count']
booster_success = booster_success.sort_values('Count', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(booster_success['BoosterVersion'], booster_success['SuccessRate'] * 100,
               color=[colors['success'] if v > 0.6 else colors['primary'] for v in booster_success['SuccessRate']],
               edgecolor='white', linewidth=0.5)

ax.set_xlabel('Success Rate (%)', fontsize=14, color='white')
ax.set_ylabel('Booster Version', fontsize=14, color='white')
ax.set_title('Success Rate by Booster Version', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.grid(True, alpha=0.2, axis='x')
ax.set_xlim(0, 110)

plt.tight_layout()
plt.savefig(f'{output_dir}/booster_success_rate.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: booster_success_rate.png")

# ============================================
# 10. Class Distribution (Pie Chart)
# ============================================
class_counts = df['Class'].value_counts()

fig, ax = plt.subplots(figsize=(8, 8))
wedges, texts, autotexts = ax.pie(class_counts,
                                   labels=['Success', 'Failure'],
                                   colors=[colors['success'], colors['failure']],
                                   autopct='%1.1f%%',
                                   startangle=90,
                                   explode=(0.05, 0),
                                   textprops={'color': 'white', 'fontsize': 14})
ax.set_title('Landing Outcome Distribution', fontsize=16, fontweight='bold', color='white', pad=20)
fig.patch.set_facecolor('#0A0A14')

# Add count labels
ax.text(0, -1.3, f'Total: {len(df)} launches\nSuccess: {class_counts[1]} | Failure: {class_counts[0]}',
        ha='center', fontsize=12, color='white')

plt.tight_layout()
plt.savefig(f'{output_dir}/class_distribution.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: class_distribution.png")

# ============================================
# 11. GridFins & Legs vs Success
# ============================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# GridFins
gridfins_success = df.groupby('GridFins')['Class'].mean() * 100
axes[0].bar(['No GridFins', 'GridFins'], gridfins_success.values,
            color=[colors['failure'], colors['success']], edgecolor='white', linewidth=0.5)
axes[0].set_ylabel('Success Rate (%)', fontsize=12, color='white')
axes[0].set_title('GridFins Impact on Success', fontsize=14, fontweight='bold', color='white')
axes[0].set_facecolor('#0A0A14')
axes[0].set_ylim(0, 110)
for i, v in enumerate(gridfins_success.values):
    axes[0].text(i, v + 2, f'{v:.0f}%', ha='center', fontsize=12, color='white')

# Legs
legs_success = df.groupby('Legs')['Class'].mean() * 100
axes[1].bar(['No Legs', 'Legs'], legs_success.values,
            color=[colors['failure'], colors['success']], edgecolor='white', linewidth=0.5)
axes[1].set_ylabel('Success Rate (%)', fontsize=12, color='white')
axes[1].set_title('Landing Legs Impact on Success', fontsize=14, fontweight='bold', color='white')
axes[1].set_facecolor('#0A0A14')
axes[1].set_ylim(0, 110)
for i, v in enumerate(legs_success.values):
    axes[1].text(i, v + 2, f'{v:.0f}%', ha='center', fontsize=12, color='white')

fig.patch.set_facecolor('#0A0A14')
plt.tight_layout()
plt.savefig(f'{output_dir}/hardware_impact.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: hardware_impact.png")

# ============================================
# 12. Reused vs Success
# ============================================
fig, ax = plt.subplots(figsize=(10, 6))
reused_success = df.groupby('Reused')['Class'].agg(['mean', 'count']).reset_index()
reused_success.columns = ['Reused', 'SuccessRate', 'Count']

bars = ax.bar(['New Booster', 'Reused Booster'], reused_success['SuccessRate'] * 100,
              color=[colors['primary'], colors['success']], edgecolor='white', linewidth=0.5)

ax.set_ylabel('Success Rate (%)', fontsize=14, color='white')
ax.set_title('New vs Reused Booster Success Rate', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.set_ylim(0, 110)

for bar, (rate, count) in zip(bars, zip(reused_success['SuccessRate'], reused_success['Count'])):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
            f'{rate*100:.0f}%\n({count} flights)', ha='center', fontsize=12, color='white')

plt.tight_layout()
plt.savefig(f'{output_dir}/reused_vs_success.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: reused_vs_success.png")

# ============================================
# 13. Payload Mass Distribution
# ============================================
fig, ax = plt.subplots(figsize=(12, 6))

# Histogram with KDE
ax.hist(df[df['Class'] == 1]['PayloadMass'], bins=20, alpha=0.7,
        color=colors['success'], label='Success', edgecolor='white')
ax.hist(df[df['Class'] == 0]['PayloadMass'], bins=20, alpha=0.5,
        color=colors['failure'], label='Failure', edgecolor='white')

ax.set_xlabel('Payload Mass (kg)', fontsize=14, color='white')
ax.set_ylabel('Number of Launches', fontsize=14, color='white')
ax.set_title('Payload Mass Distribution by Outcome', fontsize=16, fontweight='bold', color='white')
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')
ax.legend(facecolor='#1a1a2e')
ax.grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig(f'{output_dir}/payload_distribution.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: payload_distribution.png")

# ============================================
# 14. Correlation Heatmap
# ============================================
# Select numeric columns
numeric_cols = ['FlightNumber', 'PayloadMass', 'Flights', 'GridFins', 'Reused',
                'Legs', 'Block', 'ReusedCount', 'Class']
df_numeric = df[numeric_cols].copy()
df_numeric['GridFins'] = df_numeric['GridFins'].astype(int)
df_numeric['Reused'] = df_numeric['Reused'].astype(int)
df_numeric['Legs'] = df_numeric['Legs'].astype(int)

corr_matrix = df_numeric.corr()

fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
cmap = sns.diverging_palette(220, 150, as_cmap=True)

sns.heatmap(corr_matrix, mask=mask, cmap=cmap, center=0,
            annot=True, fmt='.2f', square=True, linewidths=0.5,
            ax=ax, cbar_kws={"shrink": 0.8})

ax.set_title('Feature Correlation Heatmap', fontsize=16, fontweight='bold', color='white', pad=20)
ax.set_facecolor('#0A0A14')
fig.patch.set_facecolor('#0A0A14')

plt.tight_layout()
plt.savefig(f'{output_dir}/correlation_heatmap.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: correlation_heatmap.png")

# ============================================
# 15. Summary Statistics Card
# ============================================
fig, ax = plt.subplots(figsize=(14, 8))
ax.axis('off')
fig.patch.set_facecolor('#0A0A14')

# Create text summary
summary_text = f"""
SPACEX FALCON 9 DATASET SUMMARY

Total Launches: {len(df)}
Success Rate: {df['Class'].mean()*100:.1f}%
Successful Landings: {df['Class'].sum()}
Failed Landings: {len(df) - df['Class'].sum()}

Payload Statistics:
  - Mean: {df['PayloadMass'].mean():.0f} kg
  - Min: {df['PayloadMass'].min():.0f} kg
  - Max: {df['PayloadMass'].max():.0f} kg

Launch Sites: {df['LaunchSite'].nunique()}
Orbit Types: {df['Orbit'].nunique()}
Date Range: {df['Date'].min()} to {df['Date'].max()}

Key Insights:
  - GridFins improve success rate by ~{(df[df['GridFins']==True]['Class'].mean() - df[df['GridFins']==False]['Class'].mean())*100:.0f}%
  - Reused boosters success: {df[df['Reused']==True]['Class'].mean()*100:.0f}%
  - Block 5 success rate: {df[df['Block']==5]['Class'].mean()*100:.0f}%
"""

ax.text(0.5, 0.5, summary_text, transform=ax.transAxes,
        fontsize=14, verticalalignment='center', horizontalalignment='center',
        color='white', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='#1a1a2e', edgecolor=colors['primary'], linewidth=2))

plt.tight_layout()
plt.savefig(f'{output_dir}/dataset_summary.png', dpi=150, facecolor='#0A0A14', bbox_inches='tight')
plt.close()
print("Saved: dataset_summary.png")

print(f"\n✅ All EDA visualizations saved to {output_dir}/")
print("Total images generated: 15")
