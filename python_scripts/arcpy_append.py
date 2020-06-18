# Name: Append.py
# Description: Use the Append tool to combine several shapefiles
# http://pro.arcgis.com/en/pro-app/tool-reference/data-management/append.htm

# import system modules 
import arcpy
import os 

# Set environment settings
arcpy.env.workspace = "C:/users/awiegman/Downloads/VTGeologicSoils/"

# Set local variables
outLocation = "C:/Users/awiegman/Downloads/VTGeologicSoils/rasters/"
outName = "Geologic_SO01_SO21_poly.shp"
schemaType = "NO_TEST"
fieldMappings = ""
subtype = ""
fileTemplate = "Geologic_SO01_poly.shp"
spatialReference =arcpy.Describe(fileTemplate).spatialReference


# Process:  Create a new empty feature class to append shapefiles into
emptyFC = arcpy.CreateFeatureclass_management(out_path = outLocation, out_name = outName, geometry_type="POLYGON", 
                                              template=fileTemplate,spatial_reference=spatialReference)

# We want a list of all polygon FCs in the workspace to append to the shape
fcList = arcpy.ListFeatureClasses("", "POLYGON")

# Create FieldMappings object to manage merge output fields
fieldMappings = arcpy.FieldMappings()

# Add the target table to the field mappings class to set the schema
fieldMappings.addTable(emptyFC)

# List attribute labels
attribute_Labels = ["MUSYM","MUID","MUKEY","MUID",
					"Kw","TFACTOR","PARENT","PARENTSUB",
					"ROCKDEEP","SLOPELOW","SLOPEHIGH",
					"ROCKSHALLO","WATERSHALL","WATERDEEP",
					"HYDROGROUP","FORSTGRP","FORSTVAL"]
# Add fields in loop over list of attributes
for i in range(len(attribute_Labels)):
	print(i,attribute_Labels[i])
	# Create FieldMap object
	fldMap = arcpy.FieldMap()
	# Add input fields
	fldMap.addInputField("Geologic_SO01_poly.shp", attribute_Labels[i])
	fldMap.addInputField("Geologic_SO21_poly.shp", attribute_Labels[i])
	
	# Set the output field properties for both FieldMap objects
	attr_name = fldMap.outputField
	attr_name.name = attribute_Labels[i]
	fldMap.outputField = attr_name
	
	# Add output field to field mappings object
	fieldMappings.addFieldMap(fldMap)

    
"""	THE CODE BELOW IS NOT WORKIN RIGHT NOW
# using arcpy.ListFields 	
for field in arcpy.ListFields("Geologic_SO01_poly.shp"):
	fldMap.addInputField("Geologic_SO01_poly.shp", field.name)
	fldMap.addInputField("Geologic_SO21_poly.shp", field.name)
"""

emptyPath = 'C:/Users/awiegman/Downloads/VTGeologicSoils/rasters/Geologic_SO01_SO21_poly.shp'
# Process: Append the feature classes into the empty feature class
arcpy.Append_management(fcList, emptyFC, schemaType, 
                        fieldMappings, subtype)