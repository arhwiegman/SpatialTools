# PROGRAM VITALS ==============================================
# Name: arcpy_Functions.py 
# Description: Functions for manipulating geospatial data with arcpy
# Author: Adrian Wiegman, adrian.wiegman@uvm.edu
# Date: 2018-06-19
# Notes:
# all functions must be written with the format below...
# ~~~~~~~~~~~~~~~~~~~~~ example format ~~~~~~~~~~~~~~~~~~~~~~~~
# (Line 1)      `# functionName ---------------`
# (Line 2)      `# function description `
# (Line 3 to n) `# additional links and build notes `
# (Line n+1)    `def functionName`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ==============================================================


# DEFINE FUNCTIONS #################################################### 
print("COMPILING FUNCTIONS...")
print("")
# >>> GENERAL FUNCTIONS................................................

# gitRunScript ---------------------------------------------------------
# downloads a python script from raw text on git hub and executes the file
def gitRunScript(rawURL=None):
	import requests
	if rawURL is None: 
		rawURL= "https://raw.githubusercontent.com/arhwiegman/UVM-research/master/LCB-Geospatial/Otter-analysis/Python_scripts/arcpy_Functions.py?token=AfPESkqBox4-kodP_LcWwWPz-rF-aAdcks5bF_gYwA%3D%3D"
	r = requests.get(rawURL)
	exec(r.text)

# gitSaveRaw -----------------------------------------------------------------
# saves a raw text from a github raw text url and asks user if the file can be saved
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

# writeMetadata ------------------------------------------------------
# generates a metadata file in specified folder
def writeMetadata(folder=None):
	import os
	from datetime import date
	today = str(date.today())
	if folder == None : folder = os.getcwd()
	filepath = os.path.join(folder, "metadata.txt")         
	f = open(filepath, "w")
	query = input("type 'Y' to update metadata.txt in this folder.")
	if (query != "Y"): return
	metadata = raw_input("Enter information on this data:")
	date = datetime.datetime.today().strftime('%Y-%m-%d')
	f.append("META DATA (date of entry:",today,")")
	f.append(metadata+"\n ---------------------")
	f.close()
	
# yyyymmdd --------------------------------------------
# returns string of system date in yyyymmdd format
def yyyymmdd():
	import datetime
	return(datetime.datetime.today().strftime('%Y%m%d'))

# buildFunctionDictionary --------------------------
# searches for functions in python script and creates a dicitonary
# all functions must be organized with the same format...
# =================== example format =======================
# (Line 1)      # functionName ---------------
# (Line 2)      # function description 
# (Line 3 to n) # additional links and build notes 
# (Line n+1)    def functionName
# ===========================================================
def buildFunctionDictionary(pyscript=None):
	
	rewind = lambda f: f.seek(0) #function to rewind file 
	import re
	import os 
	if pyscript == None: pyscript = os.path.basename(__file__)
	f = open(pyscript,"r")
	print("reading " + pyscript)
	script = f.read()
	rewind(f)
	#print("!!!!!!!!! START OF FILE: "+pyscript+" !!!!!!!!!!!!!")
	#print(script)
	#print("!!!!!!!!! END OF FILE:   "+pyscript+" !!!!!!!!!!!!!")
	# regular expression search for all functions
	print("searching script for functions...")
	pattern = "#\s(\S+)\s\-+\n#(.*)\n"#+".*def"
	functions = re.findall(pattern,script)
	dictionary = dict()
	# store function name and descriptions as dictionary
	print("building function dictionary...")
	for i in range(len(functions)):
		dictionary[functions[i][0]] = functions[i][1]
	
	return(dictionary)
#functionDictionary = buildFunctionDictionary()
print("\"functionDictionary[function.__name__]\" returns a description of a user defined function")


