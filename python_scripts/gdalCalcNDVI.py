# gdalCalcNDVI
# https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html

# LOAD LIBRARIES ------------------------
from osgeo import gdal # for spatial read/write
import glob # for searching working directory
import os # for system commands

# SET DIRECTORY
path = "C:/Users/awiegman/Downloads/"
os.chdir(path)

# OPEN RASTER
gtif = gdal.Open( "INPUT.tif" )
print gtif.GetMetadata()

# CALCULATE NDVI ---------------------------------------------------------

Years = ["2008","2011","2012","2014","2016"] # list of years
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
	
