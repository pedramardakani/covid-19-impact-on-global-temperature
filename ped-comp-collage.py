"""
Contour Fill on Maps, Pedram.
"""

#-- define a tic, toc function to check performance
#-- no output? check if the last line that contains the plot function is commented. uncomment for output.

import numpy as np
import Ngl as ngl
import Nio as nio
import datetime

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

#-- get the difference between two dates
#-- pay attention to argument placements
def getdiff(t_f,t_i):
    # check if available (later)
    return f.variables['skt'][t_f,0,:,:] - f.variables['skt'][t_i,0,:,:]

# === set variables  === #

#-- set filename to read the data from
filename = "data-comp.nc"
plotname = "collage"
plottype = "png"
db = False # set debugging mode on or off

# === start calculations  === #

#-- open file
f   = nio.open_file(filename,'r')

#-- start the graphics
wks = ngl.open_wks(plottype,plotname)

#-- resource settings
res = ngl.Resources()
res.nglFrame        = False
res.cnFillOn        = True
res.cnFillPalette   = "NCL_default"
res.cnLineLabelsOn  = False
res.lbOrientation   = "horizontal"
res.sfXArray        = lon
res.sfYArray        = lat

#-- converting time, hours since 1900-01-01
t_f = 6 # time index, from zero to
t_i = 3 # difference
plotname = plotname + str(gettime(t_f)) + " vs " + str(gettime(t_i))

if db:
    print('** filename:',filename)
    print('** available variables:')
    for vt in f.variables:
        for at in f.variables[vt].attributes:
            print("f.variables['",vt,"'].attributes['",at,"']",sep='')

var = getdiff(t_f,t_i)
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

if db:
    print('** var size:', np.size(var))
    print('** lat size:', np.size(lat))
    print('** lon size:', np.size(lon))


if db : print('** converting time:',hrs,'to Date:', gettime(t_i))

#-- check how many datasets are available under different times
print(np.size(f.variables['time'].attributes['calendar']))
print(f.variables['time'].attributes['calendar'])
print(f.variables['time'])
for i in f.variables['time']:
    print('i =',i,'Date:',h2d(i))

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

#-- Check if there are offset values available
os = f.variables['skt'].attributes['add_offset']
if(os != None):
    if db:
        print('** offset value detected:',os)
        print('** offset value:',type(os))
    # === what should we do with the offset? === #

#-- Set the plot name
plotname = f.variables['skt'].attributes['long_name'] + 'by Pedram, for Dear Saeed.'

#-- create the contour plot
plot = ngl.contour_map(wks,var,res)

#-- write variable long name and units to the plot
txres   = ngl.Resources()
txres.txFontHeightF = 0.012
ngl.text_ndc(wks, plotname + 'In degrees Celsius. Date: ' + str(gettime(t_f)) + " vs " + str(gettime(t_i)) , 0.50,0.82,txres)

# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
ngl.frame(wks)

ngl.end()
