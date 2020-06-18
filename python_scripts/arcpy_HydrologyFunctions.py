# Name: arcpy_HydrologyFunctions
# Contains functions from the arcpy spatial analyst
# hydrology toolset
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/an-overview-of-the-hydrology-tools.htm

# DEFINE FUNCTIONS --------------------------------------------
# >>> GENERAL FUNCTIONS
# defineProjections ###########################################
# defines projections on a list of files using a template
def defineProjections(inFiles=["Points"],template="elevation"):
	# get the coordinate system by describing a feature class
	dsc = arcpy.Describe(template)
	coord_sys = dsc.spatialReference
		# run the tool for the list of files
	for file in inFiles:
		try:		
			arcpy.DefineProjection_management(file, coord_sys)
			arcpy.Project_management(file,"prj"+file,template)
		# print messages when the tool runs successfully
			print(arcpy.GetMessages(0))
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
		except Exception as ex:
			print(ex.args[0])
			
# splitShapefileByFeature -------------------------------------------------
# separate one shapefile in multiple ones by one specific attribute
# Need to change Name to a field 
def splitShapefileByFeature (inDir = "C:/Temp/data/",inFile="Points.shp",outDir = "C:/Temp/data/idPoints/",field="Name"):
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
		print outSHP
		gp.Select_analysis (inputFile, outSHP, "\""+field+"\" = '" + each_attribute + "'") #<-- CHANGE my_attribute to the name of your attribute
	del rows, row, attribute_types, gp

# >>> HYDROLOGY FUNCTIONS
# basin #######################################################
# Creates a raster delineating all drainage basins.

# fill ########################################################
# Fills sinks in a surface raster to remove small imperfections in the data.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/fill.htm
def fill(inDEM):
	return(arcpy.sa.Fill(inDEM))
# flowAccum ############################################
# Creates a raster of accumulated flow into each cell. A weight factor can optionally be applied.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-accumulation.htm
def flowAccum(inFlowDir):
	return(arcpy.sa.FlowAccumulation(inFlowDir))
# flowDir ###############################################
# Creates a raster of flow direction from each cell to its downslope neighbor, or neighbors, using D8, Multiple Flow Direction (MFD) or D-Infinity (DINF) methods.
# http://pro.arcgis.com/en/pro-app/tool-reference/spatial-analyst/flow-direction.htm
def flowDir(inDEM):
	return(arcpy.sa.FlowDirection(inDEM))
# flowDist ################################################
# Computes, for each cell, the horizontal or vertical component of minimum downslope distance, following the flow path(s), to cell(s) on a stream into which they flow.

# flowLen ##################################################
# Calculates the upstream or downstream distance, or weighted distance, along the flow path for each cell.

# sink ########################################################
# Creates a raster identifying all sinks or areas of internal drainage.

# snapPrPnt ###############################################
# Snaps pour points to the cell of highest flow accumulation within a specified distance.
def snapPrPnt(inPoint,inFlowAccum, searchDist=30, pourField="Name"):
	return(arcpy.sa.SnapPourPoint(inPoint, inFlowAccum, searchDist, pourField)) 
# streamLink ##################################################
# Assigns unique values to sections of a raster linear network between intersections.

# streamOrder #################################################
# Assigns a numeric order to segments of a raster representing branches of a linear network.

# streamToFeature #############################################
# Converts a raster representing a linear network to features representing the linear network.

# watershed ###################################################
# Determines the contributing area above a set of cells in a raster.
def watershed(inPoint,inFlowDir,pourField):
	return(arcpy.sa.Watershed(inFlowDir, inPoint, pourField))



	
# LOAD MODULES ------------------------------------------------
import arcpy 
from arcpy import env
import os
import glob




# MANAGE FILES AND DIRECTORIES --------------------------------
path = "C:/Temp/data/"
env.workspace = path
os.chdir(path)
print(os.listdir(path))




# MANAGE PROJECTIONS ------------------------------------------
# call function define projections
defineProjections()



# EXECUTE OBJECTIVES ------------------------------------------
# fill sinks in DEM
filledDEM = fill("elev.tif")
filledDEM = fill("elevation")
filledDEM.save("elevfilled")
del filledDEM
# !!#%^%#!%##$!&#$^&@(%&!#(&*!#$@(#%*&@(#&$@(#$
# THIS FUNCTION DOESNT WORK WITH ARCPY
# ArcMap geoprocessing toolbox works
# !@$@&#)%)&%(!&#$!)%^&*(&*#%!%*#^@&*%^@*&#%

# calculate flow direction
flwdr = flowDir("elevfilled")
flwdr.save("flowdir")
del flwdr

# calculate flow accumulation
flwaccm = flowAccum("flowdir")
flwaccm.save("flowaccum")
del flwaccm

# snap pour points to cells with highest flow accumulation
os.chdir("C:/Temp/data/points/")
env.workspace = ("C:/Temp/data/points/")
for file in glob.glob("*.shp"):
	print ("processing point,",file)
	point = snapPrPnt(file,"flowaccum")
	point.save("snapped_"+file)
	del point

# snap pour points to cells with highest flow accumulation
points = snapPrPnt("C:/Temp/data/points.shp","flowaccum")
points.save("rstsnappoints")
points = arcpy.RasterToPoint_conversion(points,"snappoints.shp")
inLayer = "snappoints" # extensionless name of file 
del points

# copy attribute table from points to snappoints
inLayer = "snappoints" # extensionless name of file 
inField = "FID" # name of attribute table field to join 
joinTable = "points" # extensionless name of file
joinField = inField 
arcpy.AddJoin_management (inLayer, inField, joinTable, joinField)

# split shapefile by feature




#END

# calculate watershed from a list of pour point files
# Batch process watershed creation
pourPath = "C:/Temp/data/idPoints/"
os.chdir("C:/Temp/data/idPoints/")
env.workspace = "C:/Temp/data/"
inPointFiles = glob.glob("*.shp")
inPourPointField = "FID"
inFlowDirection = "flowdir"
for file in inPointFiles[0:2]:
	pourPoint = pourPath + file
	print("processing watershed for point file =",file)
	outWatershed = watershed(pourPoint,inFlowDirection,inPourPointField)
	outfile =  "wshed_" + file[2:(len(file)-4)]
	print("saving output... file =",outfile)
	outWatershed.save(outfile)
	#del outWatershed 



