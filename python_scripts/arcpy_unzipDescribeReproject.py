# Name: arcpy_unzipDescribeReproject.py
# Objective: unzips data files reads and describes the files and re-projects the spatial reference
# Author: Adrian Wiegman adrian.wiegman@gmail.com
# Vermont gridded soil survey geodatabase gdb
# downloaded from https://nrcs.app.box.com/v/soils/file/289014874015

# DEFINE FUNCTIONS --------------------------------------------------------------
# selectZips: uses glob to select .zip files in a specified working directory 
def selectZips(wd=""):
	import glob
	if wd=="":
		search = "*.zip"
	elif (wd[len(wd)-1] == "/" or wd[len(wd)-2:] == "\\"):
		search = wd + "*.zip"
	else:
		search = wd + "/*.zip"
	return(glob.glob(search))
	
	


	
# extractZips: uses zipfile to extractall files in a list of zipfiles
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
					
					
	
# selectData: uses glob to select data in a working directory matching a list of extensions 
def selectData(wd="",extList=[".shp",".tif"]):
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



# describeData: returns a dictionary of for each file with data descriptions and projections
def describeData(fileList):
	import arcpy
	descriptions = dict()
	for f in fileList:
		print(f)
		dsc = arcpy.Describe(f)
		prj = dsc.spatialreference
		descriptions[str(f)]=[dsc,prj] #dictionary
	return(descriptions)

			
		
# reprojectData: reprojects a list of data files to a specified output coordinated reference system
def reprojectData(fileList,outCRS):
	import arcpy
	import re 
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
			if ext=='.shp': arcpy.Project_management(data,"prj"+data,outCRS)
			if ext!='.shp': arcpy.ProjectRaster_management(data,"prj"+data,outCRS)
			# print messages when the tool runs successfully
			print(arcpy.GetMessages(0))
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
		except Exception as ex:
			print(ex.args[0])

# PRELIMINARY SETUP ------------------------------------------------------------
# import modules
import zipfile
import os
import glob
import arcpy

# set working directory
wd = "C:/temp/data/"
os.chdir(wd)
arcpy.env.workspace = wd

# EXECUTE OBJECTIVES ------------------------------------------------------------
zips = selectZips(wd)
extracted = extractZips(zips)
os.chdir("C:/temp/data/reproject/")
arcpy.env.workspace=("C:/temp/data/reproject/")
selected = selectData()
descriptions = describeData(selected)
reprojectData(selected,"prj.adf")

os.chdir("C:/temp/data/idPoints")
arcpy.env.workspace=("C:/temp/data/idPoints/")
selected = selectData()
descriptions = describeData(selected)
reprojectData(selected,"prj")