# defLookup ----------------------------------------------
# looks up a user defined function in the global environment
# assumed functionDictionary = 
def defLookup(function=""):
	if function == "":
		print("\"defLookup(functionName)\" inspects user defined functions")
		return

	def buildFunctionDictionary(pyscript=None):
		rewind = lambda f: f.seek(0) #function to rewind file 
		import re
		import os 
		if pyscript == None: pyscript = os.path.basename(__file__)
		f = open(pyscript,"r")
		print("reading " + pyscript)
		script = f.read()
		rewind(f)
		#print("!!!!!!!!! START OF FILE: "+pyscript+" !!!!!!!!!!!!!")
		#print(script)
		#print("!!!!!!!!! END OF FILE:   "+pyscript+" !!!!!!!!!!!!!")
		# regular expression search for all functions
		print("searching script for functions...")
		pattern = "#\s(\S+)\s\-+\n#(.*)\n"#+".*def"
		functions = re.findall(pattern,script)
		dictionary = dict()
		# store function name and descriptions as dictionary
		print("building function dictionary...")
		for i in range(len(functions)):
			dictionary[functions[i][0]] = functions[i][1]	
		return(dictionary)
		print("\"functionDictionary[function.__name__]\" returns a description of a user defined function")
	functionDictionary = buildFunctionDictionary()
	name = function.__name__
	print('')
	print('')
	print('Looking up user defined function...')
	print('name:',name)
	print('decription:',functionDictionary[name])
	import inspect
	print('source code:')
	print('--------------start-------------------')
	print('')
	print(inspect.getsource(function))
	print('')
	print('--------------end---------------------')
	print("")
	


# reFilterList --------------------------------------------
# filters a list of strings with regex search and returns new list 
def reFilterList(lines, regex):
	import re
	m = list()
	for n in lines: m.append(re.match(regex,n).group())
	return(m)
	

# selectZips ---------------------------------------------------------
# uses glob to select .zip files in a specified working directory 
def selectZips(wd=""):
	import glob
	if wd=="":
		search = "*.zip"
	elif (wd[len(wd)-1] == "/" or wd[len(wd)-2:] == "\\"):
		search = wd + "*.zip"
	else:
		search = wd + "/*.zip"
	return(glob.glob(search))

# extractZips -------------------------------------------------------------------
# uses zipfile to extractall files in a list of zipfiles
def extractZips(zipList):
	import zipfile
	pathList = []
	for f in zipList:
		path = f[:(len(f)-len(".zip"))]
		pathList.append(path)
		with zipfile.ZipFile(f,"r") as z:
			z.extractall()
			print(f+" extracted to directory:"+os.getcwd())
	return(pathList)

# globSelectData ---------------------------------------------------------------
# uses glob to select data in a working directory matching a list of extensions 
def globSelectData(wd="",extList=[".shp",".tif"]):
	import glob
	# lambda functions ------
	# flatten: flattens a list 
	flatten = lambda l: [item for sublist in l for item in sublist]
	# omitEmpty: removes empty lists from list
	omitEmpty = lambda l: [x for x in l if x]
	dataList = [] # initialize datafiles as a list
	for e in extList:
		if wd=="": 
			search = "*" + e 
		else:
			search = wd + "/*" + e
		print(search)
		matches = glob.glob(search) # glob search for data files
		dataList.append(matches) #append the list with matches of glob search
	dataList = flatten(omitEmpty(dataList)) # remove empty cells
	return(dataList)

def extractZips2Path(zipList):
	import zipfile
	pathList = []
	for f in zipList:
		path = f[:(len(f)-len(".zip"))]
		pathList.append(path)
		with zipfile.ZipFile(f,"r") as z:
			z.extractall(path)
			print(f+" extracted to "+path)
			if "C:" not in f: print("in directory:"+os.getcwd())
	return(pathList)
	
	
# globSelectFiles -----------------------------------------------------
# selects files from glob matching specified pattern
def globSelectFiles (pattern="*"):
	import glob 
	return(glob.glob(pattern))

	
# globSearchList ----------------------------------------------------------------
# returns a list of files from a list of glob search patterns
def globSearchList (extensions = ["*.jp2","*.img"]):
	# make list of files with the the following extensions 
	import glob
	files = list()
	for ext in extensions: 
		files = files + glob.glob(ext)
	return(files)

	
# >>> OPEN SOURCE GIS FUNCTIONS..............................

