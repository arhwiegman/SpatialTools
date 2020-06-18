# PROGRAM VITALS ============================================
# Name: arcpy_main.py
# Description: executes geospatial analysis with arcpy (ESRI API)
# Author: Adrian Wiegman (github: arhwiegman, email: adrian.wiegman@gmail.com)
# Institution: University of Vermont
# Date: 2018-06-14
# Notes:
# 	- requires arcMAP 10.5.0 or later (arcpy and arcpy.sa packages)
# 	- the program loads python functions from private github repository arhwiegman 
# 	- look up functions using "defLookup(function)" or "functionDictionary[function.__name__]"
# 	- arcpy functions start with "arc" spatial analysist hydrology functions start with "archy"
# ============================================================

# PROJECT OBJECTIVES ***************************************
#1. Download GIS data from web repositories
#	10m elevation
#	NAIP Imagery (2016,2001)
#	National Croplands Data-layer (2016,2001)
#
#3. For each raster data source
#	a. Re-project data to 'EPSG:26918'
#	b. Join raster files
#	c. Mask rasters with shapefiles for a HUC8 subbasin
#	d. Mask rasters with shapefiles for NRCS easements
#	
#4. With elevation
#	a. fill sinks
#	b. calculate flow direction
#	c. calculate flow accumulation (upslope contributing area)
#	c. calculate wetness index (accumulation divided by slope)
#		
#4. For each NRCS easement calculate
#	a. upslope area from pour points in river
#	b. percent agriculture or corn draining to pour points
#		- extract number of cells in upslope area
#		- extract number of cells in upslope area equal to corn 
#	c. scipy.stats.describe wetness index
#	d. NDVI 2008 and 2016
	
#5. Append NRCS easement attribute table with the following:


# IMPORT MODULES ***********************************************
import requests, arcpy, os, glob, re, sys
import pandas as pd
import numpy as np
import scipy.stats

# GLOBAL VARIABLES ****************************************
# working directory
wd = "C:\\GISdata\\UVM_Temp\\"
# NRCS easement id codes
id = [0,1,2,3,4,5,10,12,13,14,15,16,17,18,20,21,22,24,25,39,40,41,42,43,44,45,46,47,48,49,51,52,57]

# USER DEFINED FUNCTIONS ***************************************
# download functions arcpy_Functions.py from github
# if running entire script make sure main and functions are in same directory
# set the current directory to folder containing function script
os.chdir(os.path.join(wd,"Python_scripts"))
# if you need to download arcpy_Functions.py then use code in block quotes below 
from arcpy_Functions import*
defLookup() #lookup defined functions code with defLookup
'''
# gitSaveRaw ----------------------------------
# saves raw text from git hib url
def gitSaveRaw(rawURL=None,filepath=None):
	import re, requests, os
	if rawURL is None:
		rawURL= "https://raw.githubusercontent.com/arhwiegman/UVM-research/master/LCB-Geospatial/Otter-analysis/Python_scripts/arcpy_Functions.py?token=AfPESkqBox4-kodP_LcWwWPz-rF-aAdcks5bF_gYwA%3D%3D"
	name = re.match(".*/([\S^/]+)\?.*",rawURL).group(1)
	if filepath is None: 
		filepath = os.getcwd() + "/" + name
	
	# ask user before overwriting an existing file
	Q = None
	if os.path.exists(filepath):
		Q = input(filepath+" already exists: type 'Yes' to overwrite, press any key to abort")
	if Q != "Yes": 
		print("aborting function gitSaveRaw")
		return
		
	# get text from the URL and write to file
	r = requests.get(rawURL)	
	f = open(filepath,'w')
	f.seek(0)	
	f.write(r.text)
	f.close
gitSaveRaw()

# gitRunScript ---------------------------------------------------------
# downloads a python script from raw text on git hub and executes the file
def gitRunScript(rawURL=None):
	import requests
	if rawURL is None: 
		rawURL= "https://raw.githubusercontent.com/arhwiegman/UVM-research/master/LCB-Geospatial/Otter-analysis/Python_scripts/arcpy_Functions.py?token=AfPESkqBox4-kodP_LcWwWPz-rF-aAdcks5bF_gYwA%3D%3D"
	r = requests.get(rawURL)
	exec(r.text)
'''
from arcpy_Functions import*
defLookup() #lookup defined functions code with defLookup


# MAIN PROGRAM ********************************************

# 1. MOSAIC AND RESAMPLE RASTERS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# manage directories
arcWorkspace(wd) # sets os.cwd() and arcpy.env.workspace to wd
I1 = wd + "rawdata\\" # input data folder (I1)
if not os.path.exists(I1): sys.exit("error "+I+" does not exist") 
O1 = wd + "outdata1\\" # output data folder for objective 1 (O1)
if os.path.exists(O1):
	sys.exit(O1+"already exists, remove it from this directory to proceed")
else: 
	os.mkdir(O1)

