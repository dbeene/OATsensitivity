# Modules
import arcpy
from arcpy import env
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
arcpy.env.overwriteOutput = True
# Workspace
arcpy.env.workspace = r'' ##User-defined workspace

# Raster locations - user-defined.
landforms = Raster(arcpy.env.workspace+'')
proximity = Raster(arcpy.env.workspace+'')
TWE = Raster(arcpy.env.workspace+'')
windIndex = Raster(arcpy.env.workspace+'')

# Populate tuples of rasters and weights.
rtups = (
        (landforms,0.25),
        (proximity,0.25),
        (TWE,0.25),
        (windIndex,0.25)
        )
# Empty list to populate with adjusted sensitivity coefficients
senslist = [0.0,0.0,0.0,0.0]

# Recalculate values in sensitivity list according to +/-10% change to first coefficient
rasterlist = []
for r in rtups:
    rasterlist.append(r[0])
weightlist = []
for w in rtups:
    weightlist.append(w[1])
for pct in range(-20, 21, 5):
    senslist[0] = weightlist[0]*((100+pct)/100.0)
    for i in range(1, len(weightlist)):
        senslist[i] = ((1-senslist[0])*(weightlist[i])/(1-weightlist[0]))

    # Sort rasterlist by order list
    order=[0,1,2,3] # Make order list same length as rasterlist -- need to figure out way to automate order list based on length of rasterlist
    for i in range(len(order)):
        neworder=order[i:]+order[:i]
        orasterlist = [rasterlist[i] for i in neworder]
        # Loop through orasterlist and multiply by senslist
        r0 = orasterlist[0]*senslist[0]
        r1 = orasterlist[1]*senslist[1]
        r2 = orasterlist[2]*senslist[2]
        r3 = orasterlist[3]*senslist[3]
        # Overlay rasters
        overlay = r0+r1+r2+r3
        overlay.save(str(orasterlist[0])[:-4]+str(pct)+'.tif')