# plotRasterPanel ----------------------------------------------------
# plots raster list of data in figure panel of with default 3 column layout
#def plotRasterPanel(filelist, Ncol=3, clim=None, titles=None, cmap='inferno', label=None, overlay=None, fn=None):
#	import rasterio
#	import numpy as np
#	import matplotlib.pyplot as plt
#	
#   raster_list = [rasterio.open(f).read() for f in filenames]
#	Nrow = int(round((len(raster_list())/X),0))
#   fig, axa = plt.subplots(Nrow,Ncol, sharex=True, sharey=True, figsize=(10,5))
#    alpha = 1.0
#    for n, ax in enumerate(axa):
#        #Gray background
#        ax.set_facecolor('0.5')
#        #Force aspect ratio to match images
#        ax.set(adjustable='box-forced', aspect='equal')
#        #Turn off axes labels/ticks
#        ax.get_xaxis().set_visible(False)
#        ax.get_yaxis().set_visible(False)
#        if titles is not None:
#            ax.set_title(titles[n])
#        #Plot background shaded relief map
#        if overlay is not None:
#            alpha = 0.7
#            axa[n].imshow(overlay[n], cmap='gray', clim=(1,255)) 
#    #Plot each array 
#    im_list = [axa[i].imshow(raster_list[i], clim=clim, cmap=cmap, alpha=alpha) for i in range(len(raster_list))]
#    fig.tight_layout()
#    fig.colorbar(im_list[0], ax=axa.ravel().tolist(), label=label, extend='both', shrink=0.5)
#    if fn is not None:
#        fig.savefig(fn, bbox_inches='tight', pad_inches=0, dpi=150)
#    r.close() for r in raster_list

# subsetGeoDataFrame -------------------------
def gdfSelectData(gdf,row=None,col=None):
	if row == None: # select all rows
		if col == None: # select all rows and columns
			subset = gdf.cx[:,:]
		subset = gdf.cx[:,col]
	elif col == None: # select all columns
		subset = gdf.cx[row,:]
	else:
		subset = gdf.cx[row,col]

	
# mergeGeoDataFrames ---------------------------
#https://automating-gis-processes.github.io/2016/Lesson3-spatial-join.html
# returns a geodataframe merged with a dataframe on an index column
# gdf: the geodataframe to be the left side data
# df: the geodataframe or dataframe to be added on the right
# index_column: a string containing the matching column 'name'   
def mergeGeoDataFrames(gdf,df,index_column):
	import geopandas as gpd
	return(gdf.merge(df,on=index_column))

# shp2GeoDataFrame ------------------------
# input shapefile output geodataframe
def shp2GeoDataFrame(filepath):
	import geopandas as gpd
	return(gpd.read_file(filepath))
	
# merge data with shapefile feature table
# joinDataFramesOnID ------------------------
# input shapefile output geodataframe
def joinDataFramesOnID(df1,df2,ID='id'):
	import pandas as pd
	return(gdf.join(df.set_index(ID), on=ID))

# https://geohackweek.github.io/raster/06-pygeotools_rainier/
# raster2NumPyMaskedArray ---------------------------
# input gdal dataset 
# output numpy array with 'no data' values masked
def raster2NumPyMaskedArray(gdal_ds):
	from pygeotools.lib import iolib
	return(iolib.ds_getma(gdal_ds))
	
# warpMultipleFiles ------------------------------------
# warp data to match the intersection of files and use minimum resolution of files, use spatial reference of template
# returns warped, in-memory GDAL dataset objects
def warpMultipleFiles(filenames,srs_template):
	from pygeotools.lib import warplib 
	return(warplib.memwarp_multi_fn(filenames, extent='intersection', res='min', t_srs=srs_template))

# rasterioMaskedArray --------------------------------------------
# opens file with rasterio 
# returns numpy array with invalid values masked
def rasterioMaskedArray(filename):
	import rasterio
	import numpy as np
	with rasterio.open(filename) as ds: # open datasource with rasterio
		if 'NAIP' in filename: # calculate NDVI from NAIP imagery
			red = ds.read(1).astype(np.float64)
			grn = ds.read(2).astype(np.float64)
			blu = ds.read(3).astype(np.float64)
			nir = ds.read(4).astype(np.float64)
			array = NDVI(red,nir)
		else:
			array = ds.read()
	return(np.ma.masked_invalid(array))

# NDVI -------------------------------------------------------
# takes red and nir array data and returns and array of NDVI
def NDVI(red,nir):
	return (nir - red)/(nir + red)	

