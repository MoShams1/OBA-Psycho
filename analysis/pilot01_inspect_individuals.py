import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------

# /// SET UP SOURCE DATA PATH AND PARAMETERS ///

# beh_file = '0004_20230525_104456_pilot01.json'
# beh_file = '1191_20230525_105707_pilot01.json'
# beh_file = '0012_20230526_104319_pilot01.json'
beh_file = '0006_20230526_111829_pilot01.json'

# set the full path to the raw data
beh_path = os.path.join('..', 'data', 'pilot01', 'raw', beh_file)
df = pd.read_json(beh_path)
# ----------------------------------------------------------------------------

# index correctly responded trials
correct_blue = (df.rel_image == 1) & (df.response == 'right')
correct_red = (df.rel_image == 2) & (df.response == 'left')
correct_trials = correct_blue | correct_red
# index trials of each condition
i_cnd1 = df['condition_num'] == 1
i_cnd2 = df['condition_num'] == 2
i_cnd3 = df['condition_num'] == 3
i_cnd4 = df['condition_num'] == 4
# extract mean rt of each condition
mean_rt_cnd1 = np.round(df.loc[i_cnd1 & correct_trials, 'rt'].mean(), 0)
mean_rt_cnd2 = np.round(df.loc[i_cnd2 & correct_trials, 'rt'].mean(), 0)
mean_rt_cnd3 = np.round(df.loc[i_cnd3 & correct_trials, 'rt'].mean(), 0)
mean_rt_cnd4 = np.round(df.loc[i_cnd4 & correct_trials, 'rt'].mean(), 0)
# calculate error rate in each condition
er_cnd1 = np.round(np.sum(i_cnd1 & (~correct_trials)) / np.sum(i_cnd1) * 100,
                   0)
er_cnd2 = np.round(np.sum(i_cnd2 & (~correct_trials)) / np.sum(i_cnd2) * 100,
                   0)
er_cnd3 = np.round(np.sum(i_cnd3 & (~correct_trials)) / np.sum(i_cnd3) * 100,
                   0)
er_cnd4 = np.round(np.sum(i_cnd4 & (~correct_trials)) / np.sum(i_cnd4) * 100,
                   0)
# ----------------------------------------------------------------------------
# demonstrate RT results
print("==============================================")
print(f"mean rt CND1 (Blue-Cong.): {mean_rt_cnd1} ms")
print(f"mean rt CND2 (Blue-Incong.): {mean_rt_cnd2} ms")
print(f"mean rt CND3 (Red-Cong.): {mean_rt_cnd3} ms")
print(f"mean rt CND4 (Red-Incong.): {mean_rt_cnd4} ms")

fig, axs = plt.subplots(2, 1, figsize=(4, 7))
hist_bins = range(0, 1000, 100)

axs[0].hist(df.loc[i_cnd1 & correct_trials, 'rt'], facecolor='k', alpha=.5,
            bins=hist_bins, label='Blue-Cong.')
axs[0].hist(df.loc[i_cnd2 & correct_trials, 'rt'], facecolor='r', alpha=.5,
            bins=hist_bins, label='Blue-Incong.')
axs[0].set_xticks(range(0, 1000 + 1, 250))
axs[0].set(xticks=range(0, 1000 + 1, 250),
           xlabel='RT [ms]', ylabel='Count',
           xlim=[0, 1000], ylim=[0, 30])
axs[0].legend()

axs[1].hist(df.loc[i_cnd3 & correct_trials, 'rt'], facecolor='k', alpha=.5,
            bins=hist_bins, label='Red-Cong.')
axs[1].hist(df.loc[i_cnd4 & correct_trials, 'rt'], facecolor='r', alpha=.5,
            bins=hist_bins, label='Red-Incong.')
axs[1].set_xticks(range(0, 1000 + 1, 250))
axs[1].set(xticks=range(0, 1000 + 1, 250),
           xlabel='RT [ms]', ylabel='Count',
           xlim=[0, 1000], ylim=[0, 30])
axs[1].legend()

# ----------------------------------------------------------------------------
# demonstrate error rate results
print("==============================================")
print(f"error rate in CND1 (Blue-Cong.): {er_cnd1} %")
print(f"error rate in CND2 (Blue-Incong.): {er_cnd2} %")
print(f"error rate in CND3 (Red-Cong.): {er_cnd3} %")
print(f"error rate in CND4 (Red-Incong.): {er_cnd4} %")

# ----------------------------------------------------------------------------

plt.show()
