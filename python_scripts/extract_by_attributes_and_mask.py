# This script selects raster pixels by attribute value and then extracts another raster by the selected values as a mask
# Requirements: Spatial Analyst Extension, Numpy, os, glob
def main(interactive=False):
    '''
    # SETUP ---
    # Loading modules and setting up directories
    '''
    dirs = setup_workspace(interactive)
    wd = dirs[0] # working directory
    '''
    # MAIN PROGRAM ----
    # 1. EXTRACT RASTER BY ATTRIBUTE BASED ON LAND USE HISTORY
    #   - Get areas that were forested or wetland in 1992
    #   - Get areas that were farms as of 2001
    '''
    #S1_extract_land_use_classes()
    '''
    # 2. EXTRACT DEPTH RASTER BASED ON PERCENTILES
    #   - analyze depth percentiles
    #   - get new rasters from depth selected percentiles for otter creek
    '''
    #S2_extract_depth_percentiles()
    '''
    # 3. EXTRACT RASTER BY MASK (LOCATION)
    #    get raster of conservation easements that were restored prior to 2017 
    #   (2012 is the year that the LiDAR data for Addison county was flown in VTRANS HEC-RAS model)
    '''
    S3_extract_all_by_inundation_boundary()
    
    
#LASKJDJF*@F(_@$*F(@*$F@

#START HERE USE GDAL_MERGE.py to make a raster stack then analyze data in arcgis
    
    '''
    arcpy_ExtractByMask()
    
    # 4. extract DEPTH data by mask for areas of different land use
    arcpy_ExtractByMask()
   
    # 3. ANALYSE RASTER DATA 
    '''
 
    '''
    arcpy_ResampleFromTemplate(inRast,
    inRast=u'Z:\GeoData\Temp\Agriculture2001_0p7.tif',
    outRast=u'Z:\GeoData\Temp\Agriculture2001.tif',
    method='NEAREST')
    outfile=u'Z:\GeoData\Temp\depth_agriculture2001.tif'
    
    
    infile = u'Z:\GeoData\Trueheart\Depth (Max).bathymetry029.tif'
    mask = u'Z:\GeoData\Temp\Agriculture2001.tif'
    outfile=u'Z:\GeoData\Temp\depth_forestsWetlands1992.tif'
    arcpy_ExtractByMask(infile,mask,outfile,deleteAfter=False)
    
    infile = u'Z:\GeoData\Trueheart\Depth (Max).bathymetry029.tif'
    mask = u'Z:\GeoData\Temp\Agriculture2001.tif'
    outfile=u'Z:\GeoData\Temp\depth_agriculture2001.tif'
    arcpy_ExtractByMask(infile,mask,outfile,deleteAfter=False)
    '''

 
def S4_resample_landuse_to_0p7m():
    # re-sample landuse
    input = 'masked_Agriculture2001.tif'
    arcpy_ResampleFromTemplate(inRast=input,
    template='Z:/GeoData/Trueheart/Depth (Max).bathymetry029.tif',
    outRast="resampled_"+input)
    input = 'masked_ForestWaterWetland1992.tif'
    arcpy_ResampleFromTemplate(inRast=input,
    template='Z:/GeoData/Trueheart/Depth (Max).bathymetry029.tif',
    outRast="resampled_"+input)
    
