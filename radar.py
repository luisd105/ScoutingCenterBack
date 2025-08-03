import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#  Read the tables from FBref page
url = "https://fbref.com/en/players/34e12499/Nico-Schlotterbeck"
tables = pd.read_html(url)


df_first_table = tables[0]
df_first_table.drop(df_first_table.columns[1], axis=1, inplace=True)

# Hardcoded dictionary for position-specific stats
position_metrics = {
    'Defender': [
        'Progressive Passes',
        'Aerials Won',
        'Interceptions',
        'Pass Completion %',
        'Tackles'
    ]
}


position = 'Defender'
desired_metrics = position_metrics[position]

# Convert DataFrame to dictionary for easier lookup
table_dict = dict(zip(df_first_table[df_first_table.columns[0]], df_first_table[df_first_table.columns[1]]))


values = [float(table_dict[metric]) for metric in desired_metrics]

# Radar plot
labels = desired_metrics
num_vars = len(labels)


angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
values += values[:1]  # repeat first value to close the radar chart
angles += angles[:1]


fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

ax.plot(angles, values, color='red', linewidth=2) 
ax.fill(angles, values, color='red', alpha=0.25) 


ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'])
ax.set_title(f'{position} Profile - Nico Schlotterbeck', size=15, pad=20)

plt.tight_layout()
plt.show()