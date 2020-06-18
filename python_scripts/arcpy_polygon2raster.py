# Name: arc_poly2raster.py
# Description: Converts polygon features to a raster dataset.
# http://pro.arcgis.com/en/pro-app/tool-reference/conversion/polygon-to-raster.htm

# import system modules
import arcpy
import glob
import os

# set path
arcpy.env.workspace = 'C:/Users/awiegman/Downloads/VTGeologicSoils/rasters/'
os.chdir(arcpy.env.workspace)
inPath = 'C:/Users/awiegman/Downloads/VTGeologicSoils/rasters/'
outPath = 'C:/Users/awiegman/Downloads/VTGeologicSoils/rasters/'

# select files in working directory using REGEX search
inFiles = glob.glob("*SO01_SO21*.shp")
j=0 # manually specify file element index  

# set list of attribute names from attribute table 
atts = ["Kw","PARENT","PARENTSUB","ROCKSHALLO","SLOPELOW","WATERSHALL","HYDROGROUP"]

# create 10m Geotiffs in loop over attribute names 
for i in range(len(atts)):

	# Set local variables
	inFeatures = inPath + inFiles[j] 
	outRaster = "Geologic_SO01_SO21_"+atts[i]+".tif"
	outRasterPath = outPath + outRaster
	print(i,outRaster)
	valField = atts[i]
	assignmentType = "MAXIMUM_AREA"
	priorityField = ""
	cellSize = 10
	print("processing PolygonToRaster_conversion.....")
	# Execute PolygonToRaster
	arcpy.PolygonToRaster_conversion(inFeatures, valField, outRasterPath, assignmentType, priorityField, cellSize)
	# needed to specify path from root to for function to work

print("Completed PolygonToRaster_conversion!")
print("File location:",outPath)
