#title: polyClipRaster
#this python program clips a raster file with a polygon 
#author: adrian wiegman
#updated on: 20180409
#useful links:
#https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html


#load modules------------------------------------------
import rasterio
import numpy as np 
from rasterio.plot import show, show_hist
from rasterio.mask import mask
from shapely.geometry import box, Polygon
import geopandas as gpd 
import pandas as pd
from fiona.crs import from_epsg
import pycrs

#define functions--------------------------------------
def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]
#MAIN PROGRAM------------------------------------------

#set up working directories
#raster input path
rst_path = 'C:/Users/Adria/Downloads/SpatialData/LCB-geospatial/VT_geodata_download/VT_ALL_ElevationDEM_DEM10m/'
rst_name = 'dem_10/dblbnd.adf'
#polygon input path
ply_path = 'C:/Users/Adria/Downloads/SpatialData/LCB-geospatial/VT_geodata_download/VT_Subwatershed_Boundaries__HUC12.dbf/'
ply_name = 'VT_Subwatershed_Boundaries__HUC12.dbf'
#clipped raster output path
out_path = "C:/tmp/"
out_name = "test.img"

#load raster file
print ("opening ",rst_name,"...")
rst[i] = rasterio.open((rst_path+rst_name))
show(rst[i])


#load or specify pandas geodataframe polygon 
gdf = gpd.read_file((ply_path+ply_name))
print(gdf.area)

# array to store polygon data
'''
i=0
for f in ply_name: 
	i = i + 1
	print ("opening ",f,"...")
	ply[i] = gpd.read_file((ply_path+f))
	print(ply[i])
'''
#check that CRS is the same between raster and poly
print(gdf.crs)
#reproject polygon if needed
#gdf = gdf.to_crs("+proj=utm +zone=18 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
gdf = gdf.to_crs(crs=rst[0].crs)
ply = [None,None,None]
for i in range(len(ply)): 
	ply[i] = getFeatures(gdf.iloc[[i]]) 

ply

#clip the raster with rasterio mask
for i in range(len(ply)):
	out_img, out_transform = mask(raster=rst[i], shapes=ply[i], crop=True)
	out_meta = rst[i].meta.copy()
	print(out_meta)

	#update metadata
	epsg_code = int(32618) #http://www.spatialreference.org/ref/epsg/wgs-84-utm-zone-18n/
	print(epsg_code)


	out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                  "width": out_img.shape[2],
                  "transform": out_transform,
                  #"crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()}
                          })
    out_file = (out_path + out_name[i])
	with rasterio.open((out_file), "w", **out_meta) as dest:
		dest.write(out_img)
		dest.close()

#check the file by plotting map and histogram
for i in range(len(ply)):
	out_file = (out_path + out_name[i])
	clipped = rasterio.open(out_file)
	show((clipped), cmap='terrain')
	show_hist(clipped)