# modeNDArray ---------------------------------------
# calculates mode or most common value in ndarray
def modeNDArray(ndarray):
	from collections import Counter
	return(Counter(ndarray.flatten()).most_common(1)[0][0])

# download_gdalMergePy ----------------------------------------------
# downloads gdal_merge.py into working directory from git hub 
def download_gdalMergePy(directory=None):
    import requests, os
    url = "https://raw.githubusercontent.com/geobox-infrastructure/gbi-client/master/app/geobox/lib/gdal_merge.py"
    if  == None: directory = os.getcwd()
    filename =  os.path.join(directory,'gdal_merge.py')
    r = requests.get(url)
    f = open(filename,'w')
    f.write(r.text)
    f.close
    glob.glob("gdal_merge.py")


# gdalRaster2List -------------------------------------------------
# reads a raster file with gdal and returns a list of values
# name is a string containing the name of the data source raster 
# "myraster.tif"
#def gdalRaster2List(name):
#	from osgeo import gdal
#	import numpy as np
#	f = gdal.Open(name) # open file with gdal library
#	if 'NAIP' in name: # calculate NDVI from NAIP imagery
#    	red = f.GetRasterBand(1).ReadAsArray()
#		blu = f.GetRasterBand(2).ReadAsArray()
#		grn = f.GetRasterBand(3).ReadAsArray()
#		nir = f.GetRasterBand(4).ReadAsArray()
#		red = red.astype(np.float64)
#		nir = nir.astype(np.float64)
#		array = osgNDVI(red,nir)
#	else:
#		array = f.GetRasterBand(1).ReadAsArray()
#		array = array.astype(np.float64)
#	return(array.flatten())


# randCirlcsInsidePoly ---------------------------------------------------
# create randomly selected points inside a polygon with a specified radius
def randomCirclesInsidePoly(poly,numPoints=1,radius=1,sides=64,SEED=30):
    import numpy as np
    np.random.seed(SEED)
    from shapely.geometry import Polygon, Point
    min_x, min_y, max_x, max_y = poly.bounds
    circles = []
    while len(circles) < numPoints:
        # generate random uniform number between min and max of bounds
        randomPoint = Point([np.random.uniform(min_x, max_x), np.random.uniform(min_y, max_y)])
        randomCircle = randomPoint.buffer(radius,sides)
        if (randomCircle.within(poly)):
            circles.append(randomCircle)
    return(circles)

# findRasters -----------------------------------------
# finds all raster files in specified path
def findRasters (path=None, filter="*.tif"):
    import os, fnmatch
    for root, dirs, files in os.walk(path):
        for file in fnmatch.filter(files, filter):
            yield file


#gdal_clipRasterByMask ----------------------------------------------
# clips rasters by polygon mask and saves outputs to specified folder
# uses cmd for gdalwarp http://www.gdal.org/gdalwarp.html
def gdal_clipRasterByMask(RASTERS,MASK,INPUT_FOLDER,OUTPUT_FOLDER):
    import os
    for raster in RASTERS:
        inRaster = INPUT_FOLDER + '/' + raster
        outRaster = OUTPUT_FOLDER + '/clip_' + raster
        cmd = 'gdalwarp -ot Float32 -of GTiff -t_srs "EPSG:26918" -cutline %s -crop_to_cutline %s %s' % (MASK, inRaster, outRaster)
        os.system(cmd)

# gdal_merge ---------------------------------------------
# runs command for gdalwarp or gdal_merge.py 
# http://www.gdal.org/gdalwarp.html
def gdal_merge(rasterList=None,outFile=None,SRS="EPSG:26918"):
    import os
    inRasters = ' '.join(rasterList)
    cmd = 'gdal_merge.py -of GTiff -t_srs %s -o %s %s' %(SRS,outFile,inRasters)
    os.system(cmd)

	
# >>> ARCPY FUNCTIONS.............................................................
# http://pro.arcgis.com/en/pro-app/tool-reference/introduction-anatomy/anatomy-of-a-tool-reference-page.htm

# arcWorkspace ------------------------------------------------------
# sets arcpy.env.workspace and os.dir in specified path
def arcWorkspace (path = "C:/temp/"):
	import arcpy
	import os
	os.chdir(path)
	arcpy.env.workspace = path
	

