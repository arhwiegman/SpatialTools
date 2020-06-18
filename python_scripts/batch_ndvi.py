#***META DATA***
metadata=\
'''
file: batch_ndvi.py
author: Adrian Wiegman
repository: 
contact: adrian.wiegman@gmail.com 
dependencies: 
	- arcgis pro ()
	- python ()
	- arcpy ()
	- os ()
'''

#***FUNCTIONS***
def main():
# Executes main program
#-----------------------
    import arcpy
    import os
    from arcpy import env
	# check out license for spatial analyst toolbox 
	arcpy.CheckOutExtension("spatial")
	# set working directory
    env.workspace = r'Z:\GeoData\LCB\NAIP'
    # get and print a list of JP2 rasters from the workspace
    #http://pro.arcgis.com/en/pro-app/arcpy/functions/listrasters.htm
    rasters = arcpy.ListRasters("*", "JP2")	
    batch_process_rasters(rasters,calc_ndvi)
    rasters = arcpy.ListRasters("*ndvi*", "TIF")
    mosaic_to_new_raster(rasters)
	# return the spatial analyst license 
	arcpy.CheckInExtension("spatial")
    
def batch_process_rasters(rasters,function):
# Iterates through a list of rasters by passing each to the function
#------------------------- 
    for raster in rasters:
        print("processing...",raster)
        function(raster)
        

def calc_ndvi(input):
# Calculates NDVI from multispectral imagery
# This is for 4-band NAIP imagery or Landsat TM
# The band index may need to be changed data sources
#------------------------
    # not sure what this does

    
	# select raster bands
    red = arcpy.sa.Raster(input+'/Band_3')
    NIR = arcpy.sa.Raster(input+'/Band_4')
    
	# perform calculation in steps
    num = arcpy.sa.Float(NIR-red)
    denom = arcpy.sa.Float(NIR+red)
    ndvi = arcpy.sa.Divide(num,denom)
    
	# save output file 
	output = "ndvi_"+os.path.splitext(input)[0]+
	print("...creating file",output)
	fext = '.tif'
    ndvi.save(output+fext)

def mosaic_to_new_raster (inrasters):
# merges a list of raster files into one output raster 
#-----------------------
    nbands = arcpy.Raster.bandCount(inrasters[0])
    outname = "mosaic_ndvi2016_0p6m.tif"
    arcpy.MosaicToNewRaster_management(infiles, env.workspace, \
                                       outname, arcpy.SpatialReference(26918),\
                                       "32_BIT_FLOAT",number_of_bands=nbands)

#***MAIN PROGRAM***
if __name__ == '__main__':
    main()
