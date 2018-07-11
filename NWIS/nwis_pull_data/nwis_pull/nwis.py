__author__ = 'rosskush'


import pandas as pd
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen

class pull_data:
	def realtime(siteid,start_date,end_date,param_code):
		    url = f'https://nwis.waterdata.usgs.gov/nwis/uv?cb_{param_code}=on&format=rdb&site_no={siteid}&period=&begin_date={start_date}&end_date={end_date}'
		    print(url)

		    url_file = urlopen(url).readlines()
		    file = []
		    i = 0
		    for line in url_file:
		        file.append(line.decode("utf-8"))
		        i+=1
		        if i > 45: break # assuming the data starts before line 45
		    skip = next(filter(lambda x: x[1].startswith('5s'), enumerate(file))) # find the line that starts with 5s
		    names = file[skip[0]-1].split()
		    df = pd.read_table(url, skiprows=skip[0]+1,names=names)
		    param_col = [item for item in df.columns if (param_code in item)&('cd' not in item)][0]
		    df = df[['datetime',param_col]]
		    df['datetime'] = pd.to_datetime(df['datetime'])
		    return df


