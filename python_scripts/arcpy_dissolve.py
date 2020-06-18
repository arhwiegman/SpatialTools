# Name: arcpy_dissolve.py
# Description: Dissolve features based on common attributes

 
# Import system modules
import arcpy

arcpy.env.workspace = "C:/data/Portland.gdb/Taxlots"
 
# Set local variables
inFeatures = "taxlots"
tempLayer = "taxlotsLyr"
expression = arcpy.AddFieldDelimiters(inFeatures, "LANDUSE") + " <> ''"
outFeatureClass = "C:/output/output.gdb/taxlots_dissolved"
dissolveFields = ["LANDUSE", "TAXCODE"]
 
# Execute MakeFeatureLayer and SelectLayerByAttribute.  This is only to exclude 
#  features that are not desired in the output.
arcpy.MakeFeatureLayer_management(inFeatures, tempLayer)
arcpy.SelectLayerByAttribute_management(tempLayer, "NEW_SELECTION", expression)
 
# Execute Dissolve using LANDUSE and TAXCODE as Dissolve Fields
arcpy.Dissolve_management(tempLayer, outFeatureClass, dissolveFields, "", 
                          "SINGLE_PART", "DISSOLVE_LINES")