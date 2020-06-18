# Name: arcpy_SelectFeature.py
# Description: Select a feature with a specific value from attribute table and create new Shapefile

# Import system modules
import arcpy
from arcpy import env

# Set workspace
env.workspace  = u"C:\\Users\\awiegman\\Downloads\\"

# Set local variables
in_features = "VT_Subbasin_Boundaries__HUC8\\VT_Subbasin_Boundaries__HUC8.shp"
out_feature_class = "VT_Subbasin_Boundaries__HUC8\\Subbasin_Shapes\\OtterCreek.shp"
where_clause = '"Name" = \'Otter Creek\''

# Execute Select
arcpy.Select_analysis(in_features, out_feature_class, where_clause)