# arcDescribeData -----------------------------------------------------------
# returns a dictionary of for each file with data descriptions and projections
def arcDescribeData(fileList):
	import arcpy
	descriptions = dict() #dictionary
	for f in fileList:
		print(f)
		dsc = arcpy.Describe(f)
		prj = dsc.spatialreference
		descriptions[str(f)]=[dsc,dsc.featureType,dsc.shapeType,dsc.spatialreference,dsc.hasSpatialIndex] 
		print("Feature Type:  " + dsc.featureType)
		print("Shape Type :   " + dsc.shapeType)
		print("Spatial Index: " + str(dsc.hasSpatialIndex))
		print("Spatial Reference:"+ dsc.spatialreference)
	return(descriptions)


# arcReprojectData -----------------------------------------------------------------
# reprojects a list of data files to a specified output coordinated reference system
def arcReprojectData(fileList,outCRS):
	import arcpy
	import re 
	import os
	from time import gmtime, strftime
	os.mkdir("prjdata")
	with open("prjdata\CRSmeta",'w') as meta: 
		meta.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
		meta.write("\n Coordinate Reference System \n")
	for f in fileList:
		# remove file extensions
		ext = re.match(".*(\..*)",f) 
		print(ext)
		if m != None: 
			data = f[:len(ext.group(1))] 
		else: 
			data = f
			
		# run the reprojection tool
		try:
			if ext=='.shp': arcpy.Project_management(data,"prjdata/"+data,outCRS)
			if ext!='.shp': arcpy.ProjectRaster_management(data,"prjdata/"+data,outCRS)
			# print messages when the tool runs successfully
			print(arcpy.GetMessages(0))
			meta.write(arcpy.GetMessages(0))
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
			meta.write(arcpy.GetMessages(0))
		except Exception as ex:
			print(ex.args[0])
			meta.write(arcpy.GetMessages(0))

			
# arcReprojectBatch -----------------------------------------------------------------
# re-projects a list of data files to a specified output coordinated reference system
# updated and debugged: 20180-05-31
def arcReprojectBatch(wd,fileList,outCRS=None):
	import os, glob, re,  sys, arcpy
	from time import gmtime, strftime
	arcpy.env.workspace = wd
	if type(fileList) is not list:
		print(arcReprojectBatch.__name__+"failed, fileList must be of type list")
		sys.exit(arcReprojectBatch.__name__+"failed, fileList must be of type list")
		
	if outCRS is None: ourCRS = arcpy.SpatialReference(26918) #NAD83 UTM 18N
	 
	outDir = "\\prjbatch"+strftime('%Y%m%d%H%M%S',gmtime())+"\\"
	os.mkdir(arcpy.env.workspace + outDir)
	outPath = arcpy.env.workspace + outDir
	print(outPath)

	# write metadata
	meta = open(outPath+"CRSmeta",'w')
	meta.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	meta.write("\n Coordinate Reference System \n")
	
	for f in fileList:
		# remove file extensions
		m = re.match(".*(\..*)",f)
		if m == None:
			ext=""
			data = f
		else:
			ext=m.group(1)
			data = f[:(len(f)-len(ext))] 
		print(data,ext)
		
		# run the reprojection tool
		try:
			print("trying to reproject data")
			if ext=='.shp': out = arcpy.Project_management(wd+f,outPath+f,outCRS)
			if ext!='.shp': out = arcpy.ProjectRaster_management(wd+f,outPath+f,outCRS)
			# print messages when the tool runs successfully
			del out
			print(arcpy.GetMessages(0))
			meta.write(arcpy.GetMessages(0))
			
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
			meta.write(arcpy.GetMessages(0))
		except Exception as ex:
			print(ex.args[0])
			meta.write(arcpy.GetMessages(0))
			
		mxd = arcpy.mapping.MapDocument(r"C:\Temp\ArcGIS\Untitled.mxd")
		for df in arcpy.mapping.ListDataFrames(mxd):
			for lyr in arcpy.mapping.ListLayers(mxd, "", df):
				#if lyr.name.lower() == "rivers":
				arcpy.mapping.RemoveLayer(df, lyr)
		#mxd.saveACopy(r"C:\Project\Project2.mxd")
		#del mxd
			

