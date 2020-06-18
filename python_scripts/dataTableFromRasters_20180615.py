<<<<<<< HEAD
# PROGRAM METADATA ******************************************
# Name: dataTableFromRasters.py
# Description: converts raster image files of NRCS easements into data tables 
# Author: Adrian Wiegman (github: arhwiegman, email: adrian.wiegman@gmail.com)
# Institution: University of Vermont
# Date: 2018-06-14
# Notes:
# 	- the program loads python functions from private github repository arhwiegman 
# 	- look up functions using "defLookup(function)" or "functionDictionary[function.__name__]"

# IMPORT MODULES ***********************************************
import requests, os, glob, re, sys
import pandas as pd
import numpy as np
import scipy.stats

# GLOBAL VARIABLES ****************************************
# working directory
wd = "D:\\GISdata\\UVM_Temp\\"
NRCSids = [0,1,2,3,4,5,10,12,13,14,15,16,17,18,20,21,22,24,25,39,40,41,42,43,44,45,46,47,48,49,51,52,57]
# NRCS easement id codes

# USER DEFINED FUNCTIONS ***************************************
# download functions arcpy_Functions.py from github
# if running entire script make sure main and functions are in same directory
# set the current directory to folder containing function script
os.chdir(os.path.join(wd,"Python_scripts"))
from arcpy_Functions import*

defLookup() #lookup defined functions code with defLookup

# gdalRaster2List -------------------------------------------------
# reads a raster file with gdal and returns a list of values
# name is a string containing the name of the data source raster 
# "myraster.tif"
def gdalRaster2List(name):
	from osgeo import gdal
	import numpy as np
	f = gdal.Open(name) # open file with gdal library
	if 'NAIP' in name: # calculate NDVI from NAIP imagery
    	red = f.GetRasterBand(1).ReadAsArray()
		blu = f.GetRasterBand(2).ReadAsArray()
		grn = f.GetRasterBand(3).ReadAsArray()
		nir = f.GetRasterBand(4).ReadAsArray()
		red = red.astype(np.float64)
		nir = nir.astype(np.float64)
		array = osgNDVI(red,nir)
	else:
		array = f.GetRasterBand(1).ReadAsArray()
		array = array.astype(np.float64)
	return(array.flatten().tolist())


# 4. SUMMARIZE DATA INSIDE EACH NRCS EASEMENT >>>>>>>>>>>>>>>>>>>>>>>>
# create a long format data table with summary variables for each easement


from osgeo import gdal
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

# initialize global variables
I4 = os.path.join(wd,"maskeddata") #input file dir
os.chdir(I4) # set working directory to data folder
filenames = glob.glob('*tif') # filder wd for tifs

idtable = dict() # create dictionary to store ids
valuetable = list() # create dictionary to store data

# open output file
open("outdata.csv",'w')

# start loop for files
id = "aaa"
V = [""]*(len(NRCSids)) # initialize empty list to store values
I = [""]*(len(NRCSids)) # initialize empty list to store id names
datanames = [""]*28
j = -1
i = 0
for name in filenames:
	m = re.split("_",name) # id value at beginning of filename
	if m[0] != id: # reset i if id is different from the match
		i = 0
		id = m[0]
		j = j + 1
	dataname = name[len(m[0])+1:len(name)-4]
	print('i=',i,'j=',j,'id=',id,'name=',name,'dataname=',dataname)
	values = gdalRaster2List(name) # get flat list of values from array
	ids = [id]*len(values)
	datanames[i] = dataname
	print(len(values))
    if j == 0: 
		V[i] = values
		print(values)
		I[i] = ids
	else:
		V[i].extend(values)
		I[i].extend(ids)
	i = i + 1
	statsdict[dataname] = 
	datadict[dataname] = [V[i],I[i]]

	
## STILLL NOT QUITE RIGHT
	
d = dict()
for i in range(len(datanames)):
	dn = datanames[i]
	print(i,dn+'.csv')
	
	df = pd.DataFrame([V[i],I[i]])
	df.to_csv(dn+'.csv',sep=',')

	

	

	
	
	
	

	
	
	


