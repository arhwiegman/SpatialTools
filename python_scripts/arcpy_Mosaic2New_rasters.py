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

infiles = (inRaster02+';'+inRaster03+';'+inRaster04+';'+inRaster05+';'+inRaster06+';'+inRaster07)
# Check out the ArcGIS Spatial Analyst extension license
arcpy.CheckOutExtension("Spatial")

# Execute Combine
outCombine = arcpy.MosaicToNewRaster_management(

import os 
os.mkdir("C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Combined")
# Save the output 
outCombine.save("C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Combined")



##==================================
##Mosaic To New Raster
##Usage: MosaicToNewRaster_management inputs;inputs... output_location raster_dataset_name_with_extension 
##                                    {coordinate_system_for_the_raster} 8_BIT_UNSIGNED | 1_BIT | 2_BIT | 4_BIT 
##                                    | 8_BIT_SIGNED | 16_BIT_UNSIGNED | 16_BIT_SIGNED | 32_BIT_FLOAT | 32_BIT_UNSIGNED 
##                                    | 32_BIT_SIGNED | | 64_BIT {cellsize} number_of_bands {LAST | FIRST | BLEND  | MEAN 
##                                    | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH}                               

import arcpy
arcpy.env.workspace = r"\\MyMachine\PrjWorkspace\RasGP"

##Mosaic several TIFF images to a new TIFF image
arcpy.MosaicToNewRaster_management("landsatb4a.tif;landsatb4b.tif","Mosaic2New", "landsat.tif", "World_Mercator.prj",\
                                   "8_BIT_UNSIGNED", "40", "1", "LAST","FIRST")