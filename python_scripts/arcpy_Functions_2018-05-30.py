# Functions for manipulating geospatial data with arcpy
# Author: Adrian Wiegman, adrian.wiegman@uvm.edu
# Date: 20180529

# DEFINE FUNCTIONS #################################################### 
print("COMPILING FUNCTIONS...")
print("")
# >>> GENERAL FUNCTIONS.....................................................

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
functionDictionary = buildFunctionDictionary()
print("\"functionDictionary[function.__name__]\" returns a description of a user defined function")


# defLookup ----------------------------------------------
# looks up a user defined function in the global environment
def defLookup(function):
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
print("use \"defLookup(function)\" to inspect user defined functions")
print("e.g.")
print('defLookup(defLookup)')
defLookup(defLookup)

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

	
# >>> ARCPY FUNCTIONS.............................................................
# http://pro.arcgis.com/en/pro-app/tool-reference/introduction-anatomy/anatomy-of-a-tool-reference-page.htm

# arcpyWorkspace ------------------------------------------------------
# sets arcpy.env.workspace and os.dir in specified path
def arcpyWorkspace (path = "C:/temp/"):
	import arcpy
	import os
	os.chdir(path)
	arcpy.env.workspace = path
	

# arcDescribeData -----------------------------------------------------------
# returns a dictionary of for each file with data descriptions and projections
def arcDescribeData(fileList):
	import arcpy
	descriptions = dict()
	for f in fileList:
		print(f)
		dsc = arcpy.Describe(f)
		prj = dsc.spatialreference
		descriptions[str(f)]=[dsc,prj] #dictionary
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
# update: 20180-05-30
def arcReprojectBatch(fileList,outCRS=arcpy.SpatialReference(26918)):
	import os, glob, re,  sys, arcpy
	from time import gmtime, strftime
	
	if type(fileList) is not list:
		print(arcReprojectBatch.__name__+"failed, fileList must be of type list")
		sys.exit(arcReprojectBatch.__name__+"failed, fileList must be of type list")
	# create folder to store projected data
	
	outpath = os.getcwd()+"\\prjdata"
	if not os.path.exists(outpath): 
		os.mkdir("prjdata")
	# write metadata
	meta = open("prjdata\CRSmeta",'w')
	meta.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	meta.write("\n Coordinate Reference System \n")
	
	for f in fileList:
		# remove file extensions
		ext = re.match(".*(\..*)",f).group(1)
		
		if ext != None: 
			data = f[:(len(f)-len(ext))] 
		else: 
			data = f
		print(data,ext)
		# run the reprojection tool
		try:
			if ext=='.shp' or ext=='.gdb':
				arcpy.Project_management(os.getcwd()+"/"+f,outpath+"/"+f,outCRS)
			else: 
				arcpy.ProjectRaster_management(os.getcwd()+"/"+f,outpath+"/"+f,outCRS)
			
			# print messages when the tool runs successfully
			print(arcpy.GetMessages(0))
			meta.write(arcpy.GetMessages(0))
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
			meta.write(arcpy.GetMessages(0))
		except Exception as ex:
			print(ex.args[0])
			meta.write(arcpy.GetMessages(0))
			

# arcSplitShapefileByFeature --------------------------------------------------------
# separate one shapefile in multiple ones by one specific attribute
# Need to change Name to a field
# debugged? 
def arcSplitShapefileByFeature (inDir = "C:/Temp/data/",inFile="Points.shp",outDir = "C:/Temp/data/idPoints/",field="Name"):
	import arcgisscripting
	# Starts Geoprocessing
	gp = arcgisscripting.create(9.3)
	gp.OverWriteOutput = 1
	
	# set input file path
	inputFile = inDir + inFile

	# Make the outDir if it doesn't already exist using os
	import os 
	if not os.path.isdir(outDir):
		os.mkdir(outDir)

	# Read Shapefile for different values in the attribute
	rows = gp.searchcursor(inputFile)
	row = rows.next()
	attribute_types = set([])

	while row:
		attribute_types.add(eval("row."+field)) #<-- CHANGE my_attribute to the name of your attribute
		row = rows.next()
	# Output a Shapefile for each different attribute
	for each_attribute in attribute_types:
		outSHP = outDir + each_attribute + u".shp"
		print(outSHP)
		gp.Select_analysis (inputFile, outSHP, "\""+field+"\" = '" + each_attribute + "'") #<-- CHANGE my_attribute to the name of your attribute
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
def arcResampleRasters (FileList=["file1.tif","file2.tif"],
	inPath=None,outPath=None,resolution="C:\\templateRaster.tif"):
	import arcpy, os
	if inPath==None: inPath=os.getcwd()
	if outPath==None: outPath=os.getcwd()
	inFileList = list()
	outFileList = list()
	for f in FileList:
		inFilePath = inPath+'\\'+f
		outFilePath = outPath+"\\scaled_"+f
		#Rescale Function Call 
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