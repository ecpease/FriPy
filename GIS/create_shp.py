import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import os

masterDF = pd.read_excel('Clearwater_SiteInformation.xlsx')
masterDF.dropna(subset=['Longitude', 'Latitude'],inplace=True)
masterDF['geometry'] = masterDF.apply(lambda xy: Point(xy['Longitude'],xy['Latitude']),axis=1)
masterDF = masterDF[['geometry', 'StationNo', 'SiteName', 'SiteType', 'WellNo', 'GeologicUnit', 'Aquifer']]
proj4 = '+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs'
masterDF = gpd.GeoDataFrame(masterDF,geometry='geometry' ,crs=proj4)
masterDF.to_file(os.path.join('shapefile', 'ClearwaterSites.shp'))