# Name: mergeRasters
# this script merges raster files using the gdal_merge.py program

#load modules

import glob

import os



#navigate to working directory

folder = "LewisCreek/"

path = "C:/Users/Adria/Downloads/SpatialData/LCB-geospatial/VT_geodata_download/HydroEnforcedDEM/"

os.chdir(path+ folder) 



#select files based on some regular expression search

ext = ".img" #file extension

file_list = glob.glob(".*"+ext)

files_string = " ".join(file_list)



#create string containing os comand to run gdal merge

command = "gdal_merge.py -o output.img -of HFA " + files_string



os.system(command)