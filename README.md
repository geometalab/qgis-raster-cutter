# Raster Cutter
***

![](docs/screenshot.png)

Raster Cutter is a QGIS Plugin developed in Python and QT. It allows the user to select a raster layer from his project, set an extent and export the raster data within this extent to a `.jpg` or `.png` image file. 

Additionally, the plugin can create a Worldfile and/or Lexocad sidecar file if desired. The plugin also supports re-projection into other Coordinate Reference Systems.

### Using this tool

1. Start QGIS - install QGIS plugin 'Raster Cutter' if necessary - and open "New Project".
2. Set the QGIS project to the CRS "EPSG:2056" (= Swiss coordinate reference system CH/LV95) (bottom right).
3. If necessary, load background/base map (e.g. OpenStreetMap or MapGeoAdmin). Make sure that the CRS is still "EPSG:2056". 
4. Load raster file/data source (= input layer) (WMS, WMTS/XYZ/TMS, GeoTIFF) and zoom to the desired section. 
5. Open the dialog of the 'Raster Cutter' plugin and define the necessary parameters:
   1. choose the input layer (if not already selected)
   2. set the extent by clicking on "Map Canvas Extent". 
   3. Set the path and name of the output and the output format (GeoTIFF, PNG or JPG).
   4. If desired, check the "Create LexoCAD" checkbox to generate LexoCAD georeference files.
6. Set additional parameters if necessary (for advanced users): CRS and Output resolution. 
7. finished (load and view with QGIS or Lexocad).

(Translated from https://md.coredump.ch/2H-jGnDTSbuBk7ai0xWIxA?view#Bedienungsanleitung)

### Set up local developement

If you want to continue developing this tool on your own, you will need the following:
* Python
* QGIS (contained in [OSGEO4W](https://www.osgeo.org/projects/osgeo4w/))
* Qt Designer (if you want to update the UI) (contained in [OSGEO4W](https://www.osgeo.org/projects/osgeo4w/))
* Plugin Build Tool ([pb_tool](https://g-sherman.github.io/plugin_build_tool/))