# blocks of commented code have been completed 
'''
# 1.1 LIDAR HyDEM...............................................
# mosaic selected raster files 
# 2013 0.7m lidar dem: Rutland county otter creek
arcWorkspace(wd) 
data = glob.glob(I1+"Elev*RVT*.img")
out = arcMosaic2NewRaster(data,outPath=O1,outName='dem0p7mRVT')
del out

# 2012 1.6m lidar dem: Addision county along otter creek
arcWorkspace(wd)
data = glob.glob(I1+"Elev*AVT*.img")
out = arcMosaic2NewRaster(data,outPath=O1,outName='dem1p6mAVT')
del out 

# resample rasters to specified resolution
arcWorkspace(O1) # reset workspace
# verify coordinate reference systems are the same
CRSname1 = arcpy.Describe("dem0p7mRVT").spatialReference.name
CRSname2 = arcpy.Describe("dem1p6mAVT").spatialReference.name
cellsizeY = arcpy.GetRasterProperties_management("dem1p6mAVT", "CELLSIZEY")
cellsizeX = arcpy.GetRasterProperties_management("dem1p6mAVT", "CELLSIZEY")
# cell size: 1.59999999999998
arcWorkspace(wd) 
out = arcpy.Resample_management("dem0p7mRVT","dem1p6mRVT",1.59999999999998,"CUBIC")
data = [I1+"dem1p6mAVT",I1+"dem1p6mRVT"]
out = arcMosaic2NewRaster(data,outPath=O1,outName="dem1p6mOtter")
del out 

# 1.2 NAIP RGB+NIR IMAGERY...................................
# mosaic selected raster files 
# 2016 NAIP IMAGERY
arcWorkspace(wd) 
data = glob.glob(I1+"*2016*.jp2")
arcpy.GetRasterProperties_management(data[1], "BANDCOUNT")
# <Result '4'>
out = arcpy.MosaicToNewRaster_management(data,O1,'NAIP2016.tif',number_of_bands=4,mosaic_method="FIRST",mosaic_colormap_mode="MATCH",cellsize=3)
del out
# 2008 NAIP IMAGERY
arcWorkspace(wd) 
data = glob.glob(I1+"*2008*.jp2")
arcpy.GetRasterProperties_management(data[1], "BANDCOUNT")
#out = arcMosaic2NewRaster(data[:3],outPath=O1,outName='NAIP2008',outExt='.tif',nbands=4)
out = arcpy.MosaicToNewRaster_management(data,O1,'NAIP2008.tif',number_of_bands=4,mosaic_method="FIRST",mosaic_colormap_mode="MATCH",cellsize=3)
#os.path.getsize
del out

#%^&*@#$@%^&#@#^*@#$^ SOMETHING WRONG WITH NAIP IMAGERY
query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()
'''
'''
# 2. REPROJECT DATA TO EPSG 26918 >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

# create new output folder for objective 2  
O2 = wd+"outdata1\\" 

if os.path.exists(O2):
	sys.exit(O2+"already exists, remove it from this directory to proceed")
else: 
	os.mkdir(O2)
arcWorkspace(O2)


# select data files for batch
# append rasters
dataList = list("n") # initialize list with one character because of error in list flattening
dataList.append(glob.glob(I1+"elev*adf")) #  10m elevation 
dataList.append(glob.glob(I1+"flowacc*")) # 10m flow accumulation
dataList.append(glob.glob(I1+"flowdir*")) # 10m flow direction
dataList.append(glob.glob(I1+"cdl*.tif")) # USDA croplands data layer 2008-2017
dataList.append(glob.glob(I1+"Geol*.tif")) # NRCS web soil survey
dataList.append(glob.glob(I1+"nlcd*.tif"))# USDA National land cover dataset
dataList.append(glob.glob(O1+"dem*otter"))# 1.6m Lidar DEM
dataList.append(glob.glob(O1+"NAIP*.tif"))# 3m 4band color imagery 
# append vectors  
dataList.append(glob.glob(I1+"nrcs_wetl*.shp")) # polygons for NRCS restoration sites
dataList.append(glob.glob(I1+"nrcs_pour*.shp")) # points in otter creek next to NRCS sites
dataList.append(glob.glob(I1+"Otter*.shp")) # HUC8 boundary of the otter creek watershed
batch = list(itertools.chain.from_iterable(dataList)) #flatten the list
batch.pop(0) # remove first list item

tifs = glob.glob("*.tif") # all '.tif' files
#adfs = [re.match("^[^.]+$",f).group(0) for f in os.listdir(O2)] # arc binary grid , anything without "."
adfs = glob.glob("*_adf") 
shps = glob.glob("*.shp")
batch = tifs + adfs + shps

CRS = arcpy.SpatialReference(26918) #NAD83 UTM Zone 18
#defLookup(arcReprojectBatch) # look up function 
arcReprojectBatch(O2,batch,CRS)
# other spatial references:
# albers equal area conic https://epsg.io/102008#
# WGS84 UTM Zone 18N https://epsg.io/32618
# NAD83 UTM Zone 18N https://epsg.io/26918
# http://pro.arcgis.com/en/pro-app/arcpy/classes/spatialreference.htm

#
query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()
'''


