# Name: mergeRasters
# this script merges raster files using the gdal_merge.py program

#load modules
import glob
import os


#navigate to working directory
folder = ""
path = "C:/Users/awiegman/Downloads/"
os.chdir(path+ folder) 


# list all files in path
files = [f for f in os.listdir(path) if os.path.isfile(f)]

# MEGE LIDAR DATA ---------------------------------------------------------
# select DEM .img files in path with glob
ext = ".img" #file extension
rgx = "Elev*"+ext # search string string, sort of regular expression
file_list = glob.glob(rgx) # glob search files in dir for rgx


# create single string of file names separated by a space
files_string = " ".join(file_list)


#create string containing os comand to run gdal merg
command = "gdal_merge.py -o output.img -of HFA " + files_string


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
	
	#create string containing os comand to run gdal merg
	command = "gdal_merge.py -o output.img -of HFA " + files_string
	
	os.system(command)