# arcRaster2NumPyArray -----------------------------------------------
# convert raster image into numpy array object
# rst is the raster file name
def arcRaster2NumPyArray(rst):
	import arcpy
	arcpy.RasterToNumPyArray(rst)
			
# arcExtractByMask ---------------------------------------------------
# extracts raster (rst) cells that overlap with the mask (msk) 
# mask can be raster or vector object
def arcExtractRasterByMask(rst,msk,outpath=None,outname=None,ext='.tif'):
	import arcpy
	import os 
	if outpath==None: outpath = "C:\\temp"
	if outname==None: outname = "extract"
	extract = arcpy.sa.ExtractByMask(rst,msk)
	print(os.path.join(outpath,outname))
	extract.save(os.path.join(outpath,outname+ext))
	return(extract)

# arcSplitShapefileByFeature --------------------------------------------------------
# separate one shapefile in multiple ones by one specific attribute
# Need to change Name to a field
# debugged? 
def arcSplitShapefileByFeature (inDir = "C:/Temp/data/",inFile="Points.shp",outDir = "C:/Temp/data/idPoints/",field="Name"):
	import arcgisscripting
	import os 
	# Starts Geoprocessing
	gp = arcgisscripting.create(9.3)
	gp.OverWriteOutput = 1
	
	# set input file path
	inputFile = os.path.join(inDir,inFile)

	# Make the outDir if it doesn't already exist using os
	import os 
	if not os.path.isdir(outDir):
		os.mkdir(outDir)

	# Read Shapefile for different values in the attribute
	rows = gp.searchcursor(inputFile)
	row = rows.next()
	attribute_types = set([])

	while row:
		attribute_types.add(eval("row."+field))
		row = rows.next()
	# Output a Shapefile for each different attribute
	for each_attribute in attribute_types:
		outSHP = os.path.join(outDir,str(each_attribute[:4]) + u".shp")
		print(outSHP)
		gp.Select_analysis (inputFile, outSHP, "\""+field+"\" = '" + each_attribute + "'") 
	del rows, row, attribute_types, gp


# arcReformatRaster ---------------------------------------------------
# converts list of raster files to a single format in specified path
# inFilesList: list of files e.g.
#                       files = ['file.img',file2.jpg','file3.gif']
#http://resources.arcgis.com/en/help/main/10.1/index.html#//001200000032000000
def arcReformatRaster (FileList=["file1.tif","file2.tif"],
	inPath=None,outPath=None,Format="TIFF"):
	import arcpy, os
	if inPath==None: inPath=os.getcwd()
	if outPath==None: outPath=os.getcwd()
	inFileList = list()
	outFileList = list()
	for f in FileList:
		inFilePath = inPath+"\\"+f
	try:
		##Convert Multiple Raster Dataset to FGDB
		arcpy.RasterToOtherFormat_conversion(inFilePath,outPath,Format)	
	except:
		print("Raster To Other Format Failed.")
		print(arcpy.GetMessages())

# arcMosaic2NewRaster -------------------------------------------------------------------		
# creates a single raster from many raster tiles
# https://pro.arcgis.com/en/pro-app/tool-reference/data-management/mosaic-to-new-raster.htm
def arcMosaic2NewRaster (inRasters=None,outPath=None,outName="NewMosaic",outExt = "",nbands=1):
	import arcpy
	if outPath is None: 
		os.mkdir("outMosaic")
		outPath = os.getcwd() + "\\outMosaic\\"
	#try: 
	arcpy.MosaicToNewRaster_management(inRasters,outPath,outName+outExt,number_of_bands=nbands,mosaic_method="FIRST",mosaic_colormap_mode="MATCH")
	#except:
	#	print("Mosaic To New Raster example failed.")
	#	print(arcpy.GetMessages())

# arcPolygon2Raster -------------------------------------------------------------
# arcPolygon2Raster(infeatures,field,outRaster)


