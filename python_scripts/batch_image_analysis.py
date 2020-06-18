#***META DATA***
metadata=\
'''
VITALS
------------------------------
file: batch_image_analysis.py
type: python script
date: 2018-01-27
author: Adrian Wiegman (https://github.com/arhwiegman/)
repository: https://github.com/arhwiegman/UVM-research/blob/master/LCB-Geospatial/Otter-analysis/Python_scripts/batch_ndvi.py
contact: adrian.wiegman@gmail.com 
dependencies: 
    - arcgis pro 
    - python libraries:
        - arcpy 
        - arcpy.sa 
        - os 
        
OBJECTIVES
-------------------------
Calculate various indexes from a batch of 4 band imagery
raster files using the `arcpy` spatial analyst toolbox

BUILD NOTES
---------------------------
- need to add status bar for processing larger files
- takes very long time (hours) to process NAIP imagery with 0.6m resolution
- need to add enhanced vegetation index function

REFERENCS
--------------------------
- NAIP Imagery http://maps.vcgi.vermont.gov/gisdata/metadata/NAIP_0_6M_CLRIR_2016.htm
    - band 1 = red
    - band 2 = green
    - band 3 = blue 
    - band 4 = near infrared
- NDVI https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
    separates plant areas densly covered with plant pigments from non vegetated areas
    also detects soils 0.1
- EVI https://en.wikipedia.org/wiki/Enhanced_vegetation_index
    separates high density vegetation better than NDVI
- NDWI https://en.wikipedia.org/wiki/Normalized_difference_water_index
    used to detect changed in water level in soils and water bodies
'''
#***FUNCTIONS***
def main():
# Executes main program
#-----------------------
    # load libraries 
    print("\n!\n!\n!\n0. PRELIMINARIES======")
    import arcpy
    import os
    import glob
    from arcpy import env
    # check out license for spatial analyst toolbox 
    arcpy.CheckOutExtension("spatial")
    # set working directory
    env.workspace = r'Z:\GeoData\LCB\NAIP'
    #env.workspace = r'C:\Workspace'
    
    print("\n!\n!\n!\n1. CALCULATIONS======")
    # select a list of JP2 rasters from the workspace
    rasters = arcpy.ListRasters("*", "JP2")
    print(rasters)
    # calculate indexes and save outputs to tif format 
    calclist = [ndvi,evi,ndwi]
    batch_process_rasters(rasters,[ndvi,evi,ndwi])

    print("\n!\n!\n!\n2. MOSAICING======")
    # mosaic outputs    
    for c in calclist:
        # select tif files to mosaic
        rasters = glob.glob(os.path.join(env.workspace,*["outputs",c.__name__+"*.tif"]))
        print(rasters)
        # merge tifs into single file
        outfile = "mosaic_"+c.__name__+"_2016_0p6m.tif"
        print("creating mosaic...",outfile)
        mosaic_to_new_raster(rasters,outfile)

    # return the spatial analyst license 
    arcpy.CheckInExtension("spatial")
    print("\n!\n!\n!\n COMPLETE!!!!!!")

    
def batch_process_rasters(rasters,functions):
# Iterates through a list of rasters by passing each 
# to a function within a list of functions
#------------------------- 
    i = 0
    for rst in rasters:
        i = i + 1
        print("processing: {}".format(i/len(rasters)),rst)
        for fnc in functions:
            print("calling function...",fnc.__name__)
            fnc(rst)
        
def ndvi(input):
# Calculates NDVI from multispectral imagery
# https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
# This is for 4-band NAIP imagery (R,G,B,NIR)
# The band index changes depending on source
#------------------------

    # select raster bands
    red = arcpy.sa.Raster(input+'/Band_1')
    #green = arcpy.sa.Raster(input+'/Band_2')
    #blue = arcpy.sa.Raster(input+'/Band_3')
    NIR = arcpy.sa.Raster(input+'/Band_4')
    
    # perform calculation in steps
    num = arcpy.sa.Float(NIR-red)
    denom = arcpy.sa.Float(NIR+red)
    calc = arcpy.sa.Divide(num,denom) # ndvi
    
    # save calc output file 
    output = "ndvi"+"_"+os.path.splitext(input)[0]+'.tif'
    print("...creating file",output)
    calc.save(os.path.join(env.workspace,*['outputs',output]))
    del calc # to prevent memory overload
    return()

def evi(input):
# Calculates EVI from multispectral imagery
# https://en.wikipedia.org/wiki/Enhanced_vegetation_index
# This is for 4-band NAIP imagery (R,G,B,NIR)
# The band index changes depending on source
#------------------------
    
    # select raster bands
    red = arcpy.sa.Raster(input+'/Band_1')
    blue = arcpy.sa.Raster(input+'/Band_3')
    NIR = arcpy.sa.Raster(input+'/Band_4')
    
    # perform calculation in steps
    num = arcpy.sa.Float(2.5*(NIR-red))
    denom = arcpy.sa.Float(NIR+red*6+blue*7.5+1)
    calc = arcpy.sa.Divide(num,denom) # evi
    
    # save calc to output file 
    output = "evi"+"_"+os.path.splitext(input)[0]+'.tif'
    print("...creating file",output)
    calc.save(os.path.join(env.workspace,*['outputs',output]))
    del calc # to prevent memory overload
    return()

def ndwi(input):
# Calculates NDWI from multispectral imagery
# https://en.wikipedia.org/wiki/Normalized_difference_water_index
# This is for 4-band NAIP imagery (R,G,B,NIR)
# The band index changes depending on source
#------------------------
    
    # select raster bands
    green = arcpy.sa.Raster(input+'/Band_2')
    NIR = arcpy.sa.Raster(input+'/Band_4')
    
    # perform calculation in steps
    num = arcpy.sa.Float(green-NIR)
    denom = arcpy.sa.Float(green+NIR)
    calc = arcpy.sa.Divide(num,denom) # ndwi
    
    # save output file 
    output = "ndwi"+"_"+os.path.splitext(input)[0]+'.tif'
    print("...creating file",output)
    calc.save(os.path.join(env.workspace,*['outputs',output]))
    del calc # to prevent memory overload
    return()
    
def mosaic_to_new_raster (inrasters,outname):
# merges a list of raster files into one output raster 
#-----------------------
    print(inrasters[0])
    nbands = arcpy.sa.Raster(inrasters[0]).bandCount
    outdir = os.path.join(env.workspace,"outputs")
    print(nbands)
    new = arcpy.MosaicToNewRaster_management(inrasters, outdir, \
                                       outname, arcpy.SpatialReference(26918),\
                                       "32_BIT_FLOAT",number_of_bands=nbands)
    del new
def print_metadata():
    with open ("batch_image_analysis"+"_metadata.md","w") as m:
        m.write(metadata)

#***MAIN PROGRAM***
if __name__ == '__main__':
    main()
    print_metadata()
