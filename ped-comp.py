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

# === set variables  === #

#-- set filename to read the data from
filename = "data-comp.nc"
plotname = "test"
plottype = "png"
db = True # set debugging mode on or off

# === start calculations  === #

#-- open file and dicover variables
f   = nio.open_file(filename,'r')

#-- Check the variable shapes. Prevent contour plot from complaining
# about the shape. This happened because of the difference between
# different data structures in the `x.nc` data files. For example,
# one data-set may contain only data worth of one month, another
# one may contain several months, and another one may contain data
# worth of several years! This will introduce different layers of
# data. Hence, the inconsistency between dimensions.
#-- The programmer is advised to have a good grasp of the data-sets,
# and use a method accordingly. The `if` function below will help
# with better understanding the data-set shape for valid data
# recollection and usage.
if db:
    print('** skin temperature details:')
    print('############################')
    print(f.variables['skt'])
    print('############################')
    print(np.shape(f.variables['skt']))
    print('** filename:',filename)
    print('** available variables:')
    for vt in f.variables:
        for at in f.variables[vt].attributes:
            print("f.variables['",vt,"'].attributes['",at,"']",sep='')

#-- check how many datasets are available under different times
print(np.size(f.variables['time'].attributes['calendar']))
print(f.variables['time'].attributes['calendar'])
print(f.variables['time'])
for i in f.variables['time']:
    print('i =',i,'Date:',h2d(i))

#-- converting time, hours since 1900-01-01
# time index, from zero to
t_i = 0
# this will count how many `time` tables are available:
t_f = np.shape(f.variables['skt'])[0]
hrs = f.variables['time'][t_i]
t_date = h2d(hrs)
plotname = plotname + str(t_date)

#-- Knowing the dimensions, now we can recall useful data:
var = f.variables['skt'][t_i,0,0,:,:]
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

#-- Recheck the variables shapes in debug mode:
if db:
    print('** var shape:', np.shape(var))
    print('** lat shape:', np.shape(lat))
    print('** lon shape:', np.shape(lon))

#-- resource settings
res = ngl.Resources()
res.nglFrame        = False
res.cnFillOn        = True
res.cnFillPalette   = "NCL_default"
res.cnLineLabelsOn  = False
res.lbOrientation   = "horizontal"
res.sfXArray        = lon
res.sfYArray        = lat
wks = ngl.open_wks(plottype,plotname)

if db : print('** converting time:',hrs,'to Date:', t_date)

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
ngl.text_ndc(wks, plotname + 'In degrees Celsius. Data date: ' + str(t_date) , 0.50,0.82,txres)

# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
ngl.frame(wks)

ngl.end()
