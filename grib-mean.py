"""
30 Year mean from 1981 to 2010, Pedram.
"""

#-- define a tic, toc function to check performance
#-- no output? check if the last line that contains the plot function is commented. uncomment for output.

import numpy as np
import Ngl as ngl
import Nio as nio
import datetime
import sys

# === define functions === #

#-- convert time, hours since 1800-01-01
def h2d(hrs):
    tstart = datetime.date(1800,1,1) # Note the change! The grib files start from 1800 instead of 1900
    tdelta = datetime.timedelta(hours=float(hrs))
    res = tstart + tdelta
    return res

#-- get time straight from data table
def gettime(index):
    hrs = f.variables['initial_time0_hours'][index]
    res = h2d(hrs)
    return res

#-- get data according to index
def getdata(index):
    # check which file to read
    f   = nio.open_file(filename,'r')
    # get the data ready
    var = f.variables['SKT_GDS0_SFC_S123'][index,:,:]

    #-- Check the data type, if it's anything other than float64, numpy will complain
    if(var.dtype != 'float64'):
        if db: print('** caution! current data type:','(',var.dtype,'), changing ...')
        var = var.astype('float64')
        if db and (var.dtype == 'float64'):
            print('** success! new data type:',var.dtype)

    # since the data is in K, convert to C
    var = var - 273.15
    return var

# === set variables  === #

#t_f = 12 # time index, from zero to
#t_i = 9 # difference
#-- check if there are any data to take the difference of
try:
    t_i = int(sys.argv[1])
except:
    t_i = None

scalemax = 50
scalemin = -1 * scalemax
scalestep = 2

#-- set filename to read the data from
#-- the data is in absolute form, change it to relative if need be
filename = "copernicus-era5-skt-30-years.grib"

#-- set saved file name
plotname = "30-years-"
plottype = "pdf"
db = True # set debugging mode on or off

# === start calculations  === #

#-- open file and dicover variables
f   = nio.open_file(filename,'r')

#-- check how many datasets are available under different times
print(np.size(f.variables['initial_time0_hours']))
for i in f.variables['initial_time0_hours']:
    print('i =',i,'Date:',h2d(i))

#-- converting time, hours since 1900-01-01
#-- check if there is a time difference available
    
if t_i != None:
    plotname = plotname + str(gettime(t_i))
else:
    plotname = plotname + "theDefault"

if db:
    print('** filename:',filename)
    print('** available variables:')
    for vt in f.variables:
        for at in f.variables[vt].attributes:
            print("f.variables['",vt,"'].attributes['",at,"']",sep='')


#-- just set a default map draw thingy
# TODO: remove this later, or change
if t_i == None:
    t_i = 0
var = getdata(t_i)
lat = f.variables['g0_lat_1'][:]
lon = f.variables['g0_lon_2'][:]

if db:
    print('** var size:', np.size(var))
    print('** lat size:', np.size(lat))
    print('** lon size:', np.size(lon))

#-- resource settings
res = ngl.Resources()
#res.nglDraw         = False #-- don't draw the plot yet
res.nglFrame        = False #-- don't advance the frame yet
res.cnFillOn        = True  #-- turn on color fill
if t_i != None:
    res.cnFillPalette   = "cmp_b2r"    #-- set the colormap to be used
else:
    res.cnFillPalette   = "temp_diff_18lev"    #-- set the colormap to be used

#res.cnFillPalette   = "ncl_default" #-- set the colormap to be used
#res.cnFillPalette   = "NCL-BYR-03" #-- set the colormap to be used
res.cnFillMode      = "RasterFill"
res.cnLineLabelsOn  = False         #-- turn off contour line labels
res.cnLinesOn       = False         #-- turn off contour lines
res.cnInfoLabelOn   = False         #-- turn off contour info labels

res.cnLevelSelectionMode = "ManualLevels" #-- select manual levels
res.cnMinLevelValF  = scalemin #-- minimum contour value
res.cnMaxLevelValF  = scalemax #-- maximum contour value
res.cnLevelSpacingF = scalestep #-- contour increment
res.cnFillDrawOrder = "Predraw" #-- let the mask work!
res.mpGridAndLimbOn = False

res.lbBoxLinesOn    = False
res.lbLabelStride   = 10    #-- skip every other label
#res.pmLabelBarOrthogonalPosF = -0.26 #-- move label upward (how much?)
res.lbLabelFontHeightF  = 0.009     #-- label bar font height
res.lbBoxMinorExtentF   = 0.24      #-- decrease height of labelbar box
res.lbOrientation   = "horizontal"  #-- horizontal labelbar

#-- check if this works
res.mpFillOn        = True
res.mpAreaMaskingOn = True
#res.mpOutlineBoundarySets = "National" #-- draw national borders
#res.mpMaskAreaSpecifiers = ["water"]
res.mpFillAreaSpecifiers = ["water"]
res.mpSpecifiedFillColors= ["gray65"]

#-- make a mask on the map
res.mpLandFillColor = "Transparent"
res.mpOceanFillColor= "gray50"
#res.mpInLandWaterFillColor  = "Gray80"
#res.mpOutlineOn = True
#res.mpGeophysicalLineColor = "gray50"

# res.tiMainString  = "Colors: temperature, Lines: ... "    #-- title string

res.sfXArray        = lon
res.sfYArray        = lat
wks = ngl.open_wks(plottype,plotname)

#-- Check the variable before passing it to contour map plot
if db: print('*** variable type:', type(var),' and shape: ',np.shape(var))

#-- Set the plot name
plotname = f.variables['SKT_GDS0_SFC_S123'].attributes['long_name'] + ' -PS- GRIB -'
#-- check if the data is in a difference or not

#-- create the contour plot
plot = ngl.contour_map(wks,var,res)

#-- write variable long name and units to the plot
txres   = ngl.Resources()
txres.txFontHeightF = 0.012

#-- name the plot
ngl.text_ndc(wks, plotname + '(C). Date: ' + str(gettime(t_i)), 0.50,0.82,txres)

# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
ngl.frame(wks)

ngl.end()
