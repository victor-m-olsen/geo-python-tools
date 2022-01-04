# Import necessary packages
import os
import pandas as pd

#Setting up directories
project =  r"C:\Users\reach\Desktop\Private\Publication\8-propensity_score\zonal_stats\out2"
# raw = os.path.join(project, 'out2-raw')
# process = os.path.join(project, '02-data-process', 'plots')
os.chdir(project)

# Loading datasets
t = pd.read_csv('comb_17_sample.csv') #, parse_dates=['system:time_start'], index_col=['system:time_start']).rename(columns={'avg_rad':'Sana'})
t18 = pd.read_csv('comb_18_sample.csv')

# Calculate change in agriculture
# create two new columns that are the result of:
# ag17_count-ag16_count
# ag18_count-ag17_count

t['change_2016_2017'] = t['ag17_count'] - t['ag16_count']
t['change_2017_2018'] = t['ag18_count'] - t['ag17_count']
t['change_2016_2018'] = t['ag18_count'] - t['ag16_count']

t18['change_2016_2017'] = t18['ag17_count'] - t18['ag16_count']
t18['change_2017_2018'] = t18['ag18_count'] - t18['ag17_count']
t18['change_2016_2018'] = t18['ag18_count'] - t18['ag16_count']

t['chirps'] = t['ch16-mean']
t18['chirps'] = t18['ch17_mean']

print(t['chirps'])
print(t18['chirps'])

# Getting unique values using set
# print(set(t['layer'].tolist()))

# Setting correct change year as 'change' column

t['change'] = t['change_2016_2017']
# print('change_2016_2017', t['change_2016_2017'])
# print('change', t['change'])

t18['change'] = t18['change_2017_2018']
# print('change_2017_2018', t18['change_2017_2018'])
# print('change', t18['change'])






# print(set(t['layer'].tolist()))
# conflict_sample_17_10k
# non_conflict_sample_17_10k
# conflict_sample_17_5k
# non_conflict_sample_17_5k

# print(set(t18['layer'].tolist()))
#

#set anno
#set km
#set treatment status
#combine into one df
#split in two based on size

t.loc[t.layer == "conflict_sample_17_5k", "treated"] = 1
t.loc[t.layer == "conflict_sample_17_10k", "treated"] = 1
t.loc[t.layer == "non_conflict_sample_17_5k", "treated"] = 0
t.loc[t.layer == "non_conflict_sample_17_10k", "treated"] = 0

t.loc[t.layer == "conflict_sample_17_5k", "km"] = 5
t.loc[t.layer == "conflict_sample_17_10k", "km"] = 10
t.loc[t.layer == "non_conflict_sample_17_5k", "km"] = 5
t.loc[t.layer == "non_conflict_sample_17_10k", "km"] = 10

t.loc[t.layer == "conflict_sample_17_5k", "anno"] = 17
t.loc[t.layer == "conflict_sample_17_10k", "anno"] = 17
t.loc[t.layer == "non_conflict_sample_17_5k", "anno"] = 17
t.loc[t.layer == "non_conflict_sample_17_10k", "anno"] = 17


t18.loc[t18.layer == "conflict_sample_18_5k", "treated"] = 1
t18.loc[t18.layer == "conflict_sample_18_10k", "treated"] = 1
t18.loc[t18.layer == "non_conflict_sample_18_5k", "treated"] = 0
t18.loc[t18.layer == "non_conflict_sample_18_10k", "treated"] = 0

t18.loc[t18.layer == "conflict_sample_18_5k", "km"] = 5
t18.loc[t18.layer == "conflict_sample_18_10k", "km"] = 10
t18.loc[t18.layer == "non_conflict_sample_18_5k", "km"] = 5
t18.loc[t18.layer == "non_conflict_sample_18_10k", "km"] = 10

t18.loc[t18.layer == "conflict_sample_18_5k", "anno"] = 18
t18.loc[t18.layer == "conflict_sample_18_10k", "anno"] = 18
t18.loc[t18.layer == "non_conflict_sample_18_5k", "anno"] = 18
t18.loc[t18.layer == "non_conflict_sample_18_10k", "anno"] = 18


#
# print(t['km'])
# print(t18['km'])

combined = pd.concat([t, t18])

#combined.to_csv('combined.csv')

sample_5km = combined[combined['km'] == 5]
sample_10km = combined[combined['km'] == 10]


print(sample_5km)
print(sample_10km)

sample_5km.to_csv('sample_5km.csv')
sample_10km.to_csv('sample_10km.csv')

#sample_5km.to_csv('sample_5km.csv')
#sample_10km.to_csv('sample_10km.csv')


    # if row['layer'] == 'conflict_sample_17_10k':
    #     row['treated'] = 1

# print(t['treated'])

#
# t['treated'] = 1
#
#
#
# t18['treated'] = t18['ag18_count'] - t18['ag16_count']









# t.loc[t['layer'] == 'conflict_sample_17_10k']
#
# print(t.loc[t['layer'] == 'conflict_sample_17_10k'])
#


# print('ag18_count', t['ag18_count'])
# print('ag17_count', t['ag17_count'])
# print('change_2017_2018', t['change_2017_2018'])

# print('ag17_count', t['ag17_count'])
# print('ag16_count', t['ag16_count'])
# print('change_2016_2017', t['change_2016_2017'])
