# PROGRAM METADATA ========================================
# Name: selectFeatures.py
# Description: select features of an arcgis data file 
# Author: Adrian Wiegman (github: arhwiegman, email: adrian.wiegman@gmail.com)
# Institution: University of Vermont
# Date: 2018-06-19
# Notes:
# - requires arcgis 10.5.0 or later and python 2.7
#==========================================================

# IMPORT MODULES ******************************************
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, glob, re
from scipy import stats

# DEFINE FUNCTIONS ****************************************
# working directory
os.chdir('C:\\Users\\Adria\\Documents\\UVM-research\\LCB-Geospatial\\Otter-analysis\\Python_scripts')
os.chdir('C:\\Temp\\Wiegman_GIS\\')
exec(open('arcpy_Functions.py','r').read())

# MAIN PROGRAM ********************************************
wd = "C:\\Users\\Adria\\Google Drive\\AW_Career\\Education\\UVM\\Research\\NCED Labratory\\NCED_Wetlands_2018\\SampleSites"
wd = 'C:\\Temp\\Wiegman_GIS\\riparianwetlandshapefiles'
os.chdir(wd)
filelist = glob.glob('*.shp')

gdfs = [gpd.read_file(f) for f in filelist]



selected_sites = gdfSelectData(gdf[2],row=gdf[:,'id'==priority_ids],col='id')

arcSplitShapefileByFeature(inDir=wd, inFile='NRCSuvmsoils.shp', outDir=wd, field='Comment')
arcMergeFeatures(wd,['Roch.shp','nrcs_wetland_easemts_041618.shp'],'nrcs_easements_20180619.shp','Roch.shp')	

id = [16,11,23,13,25,4,42,43,45,47,48,43,15,14,40,39,3,52,1]
sql = '"FID" IN ({0})'.format(', '.join(map(str, id)) or 'NULL')
arcSelectAndSaveNew(wd,'nrcs_easements_20180619',"extended_site",sql)
priority_ids = [15,25,45,40,39,16]
sql = '"FID" IN ({0})'.format(', '.join(map(str, priority_ids)) or 'NULL')
arcSelectAndSaveNew(wd,'nrcs_easements_20180619',"priority_sites",sql)
