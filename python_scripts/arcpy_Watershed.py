# Name: arcpy_Watershed.py
# Description: Determines the contributing area above a set of cells in a
#     raster.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = "C:\\Users\\awiegman\\Downloads\\OtterData\\"

# Set local variables
inFlowDirection = "ElevationDEM_VTHYDRODEM\\OtterCreek\\FlowDir"
inPourPointData = "NRCS_easements_OtterCreek\\Points.shp"
inPourPointField = "FID"

# Execute Watershed
outWatershed = Watershed(inFlowDirection, inPourPointData, inPourPointField)

# Save the output 
outWatershed.save("C:/Temp/Watershed")