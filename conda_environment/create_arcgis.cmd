REM Must be run as Administrator due to the commands modfying a file in the "C:\Program Files" directory
REM Sets up channels in the "C:\Program Files\ArcGIS\Pro\bin\Python\.condarc" file
REM This is required so ArcGIS Pro will recognize the packages we are adding
CALL conda config --add channels conda-forge
CALL conda config --add channels esri
CALL conda config --add channels knu2xs