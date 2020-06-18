# Name: arc_poly2raster.py
# Description: Converts polygon features to a raster dataset.
# http://pro.arcgis.com/en/pro-app/tool-reference/conversion/polygon-to-raster.htm

'''
# look in directory for files
import glob
# regular expressions search w/ glob
glob.glob('./*.txt')
'''

# import system modules
import arcpy
from arcpy import env


# set path
env.workspace = 'C:/Users/awiegman/Downloads'

# Set local variables
inFeatures = "Geologic_SO01/Geologic_SO01_poly.shp"
valField = "Kw"
outRaster = "C:/Users/awiegman/Downloads/outputs/Geologic_SO01_poly.shp"
assignmentType = "MAXIMUM_AREA"
priorityField = "MALES"
cellSize = 10

# Execute PolygonToRaster
arcpy.PolygonToRaster_conversion(inFeatures, valField, outRaster, 
                                 assignmentType, priorityField, cellSize)
								 
								 
								 
# ARC command shell

>>> import arcpy
>>> from arcpy import env
>>> env.workspace = 'C:/Users/awiegman/Downloads/GeologicSoils_SO01/'
>>> arcpy.PolygonToRaster_conversion("Geologic_SO01_poly.shp", "Kw",
...                                  "c:/Users/awiegman/Downloads/OUTS/Geologic_SO01.tif",
...                                  "MAXIMUM_AREA", "NONE", 0.25)