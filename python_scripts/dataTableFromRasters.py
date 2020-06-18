# PROGRAM METADATA ******************************************
# Name: dataTableFromRasters.py
# Description: converts raster image files of NRCS easements into data tables 
# Author: Adrian Wiegman (github: arhwiegman, email: adrian.wiegman@gmail.com)
# Institution: University of Vermont
# Date: 2018-06-14
# Notes:
# 	- the program loads python functions from private github repository arhwiegman 
# 	- look up functions using "defLookup(function)" or "functionDictionary[function.__name__]"

# IMPORT MODULES ******************************************
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os, glob, re
from scipy import stats

# DEFINE FUNCTIONS ****************************************
# working directory
wd = "D:\\GISdata\\UVM_Temp\\"
     
os.chdir(os.path.join(wd,"Python_scripts"))
os.chdir('C:\\Users\\Adria\\Documents\\UVM-research\\LCB-Geospatial\\Otter-analysis\\Python_scripts')
exec(open('arcpy_Functions.py','r').read())
#from arcpy_Functions import *

# GLOBAL VARIABLES ****************************************
shpfile = 'D:\\GISdata\\UVM_Temp\\prjdata\\nrcs_wetland_easemts_041618_otter.shp'
gdf = shp2GeoDataFrame(shpfile)
NRCSids = list(gdf['id'])	

# initialize global variables
inpath = os.path.join(wd,"maskeddata") #input file dir
os.chdir(inpath) # set working directory to data folder
filenames = glob.glob(str(51)+'*tif') # folder wd for tifs
M = np.zeros([len(NRCSids),len(filenames)]) # matrix to store data 
# https://pandas.pydata.org/pandas-docs/stable/tutorials.html	
statsdict=[dict()]*len(filenames)

# MAIN PROGRAM*********************************************
k = 0
for i in NRCSids:
	filenames = glob.glob(str(i)+'_*tif')
	#print(i,len(filenames))
	template = str(i)+"_lidardem_adf"
	# warp data to match the intersection of files and use minimum resolution of files, use spatial reference of template
	#ds_list = warplib.memwarp_multi_fn(filenames, extent='intersection', res='min', t_srs=template)
	#get numpy masked array from raster files
	maskedarrays = [rasterioMaskedArray(j) for j in filenames]
	if "NAIP2016" in j plt.imshow(j) for j in filenames
		
	#flatarrays = [np.ma.MaskedArray.flatten(j) for j in maskedarrays]
	#https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#data-with-a-given-value-representing-missing-data
	#store descriptions of maskedarrays 
	#arraystats = [stats.mstats.describe(j) for j in maskedarrays]
	#https://docs.scipy.org/doc/scipy/reference/stats.mstats.html
	#plotRasterPanel(filenames)
	for l in range(len(maskedarrays)):
		print(i,filenames[l],'median',np.ma.median(maskedarrays[l]))
		M[k,l] = np.ma.median(maskedarrays[l])
	#https://docs.scipy.org/doc/numpy/reference/routines.ma.html#masked-arrays-arithmetics
	#statsdict[k]=[{'min':np.ma.min(j),'max':np.ma.max(j),'median':np.ma.median(j),'variance':np.ma.var(j)} for j in maskedarrays]
	#print(statsdict)
	#print(flatarrays)
	k = k + 1
	
print(M)
	
# create data.frame with output matrix	
df = pd.DataFrame(M)
colnames = [n[len(re.split('_',n)[0])+1:len(n)-4] for n in filenames]
df.columns = colnames
df['id'] = NRCSids 
# join data frames on id columns 
output_df = joinDataFramesOnID(df1=gdf,df2=df,ID='id')
output_df.to_csv("D:\\GISdata\\UVM_Temp\\dataframes\\nrcs_wetland_easements_addedData_"+yyyymmdd()+".csv")
