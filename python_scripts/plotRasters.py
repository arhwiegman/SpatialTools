# IMPORT MODULES ******************************************
import numpy as np
import matplotlib.pyplot as plt
import os, glob
from scipy import stats

# DEFINE FUNCTIONS ****************************************
# working directory
wd = "D:\\GISdata\\UVM_Temp\\"
os.chdir(os.path.join(wd,"Python_scripts"))
from arcpy_Functions import *

# GLOBAL VARIABLES ****************************************
NRCSids = [0,1,2,3,4,5,10,12,13,14,15,16,17,18,20,21,22,24,25,39,40,41,42,43,44,45,46,47,48,49,51,52,57]
# initialize global variables
inpath = os.path.join(wd,"maskeddata") #input file dir
os.chdir(inpath) # set working directory to data folder
filenames = glob.glob('51*tif') # filder wd for tifs

# MAIN PROGRAM*********************************************
for i in NRCSids[:1]:
	filenames = glob.glob(str(i)+'*NAIP*tif')
	template = str(i)+"_lidardem_adf"
	# warp data to match the intersection of files and use minimum resolution of files, use spatial reference of template
	#ds_list = warplib.memwarp_multi_fn(filenames, extent='intersection', res='min', t_srs=template)
	#get numpy masked array from raster files
	maskedarrays = [rasterioMaskedArray(f) for f in filenames]
	flatarrays = [ma.x.flatten(ma) for x in maskedarrays]
	#https://docs.scipy.org/doc/numpy/reference/maskedarray.generic.html#data-with-a-given-value-representing-missing-data
	#store descriptions of maskedarrays 
	arraystats = [scipy.stats.mstats.describe(ma) for ma in maskedarrays]
	#https://docs.scipy.org/doc/scipy/reference/stats.mstats.html
	#plotRasterPanel(filenames)
	for j in range(len(maskedarrays)):
		print(i,filenames[j],'min',np.ma.median(maskedarrays[j]))
	#https://docs.scipy.org/doc/numpy/reference/routines.ma.html#masked-arrays-arithmetics
	statsdict=[{'min':np.ma.min(j),'max':np.ma.max(j),'median':np.ma.median(j),'variance':np.ma.var(j)}]
	
	

		