'''	
		
    # A list or 1d array of values
	value[i] = array.flatten() # numpy
	ids[i] = [id]*len(values) 
	
	stats = scipy.stats.describe(values)
	plt.imshow(array)
	plt.colorbar(array)
		


query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()
=======
# PROGRAM METADATA ******************************************
# Name: dataTableFromRasters.py
# Description: converts raster image files of NRCS easements into data tables 
# Author: Adrian Wiegman (github: arhwiegman, email: adrian.wiegman@gmail.com)
# Institution: University of Vermont
# Date: 2018-06-14
# Notes:
# 	- the program loads python functions from private github repository arhwiegman 
# 	- look up functions using "defLookup(function)" or "functionDictionary[function.__name__]"

# IMPORT MODULES ***********************************************
import requests, os, glob, re, sys
import pandas as pd
import numpy as np
import scipy.stats

# GLOBAL VARIABLES ****************************************
# working directory
wd = "D:\\GISdata\\UVM_Temp\\"
NRCSids = [0,1,2,3,4,5,10,12,13,14,15,16,17,18,20,21,22,24,25,39,40,41,42,43,44,45,46,47,48,49,51,52,57]
# NRCS easement id codes

# USER DEFINED FUNCTIONS ***************************************
# download functions arcpy_Functions.py from github
# if running entire script make sure main and functions are in same directory
# set the current directory to folder containing function script
os.chdir(os.path.join(wd,"Python_scripts"))
from arcpy_Functions import*

defLookup() #lookup defined functions code with defLookup

# gdalRaster2List -------------------------------------------------
# reads a raster file with gdal and returns a list of values
# name is a string containing the name of the data source raster 
# "myraster.tif"
def gdalRaster2List(name):
	from osgeo import gdal
	import numpy as np
	f = gdal.Open(name) # open file with gdal library
	if 'NAIP' in name: # calculate NDVI from NAIP imagery
    	red = f.GetRasterBand(1).ReadAsArray()
		blu = f.GetRasterBand(2).ReadAsArray()
		grn = f.GetRasterBand(3).ReadAsArray()
		nir = f.GetRasterBand(4).ReadAsArray()
		red = red.astype(np.float64)
		nir = nir.astype(np.float64)
		array = osgNDVI(red,nir)
	else:
		array = f.GetRasterBand(1).ReadAsArray()
		array = array.astype(np.float64)
	return(array.flatten())


# 4. SUMMARIZE DATA INSIDE EACH NRCS EASEMENT >>>>>>>>>>>>>>>>>>>>>>>>
# create a long format data table with summary variables for each easement


from osgeo import gdal
import rasterio
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats

# initialize global variables
I4 = os.path.join(wd,"maskeddata") #input file dir
os.chdir(I4) # set working directory to data folder
filenames = glob.glob('*tif') # filder wd for tifs

idtable = dict() # create dictionary to store ids
valuetable = list() # create dictionary to store data

# open output file
open("outdata.csv",'w')

# start loop for files
id = "aaa"
V = [""]*(len(NRCSids)) # initialize empty list to store values
I = [""]*(len(NRCSids)) # initialize empty list to store id names
datanames = [""]*28
j = -1
i = 0
for name in filenames:
	m = re.split("_",name) # id value at beginning of filename
	if m[0] != id: # reset i if id is different from the match
		i = 0
		id = m[0]
		j = j + 1
	dataname = name[len(m[0])+1:len(name)-4]
	values = gdalRaster2List(name) # get flat list of values from array
	ids = [id]*len(values)
	datanames[i] = dataname
	print(dataname)
	print(len(values))
    if j == 0: 
		V[i] = [values]
		I[i] = [ids]
	else:
		V[i].extend(values)
		I[i].extend(ids)
	print('i=',i,'j=',j,'id=',id,'name=',name,'dataname=',dataname)
	
	
	stats = scipy.stats.describe(values)
	i = i + 1

	
d = dict()
for i in range(len(datanames)):
	dn = datanames[i]
	print(i,dn+'.csv')
	d[dn] = [V[i],I[i]]
	df = pd.DataFrame([V[i],I[i]])
	df.to_csv(dn+'.csv',sep=',')
	
	

	

	
	
	
	

	
	
	


'''	
		
    # A list or 1d array of values
	value[i] = array.flatten() # numpy
	ids[i] = [id]*len(values) 
	
	stats = scipy.stats.describe(values)
	plt.imshow(array)
	plt.colorbar(array)
		


query = input("objective complete, type 'Y' to continue to the next objective")		
if query != 'Y': 
	print('exiting script')
	sys.exit()
>>>>>>> 7420e751d7fe487f04c21e2209a61df6c5680f64
'''