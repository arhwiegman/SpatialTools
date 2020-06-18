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
from arcpy_Functions import *

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

print(df)
print(M)
# MAIN PROGRAM*********************************************
for i in NRCSids[:2]:
	k = k + 1
	filenames = glob.glob(str(i)+'*tif')
	template = str(i)+"_lidardem_adf"
	# warp data to match the intersection of files and use minimum resolution of files, use spatial reference of template
	#ds_list = warplib.memwarp_multi_fn(filenames, extent='intersection', res='min', t_srs=template)
	#get numpy masked array from raster files
	maskedarrays = [rasterioMaskedArray(j) for j in filenames]
	flatarrays = [np.ma.MaskedArray.flatten(j) for j in maskedarrays]
	#https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#data-with-a-given-value-representing-missing-data
	#store descriptions of maskedarrays 
	arraystats = [stats.mstats.describe(j) for j in maskedarrays]
	#https://docs.scipy.org/doc/scipy/reference/stats.mstats.html
	#plotRasterPanel(filenames)
	for l in range(len(maskedarrays)):
		print(i,filenames[l],'median',np.ma.median(maskedarrays[l]))
		M[k,l] = np.ma.median(maskedarrays[l])
	#https://docs.scipy.org/doc/numpy/reference/routines.ma.html#masked-arrays-arithmetics
	statsdict[i]=[{'min':np.ma.min(j),'max':np.ma.max(j),'median':np.ma.median(j),'variance':np.ma.var(j)} for j in maskedarrays]
	print(statsdict)
	print(flatarrays)

# create data.frame with output matrix	
df = pd.DataFrame(M)
colnames = [n[len(re.split('_',n)[0])+1:len(n)-4] for n in filenames]
df.columns = colnames
df['id'] = NRCSids 
# join data frames on id columns 
output_df = joinDataFramesOnID(df1=gdf,df2=df,ID='id')
output_df.to_csv("nrcs_wetland_easements_addedData_"+yyyymmdd())
