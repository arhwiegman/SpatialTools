# Name: ExtractByMask_Ex_02.py
# Description: Extracts the cells of a raster that correspond with the areas
#    defined by a mask.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace  = u"C:\\Users\\awiegman\\Downloads\\OtterData\\ElevationDEM_VTHYDRODEM\\"

# Set local variables
inRaster = "vthydrodem"
inMaskData = "C:\\Users\\awiegman\\Downloads\\OtterData\\HUC8_boundary\\OtterCreek.shp"

# Execute ExtractByMask
outExtractByMask = ExtractByMask(inRaster, inMaskData)

# Save the output
env.workspace  = u"C:\\Users\\awiegman\\Downloads\\OtterData\\ElevationDEM_VTHYDRODEM\\OtterCreek"
outExtractByMask.save("elevation") # GRID files cannot exceed 13 characters
# if saving adf file, the file must not have anything other than alphanumeric symbols