# Import packages
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from urllib.request import urlopen
# get_ipython().run_line_magic('matplotlib', 'notebook')

# Start timer to see how long it takes for your script to run
startTime = datetime.now()

# Function to pull NWIS data from url and save to csv

def pull_nwis_data(parameter, site_number, start_date, end_date, site_name):
    nwis_url = f'https://nwis.waterdata.usgs.gov/nwis/uv?cb_{parameter}=on&format=rdb&site_no={site_number}&period=&begin_date={start_date}&end_date={end_date}'
    print(nwis_url)    

    url_file = urlopen(nwis_url).readlines()
    file = [0]
    i = 0
    for line in url_file:
        file.append(line.decode("utf-8"))
        i+=1
        if i > 50: break # assume data starts before line 50
    skiprows = next(filter(lambda x: x[1].startswith('5s'), enumerate(file))) # find line that begins with 5s
    names = file[skiprows[0]-1].split()
    df = pd.read_table(nwis_url, skiprows = skiprows[0]+1, names=names)
    param_col = [item for item in df.columns if (parameter in item ) & ('cd' not in item)][0]
    df = df[['DateTime', parameter]]
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    return df


    #
    # # Find where in the file the data actually starts and skip rows
    # for sr in range(25, 35):
    #     try:
    #         df = pd.read_table(nwis_url, skiprows=sr)
    #         if df.columns.values[0] == '5s':
    #             break
    #     except:
    #         print('Dormammu I have come to bargain') # Dr. Strange reference anyone?
    #
    # # Rename the columns to something easier to read
    # columns = ['Name', 'Site', 'DateTime', 'Tz', f'{parameter}', 'qual_code']
    # print(columns)
    #
    # # Read the table, skipping the rows
    # df = pd.read_table(nwis_url, skiprows=sr+1, names=columns)
    #
    # # Export to csv with the title you give
    # df.to_csv(f"{site_name}"+'.csv')
    # df['DateTime'] = pd.to_datetime(df['DateTime'])
    # return df

# Call the function to pull NWIS data
parameter = str('00060')
Shoal_Ck_15min = pull_nwis_data(parameter=parameter, site_number='08156800', start_date='2018-02-01', end_date='2018-02-18', site_name='08156800')
Shoal_Ck_15min.head()

# Give the plot a title
site_name='USGS 08156800 Shoal Ck at W 12th St, Austin, TX'

fig, ax = plt.subplots()
x = Shoal_Ck_15min['DateTime']
y = Shoal_Ck_15min[f'{parameter}']
# ax.plot(Shoal_Ck_15min['DateTime'], Shoal_Ck_15min[f'{parameter}']) <--- you could also define your x and y within the ax.plot function

ax.plot(x, y)
plt.xlabel('DateTime')
plt.ylabel('Discharge (cfs): Code '+ f'{parameter}')
# plt.title('USGS 08156800 Shoal Ck at W 12th St, Austin, TX: Discharge') <--- this way works too
plt.title(site_name)
plt.legend()
fig.autofmt_xdate()
fig.tight_layout()

plt.show();


# ## Let's look at the 15 minute data again
parameter = '00060'
Shoal_Ck_15min = pull_nwis_data(parameter=parameter, site_number='08156800', start_date='2018-02-01', end_date='2018-02-18', site_name='08156800')
Shoal_Ck_15min.head(10)

# We can resample the 15 minute data to make it hourly
# this resamples a datetime index to hourly and averages each value within the hour 
Shoal_Ck_hr = Shoal_Ck_15min.resample('h', on=str('DateTime')).mean()
Shoal_Ck_hr.head(10)

# Plot both resolutions together
site_name='USGS 08156800 Shoal Ck at W 12th St, Austin, TX'

fig, ax = plt.subplots()

# 15-minute discharge data
x_15 = Shoal_Ck_15min.index
y_15 = Shoal_Ck_15min[f'{parameter}']
ax.plot(Shoal_Ck_15min['DateTime'], Shoal_Ck_15min[f'{parameter}'], label="15-min interval")

# Hourly discharge data
x_hour = Shoal_Ck_hr.index 
y_hour = Shoal_Ck_hr[f'{parameter}']
ax.plot(Shoal_Ck_hr.index, Shoal_Ck_hr[f'{parameter}'], label="1-hour interval")

# Add necessary features to plot
plt.xlabel('DateTime')
plt.ylabel('Discharge (cfs): Code '+ f'{parameter}')
# plt.title('USGS 08156800 Shoal Ck at W 12th St, Austin, TX: Discharge') <--- this way works too
plt.title(site_name)
plt.legend()
plt.grid()
fig.autofmt_xdate()
fig.tight_layout()
plt.savefig('demo_figure.png')
plt.show();

