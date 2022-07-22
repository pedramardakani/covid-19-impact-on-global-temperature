"""
Contour Fill on Maps, Pedram.
"""

#-- define a tic, toc function to check performance
#-- no output? check if the last line that contains the plot function is commented. uncomment for output.

import numpy as np
import Ngl as ngl
import Nio as nio
import datetime
import sys

# === define functions === #

#-- convert time, hours since 1900-01-01
def h2d(hrs):
    tstart = datetime.date(1900,1,1)
    tdelta = datetime.timedelta(hours=float(hrs))
    res = tstart + tdelta
    return res

#-- get time straight from data table
def gettime(index):
    hrs = f.variables['time'][index]
    res = h2d(hrs)
    return res
# === set variables  === #

check_index = int(sys.argv[1])
#t_f = 12 # time index, from zero to
#t_i = 9 # difference
t_f = int(sys.argv[2])
t_i = int(sys.argv[3])

#-- set filename to read the data from
# filename = "adaptor.mars.internal-1587995993.0181034-27757-13-25eca862-11d8-4ecf-97d5-80fe4f17c987.nc"
filename = "/media/pedram/dataStorage/Ped_Doc/Research/myProjects/saeed-shojaei/pyngl/"\
			+"adaptor.mars.internal-1590162992.3450093-30030-25-7410f2f4-da91-4ef7-bf96-c68cda090a23.nc"

plotname = "manual-scale-diff-index-"+str(check_index)+"-"
#plottype = "png"
plottype = "pdf"
db = False # set debugging mode on or off

# === start calculations  === #

#-- open file and dicover variables
f   = nio.open_file(filename,'r')

#-- check how many datasets are available under different times
print(np.size(f.variables['time'].attributes['calendar']))
print(f.variables['time'].attributes['calendar'])
print(f.variables['time'])
for i in f.variables['time']:
    print('i =',i,'Date:',h2d(i))

#-- converting time, hours since 1900-01-01
plotname = plotname + str(gettime(t_f)) + " vs " + str(gettime(t_i))

if db:
    print('** filename:',filename)
    print('** available variables:')
    for vt in f.variables:
        for at in f.variables[vt].attributes:
            print("f.variables['",vt,"'].attributes['",at,"']",sep='')


if db: print('Variable dimensions:', np.shape(f.variables['skt']))

var = f.variables['skt'][t_f,0,check_index,:,:] - f.variables['skt'][t_i,0,check_index,:,:]
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

if db:
    print('** var size:', np.size(var))
    print('** lat size:', np.size(lat))
    print('** lon size:', np.size(lon))

#-- resource settings
res = ngl.Resources()
# res.nglDraw			= False	#-- don't draw the plot yet
res.nglFrame        = False	#-- don't advance the frame yet
res.cnFillOn        = True	#-- turn on color fill
#res.cnFillPalette   = "cmp_b2r"	#-- set the colormap to be used
#res.cnFillPalette   = "ncl_default"	#-- set the colormap to be used
res.cnFillPalette   = "temp_diff_18lev"	#-- set the colormap to be used
#res.cnFillPalette   = "NCL-BYR-03"	#-- set the colormap to be used
res.cnFillMode		= "RasterFill"
res.cnLineLabelsOn  = False			#-- turn off contour line labels
res.cnLinesOn		= False			#-- turn off contour lines
res.cnInfoLabelOn	= False			#-- turn off contour info labels

res.cnLevelSelectionMode = "ManualLevels" #-- select manual levels
res.cnMinLevelValF	= -20.0 #-- minimum contour value
res.cnMaxLevelValF	= +20.0 #-- maximum contour value
res.cnLevelSpacingF	= 1.0	#-- contour increment

res.mpGridAndLimbOn	= False
res.mpOceanFillColor    = "Transparent"

res.lbBoxLinesOn	= False
res.lbLabelStride	= 10	#-- skip every other label
#res.pmLabelBarOrthogonalPosF = -0.26 #-- move label upward (how much?)
res.lbLabelFontHeightF	= 0.009		#-- label bar font height
res.lbBoxMinorExtentF	= 0.24		#-- decrease height of labelbar box
res.lbOrientation   = "horizontal"	#-- horizontal labelbar

# res.tiMainString	= "Colors: temperature, Lines: ... "	#-- title string

res.sfXArray        = lon
res.sfYArray        = lat
wks = ngl.open_wks(plottype,plotname)

#-- Check the data type, if it's anything other than float64, numpy will complain
if(var.dtype != 'float64'):
    if db: print('** caution! current data type:','(',var.dtype,'), changing ...')
    var = var.astype('float64')
    if db and (var.dtype == 'float64'):
        print('** success! new data type:',var.dtype)

#-- Check if there are scale factors involved
sf = f.variables['skt'].attributes['scale_factor']
if(sf != None):
    if db:
        print('** scale factor detected:',sf)
        print('** scale factor type:', type(sf))
    var = var * np.array(sf)

#-- Check the variable before passing it to contour map plot
if db: print('*** variable type:', type(var),' and shape: ',np.shape(var))

#-- Check if there are offset values available
os = f.variables['skt'].attributes['add_offset']
if(os != None):
    if db:
        print('** offset value detected:',os)
        print('** offset value:',type(os))
    # === what should we do with the offset? === #

#-- Set the plot name
plotname = f.variables['skt'].attributes['long_name'] + ' -PS- index ' + str(check_index) + '-'

#-- create the contour plot
plot = ngl.contour_map(wks,var,res)

#-- write variable long name and units to the plot
txres   = ngl.Resources()
txres.txFontHeightF = 0.012
ngl.text_ndc(wks, plotname + '(C). Date: ' + str(gettime(t_f)) + " vs " + str(gettime(t_i)), 0.50,0.82,txres)

# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
ngl.frame(wks)

ngl.end()
