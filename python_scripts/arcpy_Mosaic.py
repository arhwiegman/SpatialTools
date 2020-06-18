##==================================
##Mosaic
##Usage: Mosaic_management inputs;inputs... target {LAST | FIRST | BLEND | MEAN | MINIMUM | MAXIMUM} {FIRST | REJECT | LAST | MATCH} 
##                         {background_value} {nodata_value} {NONE | OneBitTo8Bit} {mosaicking_tolerance}  
##                         {NONE | STATISTIC_MATCHING | HISTOGRAM_MATCHING 
##                         | LINEARCORRELATION_MATCHING}

import arcpy
# Set environment settings
env.workspace = "C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs"
import os
os.mkdir("C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Mosaic")
# Set local variables
inRaster02 = 'Elevation_DEMHF1p6m2012_AVT_345.img'
inRaster03 = 'Elevation_DEMHF1p6m2012_AVT_344.img'
inRaster04 = 'Elevation_DEMHF1p6m2012_AVT_343.img'
inRaster05 = 'Elevation_DEMHF1p6m2012_AVT_333.img'
inRaster06 = 'Elevation_DEMHF1p6m2012_AVT_332.img'
inRaster07 = 'Elevation_DEMHF1p6m2012_AVT_331.img'

infiles = (inRaster02+';'+inRaster03+';'+inRaster04+';'+inRaster05+';'+inRaster06+';'+inRaster07)

# need to create a target raster data set


##Mosaic two TIFF images to a single TIFF image
##Background value: 0
##Nodata value: 9
arcpy.Mosaic_management(infiles,"C:\\Users\\awiegman\\Downloads\\OtterData\\Lidar_DEMs\\Mosaic\\otter_mosaic.tif","LAST","FIRST","0", "9", "", "", "")

'''
##Mosaic several 3-band TIFF images to FGDB Raster Dataset with Color Correction
##Set Mosaic Tolerance to 0.3. Mismatch larget than 0.3 will be resampled
arcpy.Mosaic_management("rgb1.tif;rgb2.tif;rgb3.tif", "Mosaic.gdb\\rgb","LAST","FIRST","", "", "", "0.3", "HISTOGRAM_MATCHING")
'''