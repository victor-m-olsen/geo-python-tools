# Import necessary packages
import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing

#Setting up directories
project =  r"C:\\Users\\reach\\Desktop\\Private\\Publication\\4-geodata\\CHIRPS_time_series"
#raw = os.path.join(project, '01-data-raw')
#process = os.path.join(project, '02-data-process', 'plots')
os.chdir(project)

# Loading datasets
chirps = pd.read_csv('CHIRPS_TS.csv', parse_dates=['system:time_start'], index_col=['system:time_start']) #.rename(columns={'avg_rad':'Sana'})

# Resampling to weekly or monthly ('M')
chirps = chirps.resample('W').sum()

chirps.plot()
plt.show()