# arcResampleRasters -----------------------------------------------------------------
# takes a list of file names sets cell size to specified scale 
# FileList: list of strings containing raster file names ["file1.tif","file2.tif"]
# inPath(optional): path where input files are located, default is os.getcwd()
# outPath(optional): path where output files are created, default is os.getcwd()
# scale: You can specify the cell size in 3 different ways: 
#			1. Using a single number specifying a square cell size
#			2. Using two numbers that specify the X and Y cell size, which is space delimited
#			3. Using the path of a raster dataset from which the square cell size will be imported
# http://pro.arcgis.com/en/pro-app/tool-reference/data-management/resample.htm
def arcResampleRasters(FileList=["f1.tif","f2.tif"],inPath=None,outPath=None,resolution="C:\\templateRaster.tif"):
	import arcpy, os
	if inPath==None: inPath=os.getcwd()
	if outPath==None: 
		outPath=os.getcwd()+"\\resampled"
		os.mkdir(outPath)
	
	inFileList = list()
	outFileList = list()
	if type(FileList) is list():
		for f in FileList:
			inFilePath = inPath+'\\'+f
			outFilePath = outPath+'\\'+f
			#Rescale Function Call 
			arcpy.Resample_management(inFilePath, outFilePath, resolution,"CUBIC")
	else:
		inFilePath = inPath+'\\'+FileList
		outFilePath = outPath+"\\resampled_"+FileList
		arcpy.Resample_management(inFilePath, outFilePath, resolution,"CUBIC")
	print("completed rescale of files @ location:", outPath)
	
# arcSaveRasterBands -----------------------------------------------------------------
# saves raster individual bands from a multiband raster file 
def arcSaveRasterBands (InRaster='C:\\Users\\awiegman\\Downloads\\OtterData\\n_4307316_nw_1_20030912.jp2'):
	import arcpy, os
	# get a list of the bands that make up the raster
	arcpy.env.workspace = InRaster
	Bands = arcpy.ListRasters()
	for Bnd in Bands:
		# loop through the bands and export each one with CopyRaster
		InBand  = '{}\\{}'.format(InRaster,Bnd)
		bndDesc = arcpy.Describe(InBand)
		NoData  = bndDesc.noDataValue 
		InSplit = os.path.splitext(InRaster) # split the image name and extension
		# output file name is c:\\some\\path\\raster_Band_X.ext
		OutRaster  = '{}_{}{}'.format(InSplit[0],Bnd,InSplit[1])
		arcpy.CopyRaster_management(InBand,OutRaster,nodata_value = NoData)

		

# arcAppendFeatures -----------------------------------
# input: a list of features of the same class
# output: a new file containing input features
def arcAppendFeatures(wd,inList,outName,template="template.shp"):
	import arcpy 
	arcpy.env.workspace = wd
	dsc = arcpy.Describe(template)
	arcpy.CreateFeatureclass_management(wd, outName, dsc.shapeType, inList[0], 'DISABLED', 'DISABLED', dsc.spatialReference)
	arcpy.Append_management(inList,outName)

# arcMergeFeatures -----------------------------------
# input: a list of features of the same class
# output: a new file containing input features
def arcMergeFeatures(wd,inList,outName,template="template.shp"):
	import arcpy 
	arcpy.env.workspace = wd
	dsc = arcpy.Describe(template)
	arcpy.CreateFeatureclass_management(wd, outName, dsc.shapeType, inList[0], 'DISABLED', 'DISABLED', dsc.spatialReference)
	arcpy.Merge_management(inList,outName)

# arcSelectLayersByFID ----------------------------------
# input a list of FID numbers
# output a new feature class with only selected FID numbers
def arcSelectLayersByFID(wd,infeature,FIDlist):
	import arcpy
	arcpy.MakeFeatureLayer_management(os.path.join(wd,infeature+'.shp'), "lyr")
	sql = '"FID" IN ({0})'.format(', '.join(map(str, FIDlist)) or 'NULL')
	print(sql)
	arcpy.SelectLayerByAttribute_management('lyr',"NEW_SELECTION", sql)
	arcpy.CopyFeatures_management("lyr",os.path.join(wd,infeature+"_selection.shp"))

# arcSelectAndSaveNew ----------------------------------------
# select features from input data with sql query and save new file
def arcSelectAndSaveNew(wd=None,infeature=None,outname=None,sql=None):
	if outname==None: outname = "selection_"+infeature
	import arcpy
	arcpy.env.workspace = wd
	arcpy.Select_analysis(infeature,outname,sql)
	
