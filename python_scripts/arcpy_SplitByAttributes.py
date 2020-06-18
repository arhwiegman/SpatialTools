# Name: arcpy_SplitByAttributes.py
# Description: Use the SplitByAttributes tool to split a feature class by unique values.

# Import required modules
import arcpy

# Set local variables
in_feature_class = 'c:/data/base.gdb/ecology'
target_workspace = 'c:/data/output.gdb'
fields = ['REGION', 'ECO_CODE']

arcpy.SplitByAttributes_analysis(in_feature_class, target_workspace, fields)