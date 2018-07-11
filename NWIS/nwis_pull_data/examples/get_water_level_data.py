__author__ = 'rosskush'

# In this simmple example, we will feed the USGS site ID, date ranges, and the param code to retrieve a dataframe 

import os
import sys
sys.path.append(os.path.join('..','nwis_pull')) # from https://github.com/rosskush/nwis_pull
import nwis_pull as nwis

df = nwis.pull_data.realtime('212305157542601','2017-12-01','2017-12-28','72150')
print(df.head())

# plotting

columns = df.columns

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
ax.plot(df['datetime'],df[columns[-1]])
ax.grid()


plt.show()
