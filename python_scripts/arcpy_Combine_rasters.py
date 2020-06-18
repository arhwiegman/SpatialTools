# Name: arcpy_Combine_rasters.py
# Description: Combines multiple rasters such that a unique value is
#              assigned to each unique combination of input values
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set environment settings
env.workspace = "C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs"

# Set local variables
inRaster02 = 'Elevation_DEMHF1p6m2012_AVT_345.img'
inRaster03 = 'Elevation_DEMHF1p6m2012_AVT_344.img'
inRaster04 = 'Elevation_DEMHF1p6m2012_AVT_343.img'
inRaster05 = 'Elevation_DEMHF1p6m2012_AVT_333.img'
inRaster06 = 'Elevation_DEMHF1p6m2012_AVT_332.img'
inRaster07 = 'Elevation_DEMHF1p6m2012_AVT_331.img'
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute Combine
outCombine = Combine([inRaster02,inRaster03,inRaster04,inRaster05,inRaster06,inRaster07])

import os 
os.mkdir("C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Combined")
# Save the output 
outCombine.save("C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Combined")