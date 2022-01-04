# Import necessary packages
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing


#Setting up directories
project =  "D:\\02_Portfolios\\00_Other\\03_NightLight\\"
raw = os.path.join(project, '01-data-raw')
process = os.path.join(project, '02-data-process', 'plots')
os.chdir(process)

# Loading datasets
Sana = pd.read_csv('sana.csv', parse_dates=['system:time_start'], index_col=['system:time_start']).rename(columns={'avg_rad':'Sana'})
Aden = pd.read_csv('aden.csv', parse_dates=['system:time_start'], index_col=['system:time_start']).rename(columns={'avg_rad':'Aden'})
Marib = pd.read_csv('marib.csv', parse_dates=['system:time_start'], index_col=['system:time_start']).rename(columns={'avg_rad':'Marib'})
admin0 = pd.read_csv('admin0.csv', parse_dates=['system:time_start'], index_col=['system:time_start']).rename(columns={'avg_rad':'admin0'})


# Adding columns to combined df
df = Sana.assign(Aden = Aden['Aden']).assign(Marib = Marib['Marib']).assign(admin0 = admin0['admin0'])
print(df.head())


### Simple plotting
# df.drop(['admin0'], axis=1).plot()
# plt.show()


# print(df.columns)
# print(df.head())
# print(df.describe())
# print(df.dtypes)
# print(df.index)


# copy the data
df_max_scaled = df.copy()



# apply normalization techniques
column = 'Sana'
df_max_scaled[column] = df_max_scaled[column] /df_max_scaled[column].abs().max()

column = 'Aden'
df_max_scaled[column] = df_max_scaled[column] /df_max_scaled[column].abs().max()

column = 'Marib'
df_max_scaled[column] = df_max_scaled[column] /df_max_scaled[column].abs().max()

column = 'admin0'
df_max_scaled[column] = df_max_scaled[column] /df_max_scaled[column].abs().max()





### Plotting with a subplot
plot_df = df_max_scaled.drop(['admin0'], axis=1)

fig, ax = plt.subplots(figsize=(14, 9))

ax.plot(plot_df)
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Normalized Night Light', fontsize=12)
ax.legend()
fig.suptitle('Night Light Trends', fontsize=22)

sana_label, = plt.plot(df_max_scaled['Sana'], label='Sana', color='dodgerblue')
aden_label, = plt.plot(df_max_scaled['Aden'], label='Aden', color='Orange')
marib_label, = plt.plot(df_max_scaled['Marib'], label='Marib', color='forestgreen')

plt.legend(handles=[sana_label, aden_label, marib_label])

fig.savefig('fig9.jpg')
plt.show()





















#### NORMALIZING THE DATA ####
#
#
# # Create x, where x the 'scores' column's values as floats
# x = df2[['avg_rad']].values.astype(float)
#
# # Create a minimum and maximum processor object
# min_max_scaler = preprocessing.MinMaxScaler()
#
# # Create an object to transform the data to fit minmax processor
# x_scaled = min_max_scaler.fit_transform(x)
#
# # Run the normalizer on the dataframe
# avg_rad_norm = pd.DataFrame(x_scaled)
#
# print(avg_rad_norm)
#
# df2 = df.assign(avg_rad_norm = avg_rad_norm)
#
# print(df2.head())
#
#
#
#
#
# # Normalize time series data
# from pandas import read_csv
# from sklearn.preprocessing import MinMaxScaler
# # load the dataset and print the first 5 rows
# series = read_csv('daily-minimum-temperatures-in-me.csv', header=0, index_col=0)
# print(series.head())
# # prepare data for normalization
# values = series.values
# values = values.reshape((len(values), 1))
# # train the normalization
# scaler = MinMaxScaler(feature_range=(0, 1))
# scaler = scaler.fit(values)
# print('Min: %f, Max: %f' % (scaler.data_min_, scaler.data_max_))
# # normalize the dataset and print the first 5 rows
# normalized = scaler.transform(values)
# for i in range(5):
# 	print(normalized[i])
# # inverse transform and print the first 5 rows
# inversed = scaler.inverse_transform(normalized)
# for i in range(5):
# 	print(inversed[i])
#
#
#
#
#
# #
# # # Create x, where x the 'scores' column's values as floats
# # x = df2[['address']].values.astype(float)
# #
# # # Create a minimum and maximum processor object
# # min_max_scaler = preprocessing.MinMaxScaler()
# #
# # # Create an object to transform the data to fit minmax processor
# # x_scaled = min_max_scaler.fit_transform(x)
# #
# # # Run the normalizer on the dataframe
# # df_normalized = pd.DataFrame(x_scaled)
# #
# # print(df_normalized)
# #
# #
# # df2 = df.assign(df_normalized = df_normalized)
# #
# #
# # print(df2.head())