'''
# 3. EXTRACT DATA MASKED TO NRCS EASEMENT BOUNDARIES >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# create new output folder for objective 3  
I3 = os.path.join(wd,"prjdata")
O3 = os.path.join(wd,"maskeddata")
if os.path.exists(O3):
	sys.exit(O3+"already exists, remove it from this directory to proceed")
else: 
	os.mkdir(O3)
arcWorkspace(O3)

# split NRCS easements by feature 'id' the unique identifier for each NRCS site
maskpath = os.path.join(O3+"easements_id")
# writeMetadata(maskpath) #need to debug


#arcSplitShapefileByFeature(inDir = I3,inFile="nrcs_wetland_easemts_041618_otter.shp",outDir = maskpath,field="id")


# select masks, nrcs easements polygons saved by id
masks = glob.glob(os.path.join(maskpath,"*.shp"))

# select raster files 
tifs = glob.glob(os.path.join(I3,"*.tif")) # all '.tif' files
#adfs = [re.match("^[^.]+$",f).group(0) for f in os.listdir(O2)] # arc binary grid , anything without "."
adfs = glob.glob(os.path.join(I3,"*_adf"))
batch = tifs + adfs

# select masks for each NRCS easement site by id
for i in id:
	msk = os.path.join(maskpath,str(i)+".shp")
	print(msk)
	print(i)
	
	# extract by mask and save raster batch 
	for rst in batch:
		name = os.path.splitext(os.path.basename(rst))[0]
		arcExtractRasterByMask(rst,msk,outpath=O3,outname=str(i)+"_"+name,ext='.tif')# select masks for each NRCS easement site by id

query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()
	


	
# 4. SUMMARIZE DATA INSIDE EACH NRCS EASEMENT >>>>>>>>>>>>>>>>>>>>>>>>
# create a data table with summary variables for each easement
from osgeo import gdal
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

I4 = os.path.join(wd,"maskeddata") #input file dir
os.chdir(I4)
filenames = glob.glob('*tif')
for n in filenames:  

		f = gdal.Open(n) # open file with gdal library
		if 'NAIP' in n: 
			red = f.GetRasterBand(1).ReadAsArray()
			blu = f.GetRasterBand(2).ReadAsArray()
			grn = f.GetRasterBand(3).ReadAsArray()
			nir = f.GetRasterBand(4).ReadAsArray()
			red = red.astype(np.float64)
			nir = nir.astype(np.float64)
			array = osgNDVI(red,nir)
		else:
			array = f.GetRasterBand(1).ReadAsArray()
		values = np.extract(array)
		stats = scipy.stats.describe(values)
		plt.imshow(array)
		plt.colorbar(array)
		


query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()





	

 # !!!!!!!!!!!!!!!!!!!!!!!!!!
 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 # ROUTINE TO MERGE SUMMARY OF RASTER DATA BACK INTO SHAPE FILE
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
 
		
		

# plotRasterPanel ----------------------------------------------------
# plots raster list of data in figure panel of with default 3 column layout
def plotRasterPanel(filelist, Ncol=3, clim=None, titles=None, cmap='inferno', label=None, overlay=None, fn=None):
	import rasterio
	import numpy as np
	import matplotlib.pyplot as plt
	
   raster_list = [rasterio.open(f).read() for f in filenames]
	Nrow = int(round((len(raster_list())/X),0))
   fig, axa = plt.subplots(Nrow,Ncol, sharex=True, sharey=True, figsize=(10,5))
    alpha = 1.0
    for n, ax in enumerate(axa):
        #Gray background
        ax.set_facecolor('0.5')
        #Force aspect ratio to match images
        ax.set(adjustable='box-forced', aspect='equal')
        #Turn off axes labels/ticks
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if titles is not None:
            ax.set_title(titles[n])
        #Plot background shaded relief map
        if overlay is not None:
            alpha = 0.7
            axa[n].imshow(overlay[n], cmap='gray', clim=(1,255)) 
    #Plot each array 
    im_list = [axa[i].imshow(raster_list[i], clim=clim, cmap=cmap, alpha=alpha) for i in range(len(raster_list))]
    fig.tight_layout()
    fig.colorbar(im_list[0], ax=axa.ravel().tolist(), label=label, extend='both', shrink=0.5)
    if fn is not None:
        fig.savefig(fn, bbox_inches='tight', pad_inches=0, dpi=150)
    r.close() for r in raster_list		
		
selecteddata = ["NAIP2016","Q1p5","cdl*2008"]
filenames = [glob.glob(s+'*tif') for s in selecteddata] # folder wd for tifs


print("PROGRAM COMPLETED!!!")
'''



gdal_merge(
