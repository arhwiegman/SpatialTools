# Name: arcpy_FlowDirection.py
# Description: Creates a raster of flow direction from each cell to its
#    steepest downslope neighbor.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import * #imports spatial analyst library

# Set environment settings
env.workspace = "C:\\Users\\awiegman\\Downloads\\OtterData\\ElevationDEM_VTHYDRODEM\\OtterCreek\\"

# Set local variables
inSurfaceRaster = "elevation"

# Execute FlowDirection
outFlowDirection = arcpy.sa.FlowDirection(inSurfaceRaster)

# Save the output 
outFlowDirection.save("flowdir") # GRID files cannot exceed 13 characters