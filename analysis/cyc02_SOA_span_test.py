import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------

# /// SET UP SOURCE DATA PATH AND PARAMETERS ///

# data = 'AB01_soa_20230628_123805.json'
data = '0012_soa_20230710_114003.json'

# set the full path to the raw data
beh_path = os.path.join('..', 'data', 'cyc02', data)
df = pd.read_json(beh_path)

result_path = os.path.join('..', 'result', 'cyc02')

# ----------------------------------------------------------------------------

# /// MODIFY DATA ///

# convert absolute ms values to actual ones
df.loc[df['soa_cnd'] < 0, 'soa_ms'] = -df['soa_ms']

# create the x axis from all SOAs
soa_array = np.sort(df['soa_cnd'].unique())

# take the input responses out of the list
df['response'] = df['response'].str[0]

# create an array of response evaluation
right_resp = df['response'] == 'right'

# ----------------------------------------------------------------------------

# /// CALCULATE ACCURACY AT EACH SOA ///
acc = np.full(len(soa_array), np.nan)
for isoa, soa in enumerate(soa_array):
    selected_rows = df.loc[df['soa_cnd'] == soa].index
    total_rows = len(selected_rows)
    # print(total_rows)
    n_correct = (right_resp[selected_rows] == 1).sum()
    acc[isoa] = (n_correct / total_rows) * 100

# ----------------------------------------------------------------------------

# convert the SOA array to ms
soa_array_ms = np.round(np.sort(df['soa_cnd'].unique()) * 1000 / 60)

fig, ax = plt.subplots()
ax.plot(soa_array * 1000 / 60, acc, '-ko')

ax.set(xlabel='SOA (ms)', ylabel='Report of right appearing first (%)',
       ylim=[-2, 102])

plt.tight_layout()
plt.savefig(os.path.join(result_path, f'soa_test_{data[:4]}.pdf'))
