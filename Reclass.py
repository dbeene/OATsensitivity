# Import modules, set environments
import arcpy
import sys
from arcpy import env
from arcpy.sa import *
from arcpy.da import *
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
arcpy.env.workspace = r'' #User define workspace, should be output from OAT runs
# List rasters
rasterlist = arcpy.ListRasters()
# For raster in rasterlist:
for raster in rasterlist:
    # Reclassify by table
    remap = r'' # User-defined...see 'remap.csv' in repo for formatting
    outreclass = ReclassByTable(raster, remap, "FROM", "TO", "OUTPUT")
    # Use SearchCursor to populate new table
    arcpy.BuildRasterAttributeTable_management(outreclass, "Overwrite")
    outfile = open(r"E:\P50LocalTemp\P50LocalTemp\Sensitivity\pixelcount_april.txt", 'a')
    rows = arcpy.SearchCursor(outreclass, "", "", "Value;Count", "")
    outfile.write(str(raster) + "\n")
    for row in rows:
        val = row.getValue("Value")
        count = row.getValue("Count")
        print val, count  # Need to change this to output value/count to csv
        outfile.write(str(count) + ", ")
    outfile.write("\n")
    outfile.close()


