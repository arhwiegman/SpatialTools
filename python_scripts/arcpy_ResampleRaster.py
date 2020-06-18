# arcpy_RescaleRaster.py
# Rescale
# Usage: Rescale_management in_raster out_raster x_scale y_scale


# DEFINED FUNCTIONS #################################################################

# arcResampleRasters -----------------------------------------------------------------------
# takes a list of file names sets cell size to specified scale 
# FileList: list of strings containing raster file names ["file1.tif","file2.tif"]
# inPath(optional): path where input files are located, default is os.getcwd()
# outPath(optional): path where output files are created, default is os.getcwd()
# scale: You can specify the cell size in 3 different ways: 
#			1. Using a single number specifying a square cell size
#			2. Using two numbers that specify the X and Y cell size, which is space delimited
#			3. Using the path of a raster dataset from which the square cell size will be imported
# http://pro.arcgis.com/en/pro-app/tool-reference/data-management/rescale.htm
def arcResampleRasters (FileList=["file1.tif","file2.tif"],
						inPath=None,
						outPath=None,
						scale="templateRaster.tif"):
    import arcpy
	import os
	if inPath==None: inPath==os.getcwd()
	if inPath==None: inPath==os.getcwd()
	inFileList = for f in FileList: inPath + "scaled"+str(scale)+f)
	inFileString = if len(inFileList>1): ';'.join(map(str, inFileList)) else str(inFileList)
	outFileList =  for f in FileList: outPath + "scaled"+str(scale)+f)
	outFileString = ';'.join(map(str, outFileList)
	
	#Rescale Function Call 
	arcpy.Rescale_management(inFileString, outFileString, resolution,"CUBIC")
	print("completed rescale, output file location:", outPath)
	return()
arcRescaleRasters(FilesList=[")
	

# listFilesWithExtensions ----------------------------------------------------------------
def listFilesWithExtensions (extensions = ["*.jp2","*.img"]):
	# make list of files with the the following extensions 
	import glob
	files = list()
	for ext in extensions: files = files + glob.glob(ext)
	return(files)

# MAIN PROGRAM ######################################################################
os.chdir("C:/temp/")
# make list of files with the the following extensions 
files = list()
for ext in ["*.jp2","*.img"]: files = files + glob.glob(ext)

listFilesWithExtensions(["*.jp2","*.img"])