# merge shapefiles 
# Adrian Wiegman 
# 2018-06-19

# IMPORT MODULES ******************************************
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os, glob, re
from scipy import stats

# DEFINE FUNCTIONS ****************************************
# working directory
os.chdir('C:\\Users\\Adria\\Documents\\UVM-research\\LCB-Geospatial\\Otter-analysis\\Python_scripts')
exec(open('arcpy_Functions.py','r').read())

# MAIN PROGRAM ********************************************
wd = "C:\\Users\\Adria\\Google Drive\\AW_Career\\Education\\UVM\\Research\\NCED Labratory\\NCED_Wetlands_2018\\SampleSites"
os.chdir(wd)
filelist = glob.glob('*.shp')

gdfs = [gpd.read_file(f) for f in filelist]

priority_ids = [14,24,44,39,15]
additional_ids = [45,4,0,47,12,18,22,10,13]

selected_sites = gdfSelectData(gdf[2],row=gdf[:,'id'==priority_ids],col='id')
	
	
 gdf[2][gdf[2][:,'id'==priority_ids],:]
 gdf[2].loc[lambda gdf: gdf['id'] == priority_ids, :]
