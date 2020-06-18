# splitShapefileByFeature.py
# Script created to separate one shapefile in multiple ones by one specific
# attribute

# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"
import arcgisscripting

# Starts Geoprocessing
gp = arcgisscripting.create(9.3)
gp.OverWriteOutput = 1

#Set Input Output variables
inDir = "C:\\Users\\awiegman\\Downloads\\OtterData\\NRCS_easements_OtterCreek\\"
inputFile = inDir + "Points.shp"
outDir = "C:\\Users\\awiegman\\Downloads\\OtterData\\NRCS_easements_OtterCreek\\idPoints\\"

# Make the outDir if it doesn't already exist using os
import os 
if not os.path.isdir(outDir):
	os.mkdir(outDir)

# Reads Shapefile for different values in the attribute
rows = gp.searchcursor(inputFile)
row = rows.next()
attribute_types = set([])

while row:
    attribute_types.add(row.Name) #<-- CHANGE my_attribute to the name of your attribute
    row = rows.next()

# Output a Shapefile for each different attribute
for each_attribute in attribute_types:
    outSHP = outDir + each_attribute + u".shp"
    print outSHP
    gp.Select_analysis (inputFile, outSHP, "\"Name\" = '" + each_attribute + "'") #<-- CHANGE my_attribute to the name of your attribute

del rows, row, attribute_types, gp

#END