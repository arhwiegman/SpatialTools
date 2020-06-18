# generates a curl command to download a file github repository
# https://developer.github.com/v3/#authentication
# https://developer.github.com/v3/repos/contents/
import requests
gitraw = "https://raw.githubusercontent.com/arhwiegman/UVM-research/master/LCB-Geospatial/Otter-analysis/Python_scripts/arcpy_Functions.py?token=AfPESufaTu9wOfhxljwHUbWNGAvSVRSeks5bF_LawA%3D%3D"
r = requests.get(gitraw)
print(r.text)

#from arcpy_Functions import *

'''
password = input('enter password')
command = 


token = "2841b272c98d2d091672bd760e34cb71f7d3898e"

CURL = "curl -H 'Authorization: token 2841b272c98d2d091672bd760e34cb71f7d3898e'-H 'Accept: application/vnd.github.v3.raw' -O -L https://api.github.com/repos/arhwiegman/UVM-research/LCB-Geospatial/Otter-analysis/Python_scripts/arcpy_Functions.py"

'''