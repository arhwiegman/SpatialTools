# The objective of this script is to randomly select sample locations
# at NRCS easements
# %% 1. LOAD MODULES (This is a cell)
# 
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Polygon, Point
import geopandas as gpd
import os, glob
from osgeo import gdal

# %% USER DEFINED FUNCTIONS 
# download functions arcpy_Functions.py from github
# if running entire script make sure main and functions are in same directory
# set the current directory to folder containing function script
os.chdir('C:/Users/Adria/Documents/UVM-research/LCB-Geospatial/Otter-analysis/Python_scripts')
# if you need to download arcpy_Functions.py then use code in block quotes below 
from arcpy_Functions import*
defLookup() #lookup defined functions code with defLookup



# %% 3. OPEN FILES AND DECLARE GLOBAL VARIABLES
# set the current directory to folder containing data
os.chdir('C:\\Workspace\\Circles')
name1 = 'priority_sites.shp' # name of easement shapefile
name2 = 'Q1p5_24Apr2018.shp' # name of inundation shapefile
gdf1 = gpd.read_file(name1) # read_file with gpd is same as fiona.open
gdf2 = gpd.read_file(name2) # 
#easements.plot()
#inundation.plot()
srs = 'epsg:26918' #NAD83 Zone 18N

# %% 4. REPROJECT DATA
# set data to coordinate reference system of equal area in meters
gdf1.to_crs({'init': srs})
gdf2.to_crs({'init': srs})


# %% MANIPULATE INUNDATION BOUNDARY GEOMETRY
gdf2.geometry = gdf2.geometry.buffer(0.0) # to remove intersecting rings

# %% 6. CACLULATE INTERSECTION 
# new layer from intersection of inundation boundary and sampling area
#SamplingZone = easements['geometry'].intersection(inundation)
#SamplingZone.plot()
SamplingZone = gpd.overlay(gdf1,gdf2,'intersection')

# %% 7. GENERATE random circles inside the sampling zone

SampleCircles = [randomCirclesInsidePoly(g) for g in SamplingZone.geometry]
gdf3 = gdf1 #create new dataframe with gdf1 as template
gdf3.geometry = SampleCircles # set geometry of gdf3 as circles

# %% 8. PLOT sample CIRCLES
gdf3.plot()

# %% 9. Merge files
os.chdir('D:\\GISdata\\UVM_Temp\\rawdata')
searches = ["2008","2012","2011","2003","2014","2016"]
for s in searches:
    rasters = glob.glob("*"+s+"*.jp2")
    print(s,rasters)
    gdal_merge(rasterList = rasters,outFile="NAIP"+s+".tif")

# %% TRY MOSAIC RASTERS WITH GDAL_MERGE.PY
    
import os, glob
os.chdir("C:/Workspace/Python_scripts")
from wiegman_gis_functions import *
os.chdir("C:/Workspace/rawdata")
download_gdalMergePy()

searches = [2003,2008,2011,2012,2014,2016]
searches = [str(s) for s in searches]
results = [glob.glob("*"+s+"*.jp2") for s in searches]

for i in range(len(results[:1])):
    outFile = "NAIP"+searches[i]+".tif"
    inFiles = " ".join(results[i])
    cmd = "gdalwarp -of Gtiff -t_srs 'EPSG:26918' -o %s %s" % (outFile,inFiles)
    print (cmd)
    os.system(cmd)
    print(outFile," created!")

# %% 
# Create lines from lat and lon coordinates 
# lat lon from dec sample sites
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString, MultiPoint, Point
import matplotlib.pyplot as plt
# points (lon,lat) (x,y)

# (*&^*&%^&^%^%$$^#$^ NEED TO INSERT MODULE TO READ IN Coordinate as pandas DataFrame FROM .csv file

coords = [[(-73.15871583,44.56705639),(-73.15865167,44.56698944),(-73.15865167,44.56693167)],# n=1, id = MF, name="Munsen flat"
          [(-73.15497,43.96883),(-73.15478,43.96903)],# n=2, id = 3MB, name="3 mile bridge"
          [(-73.05466,43.4411),(-73.05437,43.74397)],# n=3, id = PO, name="Pomainville WMA" 
          [(-73.16373,43.94735),(-73.1637,43.94709)],# n=4, id = GO, name="Goodrich"
          [(-73.06694,43.65484),(-73.06698,43.65517)]# n=5, id = RO, name="Roche"
          ]

points = [MultiPoint(p) for p in coords]
print(points)
points_gdf = gpd.GeoDataFrame()
points_gdf.crs = {"init":"EPSG:4326"}
print(points_gdf.crs)
points_gdf.geometry = points
print(points_gdf)

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world.to_crs = {"init":"EPSG:4326"}
# We restrict to North America.
ax = world[world.continent == 'North America'].plot(
    color='white', edgecolor='black')
# We can now plot our GeoDataFrame.
points_gdf.plot(ax=ax, color='red')
plt.show()

# create LineString geometry and convert to geodataframe
lines =  [LineString(p) for p in coords]
lines_gdf = gpd.GeoDataFrame()
lines_gdf.geometry = points

