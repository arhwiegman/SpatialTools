#!/usr/bin/python3.6.3
##################METADATA#####################
# Name: gdalMergeRasters_dem_naipdata.py
#
# this script merges raster files using the gdal_merge.py program
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!! IMPORTANT: make sure to put a copy of !!!!
# !!!! gdal_merge in the working directory   !!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
# Author: Adrian Wiegman
# Date: 20180515
###############################################

# PRELIMINARIES -----------------------------------------------------
#load modules
import glob
import os

#navigate to working directory
folder = ""
path = "C:/Workspace/OtterData/"
os.chdir(path+ folder) 

# download_gdalMergePy ----------------------------------------------
# downloads gdal_merge.py into working directory from git hub 
def download_gdalMergePy(directory=None):
    import requests
    from os import getcwd
    url = "https://raw.githubusercontent.com/geobox-infrastructure/gbi-client/master/app/geobox/lib/gdal_merge.py"
    if directory == None: directory = getcwd()
    filename =  path + 'gdal_merge.py'
    r = requests.get(url)
    f = open(filename,'w')
    f.write(r.text)
    f.close
    glob.glob("gdal_merge.py")

#--------------------------------------------------------------------

# list all files in path
# files = [f for f in os.listdir(path) if os.path.isfile(f)]

# MEGE LIDAR DATA ---------------------------------------------------------
# select DEM .img files in path with glob
ext = ".img" #file extension
rgx = "Elev*"+ext # search string string, sort of regular expression
file_list = glob.glob(rgx) # glob search files in dir for rgx


# create single string of file names separated by a space
files_string = " ".join(file_list)

output = 'output_middleOtter_Elev_0.7mLidar2012'
#create string containing os comand to run gdal merg
command = "gdal_merge.py -o "+ output +".img -of HFA " + files_string


os.system(command)

# MERGE NAIP DATA ---------------------------------------------------------

Years = ["2003","2008","2011","2012","2014","2016"] # list of years
ext = ".jp2" #file extension

for i in range(len(Years)):
	print("processing "+Years[i]+" NAIP data...")
	# select NAIP .jp2 files in path with glob
	rgx = "*"+Years[i]+"*"+ext # search string, sort of regular expression
	file_list = glob.glob(rgx) # glob search files in dir for rgx
	
	# create single string of file names separated by a space
	files_string = " ".join(file_list)
	output = 'output_middleOtter_colorbands'+Years[i]

	#create string containing os comand to run gdal merge
	command = "gdal_merge.py -o "+ output +".img -of HFA " + files_string
	#print(command)
	os.system(command)