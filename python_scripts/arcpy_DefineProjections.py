# Name: DefineProjection.py 
# Description: Records the coordinate system information for the specified input dataset or feature class

# DEFINED FUNCTIONS --------------------------------------
# defineProjections ######################################
# defines projections on a list of files using a template

def defineProjections(inFiles=["Points"],template="elevation"):
	# get the coordinate system by describing a feature class
	dsc = arcpy.Describe(template)
	coord_sys = dsc.spatialReference
		# run the tool for the list of files
	for file in inFiles:
		try:		
			arcpy.DefineProjection_management(file, coord_sys)
		# print messages when the tool runs successfully
			print(arcpy.GetMessages(0))
		except arcpy.ExecuteError:
			print(arcpy.GetMessages(2))
		except Exception as ex:
			print(ex.args[0])

# MAIN PROGRAM ------------------------------------------
# import system modules
import arcpy
import os 

# set workspace environment
arcpy.env.workspace = "C:/Temp/data"

# call function define projections
defineProjections()
	