def S3_extract_all_by_inundation_boundary():
    # reduce file size by masking by inundation boundary
    infiles = [
    #'Z:/GeoData/Trueheart/Depth (Max).bathymetry029.tif',
    'Z:/GeoData/Temp/Agriculture2001.tif',
    'Z:/GeoData/Temp/ForestWaterWetland1992.tif',
    #'Z:/GeoData/LCB/NAIP/outputs/mosaic_ndvi_2016_0p6m.tif']
    outfiles = [
    #'masked_depth.tif',
    'masked_Agriculture2001.tif',
    'masked_ForestWaterWetland1992.tif',
    #'masked_mosaic_ndvi_2016_0p6m.tif']
    mask = 'Z:/GeoData/Trueheart/Inundation Boundary (Max Value_0).shp'
    for i in range(len(infiles)):
        arcpy_ExtractByMask(infiles[i],mask,outfiles[i],deleteAfter=False,clip=True,resample=True)
        

    
def S2_extract_depth_percentiles():
    # set input file and destination paths
    infile = u'Z:\GeoData\Trueheart\Depth (Max).bathymetry029.tif'
    dst = u'Z:\GeoData\Trueheart' # destination path
    # calculate percentiles
    pct = arcpy_CalculatePercentileFromRaster(inRaster=infile, 
    nbins=10, 
    omitValue=-9999.0, 
    trimMinMax=True,
    min=0,
    max=2.25)
    '''
    depth percentiles
    {'0.0%': 0.0009994507, 
    '10.0%': 0.27291107, 
    '20.0%': 0.46861267, 
    '30.0%': 0.62002563, 
    '40.0%': 0.7600937, 
    '50.0%': 0.899498, 
    '60.0%': 1.0399399, 
    '70.0%': 1.2348328, 
    '80.0%': 1.4948654, 
    '90.0%': 1.8216858, 
    '100.0%': 2.25}
    '''
    # select dictionary keys for lower and higher bounds of depth
    lower = ['0.0%','20.0%','40.0%','60.0%','80.0%']
    higher = ['20.0%','40.0%','60.0%','80.0%','100.0%']
    # for each range
    for i in range(len(lower)):
        low = pct[lower[i]] 
        high = pct[higher[i]]
        outfile = dst+'/depth_pct_{0:4.2f}-{1:4.2f}m.tif'.format(low,high)
        SQL = '{0} > {1} AND {0} < {2}'.format('VALUE',low,high)
        print('extracting file: {}'.format(o))
        arcpy_ExtractByAttributes(infile,SQL,outfile)
    
def S1_extract_land_use_classes():
    #   A. get raster of areas that have been forested since 1942, 1971, and 2001 respectively
    #       1992 and 2001 land use codes:
    agriculture = 2
    brush = 3
    forest = 4
    water = 5
    wetland = 6 
    #       set SQL conditions and format string (<> not equal to) 
    conditions = " {0} = {1} AND {0} = {2} AND {0} = {3} "
    SQL = conditions.format('VALUE',forest,water,wetland)
    i=u"Z:\GeoData\LCB\LCLULCB92\lclulcb92"
    o="ForestWaterWetland1992.tif"
    arcpy_ExtractByAttributes(inRaster=i,inSQL=SQL,outRaster=o)
    #   B. get raster of areas that were farms in 2001
    conditions = " {0} <> {1}"
    SQL = conditions.format('VALUE',agriculture)
    i=u"Z:\GeoData\LCB\LCLULCB01\lclulcb01"
    o="Agriculture2001.tif"
    arcpy_ExtractByAttributes(inRaster=i,inSQL=SQL,outRaster=o)

def arcpy_ResampleFromTemplate(inRast,template,outRast,method='NEAREST'):
    Y = arcpy.GetRasterProperties_management(template,'CELLSIZEY')
    X = arcpy.GetRasterProperties_management(template,'CELLSIZEX')
    arcpy.Resample_management(inRast, outRast, "{} {}".format(X,Y), method)
    return()
 
def arcpy_SelectFeatureByAttribute(inFeature,inSQL,outFeature):
    arcpy.MakeFeatureLayer_management(inFeature, 'lyr') 
    # Write the selected features to a new featureclass
    # Within selected features, further select only those cities which have a population > 10,000   
    arcpy.SelectLayerByAttribute_management('lyr', 'NEW_SELECTION', inSQL)
    arcpy.CopyFeatures_management('lyr', outFeature) 


def arcpy_ExtractByAttributes(inRaster,inSQL="VALUE > 1000",outRaster="extracted",deleteAfter=True):
    # Description: Extracts the cells of a raster based on a logical query.
    # Requirements: Spatial Analyst Extension 
    # Check out the ArcGIS Spatial Analyst extension license
    # Execute ExtractByAttributes
    print("extracting ",inSQL," from ",inRaster, "\n...")
    attExtract = arcpy.sa.ExtractByAttributes(inRaster, inSQL) 
    # Save the output 
    print("success! Saving file: ",outRaster)
    attExtract.save(outRaster)
    if deleteAfter:
        del attExtract
    return()
   
   
def arcpy_CalculatePercentileFromRaster(inRaster, nbins=10, omitValue=None, trimMinMax=False, min=None, max=None):
    # requires arcpy and numpy
    array = arcpy.RasterToNumPyArray(inRaster)
    #remove no data values, in this case zeroes, returning a flattened array  
    print ('removing no data values and flattening array.....'  )
    if omitValue is not None:
        flatArray = array[array != omitValue] 
    if trimMinMax is not None:
        print('trimming min and max values...')
        flatArray = numpy.clip(flatArray,min,max)  
    print ('sorting array....'  )
    flatArray = numpy.sort(flatArray)  
    numpy.histogram(flatArray,nbins)
    #report some summary stats  
    print('n = ', numpy.sum(flatArray)     )
    print('min = ', numpy.min(flatArray)     )
    print('median = ', flatArray[int(numpy.size(flatArray) * 0.50)] ) 
    print('max = ', numpy.max(flatArray)    )
    
    percentiles = [None]*nbins
    percentiles[0] = numpy.min(flatArray)
    # add percentile values in steps to the list of percentiles
    print('populating list with percentile values...')
    for i in range(1,nbins):
        percentiles[i] = flatArray[int(numpy.size(flatArray)*i/nbins)]
    percentiles.append(numpy.max(flatArray))
    pkeys = [str(k/nbins*100)+'%' for k in range(nbins+1)]
    pdict = dict(zip(pkeys,percentiles))
    print(pdict)
    return(pdict)


def arcpy_NormalizeRasterValues(inRaster,outRaster,maxValue=1,deleteAfter=False):
    # note that zonal statistics already calculates this so it may be faster to 
    # use http://help.arcgis.com/En/Arcgisdesktop/10.0/Help/index.html#//0017000000m7000000
    # load data, convert to array
    # requires arcpy and numpy
    orig_raster = arcpy.Raster(inRaster)
    array = arcpy.RasterToNumPyArray(inRaster)
    # do your math
    normalized_array = (array - array.min()) / (array.max() - array.min()) * maxValue
    # back to a raster
    normalized_raster = arcpy.NumPyArrayToRaster(
        in_array=normalized_array,
        lower_left_corner=inRaster.extent.lowerLeft,
        x_cell_size=inRaster.meanCellWidth,
        y_cell_size=inRaster.meanCellHeight)
    # and scene
    normalized_raster.save(outRaster)
    if deleteAfter:
        del normalized_raster
    return()
    

def arcpy_ExtractByMask(inRaster,inMask,outRaster,deleteAfter=False,clip=True,resample=True):
#takes either a raster or a shapefile and extracts data from inRaster inside mask
# requires spatial analyst extension
    if clip:
        try:
            e = arcpy.Describe(inMask).extent # create object of extent description
            extent = ("{} {} {} {}").format(e.XMin,e.YMin,e.XMax,e.YMax)
        except:
            print("oops something went wrong",traceback.print_exc())
        print('clipping ',inRaster,'to extent:\n',extent)
        inRaster = arcpy.Clip_management(inRaster,extent)
    if resample:
        inMask = arcpy_ResampleFromTemplate(inMask,inRaster)
    print("extracting by mask...")   
    masked = arcpy.sa.ExtractByMask(inRaster,inMask)
    masked.save(outRaster)
    if deleteAfter:
        del masked

def load_modules():
# arcpy doesn't
    # Loads modules and links directory paths
    import os
    import glob
    import numpy
    import arcpy
    from arcpy import env 
    arcpy.CheckOutExtension("Spatial")
    return()
   
   
def print_dir_contents(dir):
    print("Directory:\n", os.getcwd())
    print("-"*15,"contents","-"*15,"\n",os.listdir())
    return()

def setup_workspace(interactive):
    # set local variables
    import os
    import glob
    import numpy
    import arcpy
    from arcpy import env 
    arcpy.CheckOutExtension("Spatial")
    import os
    print("Current environment workspace:\n", os.getcwd())
    
    if interactive:
        wd = env.workspace = input("copy environment workspace path below\n(e.g. ' Z:/awiegman/GeoData ')\n>>>")
        dirs = [wd]
        more = input("(A) press enter continue\n(B) press any other key then enter to link more directories)")
        while len(more)>0:
            dirs[len(dirs)+1] = input("copy environment workspace path below\n(e.g. ' Z:/awiegman/GeoData ')\n>>>")
            print_dir_contents()
            more = input("(A) press enter continue\n(B) press any other key then enter to link more directories)")
        return(dirs)
    else:
        wd = env.workspace = 'Z:/awiegman/GeoData/Temp'
        print("New environment workspace: ",wd)
        return([wd])


if __name__ == '__main__':
    main(interactive=False)