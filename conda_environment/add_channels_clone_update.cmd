REM Must be run as Administrator due to the commands modfying a file in the "C:\Program Files" directory
REM Sets up channels in the "C:\Program Files\ArcGIS\Pro\bin\Python\.condarc" file
REM This is required so ArcGIS Pro will recognize the packages we are adding
CALL conda config --add channels conda-forge
CALL conda config --add channels esri
CALL conda config --add channels knu2xs

REM Run this from the ArcGIS Python Command Prompt
REM Clone and activate the new environment
REM CALL conda create --name arcgispro-py3-clone --clone arcgispro-py3
CALL activate arcgispro-py3-clone

REM Install additional packages
CALL conda env update -f environment.yml

REM Additional steps for the map widget to work in Jupyter Lab
jupyter labextension install @jupyter-widgets/jupyterlab-manager -y
jupyter labextension install arcgis-map-ipywidget@1.8.2 -y