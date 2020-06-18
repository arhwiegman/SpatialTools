# arcpy_Raster2otherFormat.py
# Raster To Other Format
# Usage: RasterToOtherFormat_conversion Input_Rasters;Input_Rasters... Output_Workspace 
# Formats:
# {TIFF | BIL | BIP | BMP | BSQ | ENVI DAT | GIF | GRID | IMAGINE Image | JP2000 | JPEG | PNG}


# DEFINE FUNCTIONS ####################################################

# arcpyWorkspace ------------------------------------------------------
# sets arcpy.env.workspace and os.dir in specified path
def arcpySession (path = "C:/temp/"):
	import arcpy
	import os
	os.chdir(path)
	arcpy.env.workspace = path
	
	
# globSelectFiles -----------------------------------------------------
# selects files from glob matching specified pattern
def globSelectFiles (pattern="*")
	import glob.glob as glb
	return(glb(pattern))

	
# ReformatRaster ---------------------------------------------------
# converts list of raster files to a single format in specified path
# inFilesList: list of files e.g.
#                       files = ['file.img',file2.jpg','file3.gif']
# inFilesList: list of files e.g.
#                       files = ['file.img',file2.jpg','file3.gif']

def ReformatRaster (inFilesList,outPath="C:/temp/",Format="TIFF"):
	inFileString = ';'.join(map(str, myList)) 
	try:
		##Convert Multiple Raster Dataset to FGDB
		arcpy.RasterToOtherFormat_conversion(inFileString,outPath,Format)
		#http://resources.arcgis.com/en/help/main/10.1/index.html#//001200000032000000
		
	except:
		print "Raster To Other Format Failed."
		print arcpy.GetMessages()

		
# MAIN PROGRAM ###########################################################


	
