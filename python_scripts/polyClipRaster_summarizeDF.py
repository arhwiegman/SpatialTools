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
import scipy.stats

#define functions--------------------------------------
def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]
#MAIN PROGRAM------------------------------------------

#set up working directories
#raster input path
rst_path = "E:/GISdata/VTgeodata/OtterData/VTGeologicSoils/rasters/"
rst_path = "E:\\GISdata\\VTgeodata\\OtterData\\NAIP_imagery\\"
rst_path = "E:/GISdata/VTgeodata/OtterData/Lidar_DEMs/"

import glob
import os
os.chdir(rst_path)
#rst_name = glob.glob('*.tif')
rst_name = glob.glob('*.img')
rst_name = glob.glob('*.jp2')
#polygon input path
ply_path = "C:/Users/Adria/Documents/UVM-research/LCB-Geospatial/Otter-analysis/"
ply_name = "nrcs_wetland_easemts_041618_otter.dbf"


#load or specify pandas geodataframe polygon 
gdf = gpd.read_file((ply_path+ply_name))
print(gdf.area)

# create an array of zeros to store results
A = np.zeros([len(gdf),len(rst_name)],dtype=None)
# convert array to Data Frame
DF = pd.DataFrame(A, index=range(len(gdf)), columns=rst_name)


# loop for raster files------------------------------------------------
k=0
#for k in range(len(rst_name)):
for k in range(len(rst_name[:5])):

	#clipped raster output path
	out_path = "C:/Workspace/otterpolyclips/"
	out_name = rst_name[k]

	# create empty list to hold rasters 
	rst = [None]*len(rst_name)
	#load raster file
	print ("opening ",rst_name[k],"...")
	rst[k] = rasterio.open((rst_path+rst_name[k]))
	from osgeo import gdal 
	show(rst[k])

	#reproject polygon if needed
	# rst[k].crs is 'init': 'epsg:32145'
	gdf = gdf.to_crs(crs=rst[k].crs)
	ply = [None]*len(gdf)
	#check that CRS is the same between raster and poly
	print(gdf.crs)


	



	# loop for polygons in shp -------------------------------------------
	#for i in range(len(ply)):
	for i in range(len(ply[:4])):
		ply[i] = getFeatures(gdf.iloc[[i]]) 
		#for i in range(0,1):
		print("processing file",i,"of",len(ply))

		#clip the raster with rasterio mask
		out_img, out_transform = mask(raster=rst[k], shapes=ply[i], crop=True)
		# copy metadata to new file 
		out_meta = rst[k].meta.copy()
		print(i,out_meta)	

		#set projection 
		epsg_code = int(32145) #http://www.spatialreference.org/ref/epsg/nad83-vermont/
		print(epsg_code)

		out_meta.update({"driver": "GTiff",
                 "height": out_img.shape[1],
                  "width": out_img.shape[2],
                  "transform": out_transform,
                  #"crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()}
                          })
    	out_file = out_path + "nrcsid" + str(i) + "_clip_" + out_name
		with rasterio.open((out_file), "w", **out_meta) as dest:
			dest.write(out_img)
			dest.close()
		print("file created:",)

		# open clipped raster
		clipped = rasterio.open(out_file)
		if i<=4:
			#check the file by plotting map and histogram
			show((clipped), cmap='terrain')
			show_hist(clipped)

		# extract and summarize data
		array = clipped.read()
		DF.loc[i,rst_name[k]] = str(scipy.stats.describe(array,axis=None))
	# END i loop --------------------------------------------------------------
#END k loop--------------------------------------------------------------------
print(DF)
DF.to_csv("C:/Users/Adria/Documents/UVM-research/LCB-Geospatial/Otter-analysis/Geologic_SO01_SO02_nrcs_ottersites.csv",sep=";")
%reset #clears global environment from python interpreter






