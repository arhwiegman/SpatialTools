# Name: arcpy_Clip.py
# Description: Clip major roads that fall within the study area. 

# Import system modules
import arcpy
from arcpy import env

# Set workspace
env.workspace  = u"C:\\Users\\awiegman\\Downloads\\"

# Set local variables
in_features = "VT_Subbasin_Boundaries__HUC12\\VT_Subbasin_Boundaries__HUC12.shp"
clip_features = "VT_Subbasin_Boundaries__HUC8\\VT_Subbasin_Boundaries__HUC8.shp"
out_feature_class = "C:\\Users\\awiegman\\Downloads\\VT_Subbasin_Boundaries__HUC12\\OtterCreek.shp"
xy_tolerance = ""

# Execute Clip
arcpy.Clip_analysis(in_features, clip_features, out_feature_class, xy_tolerance)