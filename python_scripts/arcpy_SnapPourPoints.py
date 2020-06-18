# Name: arcpy_Watershed_points.py
# Description: Determines the contributing area above a set of cells in a
#     raster.
# Requirements: Spatial Analyst Extension

# Import system modules
import arcpy
from arcpy import env
from arcpy.sa import *

# Set local variables
inFlowDirection = "C:\\Users\\awiegman\\Downloads\\OtterData\\ElevationDEM_VTHYDRODEM\\OtterCreek\\FlowDir"
import glob
import os 
os.chdir("C:\\Users\\awiegman\\Downloads\\OtterData\\NRCS_easements_OtterCreek\\idPoints\\")
inPointPath = "C:\\Users\\awiegman\\Downloads\\OtterData\\NRCS_easements_OtterCreek\\idPoints\\"
inPointFiles = glob.glob("*.shp")
inPourPointField = "FID"


# Set local variables
inPourPoint = "pourpoint"
inFlowAccum = "flowaccumulation.img"
tolerance = 5
pourField = "VALUE"

# Execute SnapPourPoints
outSnapPour = SnapPourPoint(inPourPoint, inFlowAccum, tolerance, 
                            pourField) 

# Save the output 
outSnapPour.save("c:/sapyexamples/output/outsnpprpnt02")

# Set environment settings
outDir = "C:\\Users\\awiegman\\Downloads\\OtterData\\NRCS_easements_OtterCreek\\idPoints\\"
if not os.path.isdir(outDir): 
	os.mkdir(outDir)
env.workspace = outDir

# Batch process watershed creation
for file in inPointFiles[0:2]:
	inPourPointData = inPointPath + file
	print("processing watershed for point file =",file)
	outWatershed = Watershed(inFlowDirection, inPourPointData, inPourPointField)
	outfile =  "watershed_" + file[2:(len(file)-4)]
	print("saving output... file =",outfile)
	#outWatershed.save(outfile)
	#del outWatershed 