# Name: arcpy_AddJoinByField.py
# Joins two attribute tables based on a specified field
# http://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-join.htm

import arcpy 
arcpy.env.workspace = "C:/temp/data/"

inLayer = "snappoints" # extensionless name of file 
inField = "FID" # name of attribute table field to join 
joinTable = "points" # extensionless name of file
joinField = inField 
arcpy.AddJoin_management (inLayer, inField, joinTable, joinField)