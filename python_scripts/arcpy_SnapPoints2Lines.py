# Name: arcpy_SnapPoints2Lines.py
# Description: Snap climate regions boundary to vegetation layer boundary 
#                    to ensure common boundary is coincident


# import system modules 
import arcpy

# Set environment settings
arcpy.env.workspace = "C:\\Users\\awiegman\\Downloads\\OtterData\\"

# Make backup copy of climate regions feature class, since modification with 
#  the Editing tools below is permanent
points = "NRCS_easements_OtterCreek\\Points.shp"
import os 
if not os.path.exists("C:/Temp/pointsBackup.shp"):
	pointsBackup = "C:/Temp/pointsBackup.shp"
	arcpy.CopyFeatures_management(points, pointsBackup)

"""
# Densify climate regions feature class to make sure there are enough vertices 
#  to match detail of vegetation layer when layers are snapped
arcpy.Densify_edit(climate, "DISTANCE", "10 Feet")
"""

# Snap climate regions feature class to vegetation layer vertices and edge
lines = "MajorStreams\\MajorStreams.shp"
# first, snap climate region vertices to the nearest vegetation layer vertex within 30 Feet
snapEnv1 = [lines, "VERTEX", "50 meters"]
# second, snap climate region vertices to the nearest vegetation layer edge within 20 Feet
#snapEnv2 = [veg, "EDGE", "20 Feet"]
arcpy.Snap_edit(points, [snapEnv1]) # expects a list of environments