# arcSelectAndMakeFeatureLayerCopy -------------------------------------
# this function is equivalent to "arcSelectAndSaveNew"
def arcSelectAndMakeFeatureLayerCopy(wd,infeature,name,sql):
	import arcpy	
	arcpy.env.workspace = wd
	arcpy.management.MakeFeatureLayer(infeature, "new_layer", sql)
	arcpy.management.CopyFeatures("new_layer", outname)
	arcpy.management.Delete("new_layer")
	
# >>> ARCPY SPATIAL ANALYST FUNCTIONS................................................
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/an-overview-of-the-spatial-analyst-toolbox.htm

		
# arcExportNDVI ---------------------------------------------------------------------
# export normalized vegetation difference index from multispectral raster image
# CURRENTLY CRASHING ArcMap
# inRaster: multiband raster image
# redBand: band Number where red reflectance is stored 
# NIRBand: band Number where near infrared reflectance is stored 
def arcExportNDVI (inRaster,outPath,redBand=3,NIRBand=4):
	import arcpy, os
	red = arcpy.sa.Raster(inRaster+'\\Band_'+str(redBand))
	NIR = arcpy.sa.Raster(inRaster+'\\Band_'+str(NIRBand))

	# Calculate NDVI as (NIR-red)/(NIR+red)
	numerator = arcpy.sa.Float(NIR-red)
	denom = arcpy.sa.Foat(NIR+red)
	NDVI = arcpy.sa.Divide(num, denom)

	outRaster  = '{}_{}{}'.format(InSplit[0],"NDVI",InSplit[1])
	NDVI.Save(outPath+outRaster)

# >>> >>> HYDROLOGY FUNCTIONS...
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/an-overview-of-the-hydrology-tools.htm

# basin ------------------------------------------------------------------
# Creates a raster delineating all drainage basins.

# fill -------------------------------------------------------------------
# Fills sinks in a surface raster to remove small imperfections in the data.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/fill.htm
def archyFill(inDEM):
	return(arcpy.sa.Fill(inDEM))
	

# flowAccum -----------------------------------------------------------------
# Creates a raster of accumulated flow into each cell. A weight factor can optionally be applied.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-accumulation.htm
def archyFlowAccum(inFlowDir):
	return(arcpy.sa.FlowAccumulation(inFlowDir))
	

# flowDir --------------------------------------------------------------------
# Creates a raster of flow direction from each cell to its downslope neighbor, or neighbors, using D8, Multiple Flow Direction (MFD) or D-Infinity (DINF) methods.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-direction.htm
def archyFlowDir(inDEM):
	return(arcpy.sa.FlowDirection(inDEM))
	
	
# archyFlowDist -------------------------------------------------------------------
# Computes, for each cell, the horizontal or vertical component of minimum downslope distance, following the flow path(s), to cell(s) on a stream into which they flow.



# archyFlowLen --------------------------------------------------------------------
# Calculates the upstream or downstream distance, or weighted distance, along the flow path for each cell.



# archySink -----------------------------------------------------------------------
# Creates a raster identifying all sinks or areas of internal drainage.



# archySnapPrPnt --------------------------------------------------------------------
# Snaps pour points to the cell of highest flow accumulation within a specified distance.
def archySnapPrPnt(inPoint,inFlowAccum, searchDist=30, pourField="Name"):
	return(arcpy.sa.SnapPourPoint(inPoint, inFlowAccum, searchDist, pourField)) \


	
# archyStreamLink ---------------------------------------------------------------
# Assigns unique values to sections of a raster linear network between intersections.



# archyStreamOrder ---------------------------------------------------------------
# Assigns a numeric order to segments of a raster representing branches of a linear network.



# archyStreamToFeature -----------------------------------------------------------
# Converts a raster representing a linear network to features representing the linear network.



# archyWatershed ------------------------------------------------------------------
# Determines the contributing area above a set of cells in a raster.
def archyWatershed(inPoint,inFlowDir,pourField):
	return(arcpy.sa.Watershed(inFlowDir, inPoint, pourField))

print("")
print("FUNCTIONS COMPILED WITH ZERO ERRORS")
