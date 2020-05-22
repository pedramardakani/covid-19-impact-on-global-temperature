"""
Contour Fill on Maps, Pedram.

Trying to make this code a modular one, in order to plot files easier.
"""

#-- define a tic, toc function to check performance
#-- no output? check if the last line that contains the plot function
# is commented. uncomment for output.

import numpy as np
import Ngl as ngl
import Nio as nio
import datetime
from sys import argv as av # get input right on the command line

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
    return str(res)

#-- convert data to float64 for numpy compatiblility
# and get the product from scale factor
def getdata(time):
    # Fetch the data based on the data-set architecture
    # NOTE: Because of the bug in the datasets, we'll use
    # a different architecture for time value larger than 17 - which
    # means for the `time-tables` 18 and 19.
    if(time < 18):
        var = f.variables['skt'][time,0,0,:,:]
    else:
        # NOTE: `ff` is another file!
        time = 18 - time # correct the index for the new file
        var = ff.variables['skt'][time,0,:,:]
    # Change to float64
    var = var.astype('float64')
    # Check scale
    sf = f.variables['skt'].attributes['scale_factor']
    # Apply the scale
    var = var * np.array(sf)
    return var

#-- get the difference between two dates. Pay attention to argument
# orders. Subtract the final from the initial. Hence, the result shows
# how much the temperature has changed since the initial value.
def getdiff(t_f,t_i):
    # check if available (later)
    return np.subtract(getdata(t_f),getdata(t_i))

# === set variables  === #

#-- Set filename to read the data from. Get the name from system input
# if it is provided in the command line. This could be understood from
# numbers of arguments passed to Python while running this script, i.e.
# `$ python ped-comp.py dataset-name data-to-plot`
#-- For example, the code below, plots the first data in the file named
# `data-comp.nc` in the current working directory:
# `$ python ped-comp.py data-comp.nc 0`
#filename = "data-comp.nc"
#-- Get the initial time from user input if it is available. Otherwise,
# just use the default `0` value for time index: t_i.
# Be advised, the argument has to be only one integer. Also, this value
# is not allowed to be larger than `time` tables available.
t_i = 0 # the default value. changes if the condition below is met:
if(np.size(av) > 1): t_i = int(av[1])
t_f = None # the default value. changes if the condition below is met:
if(np.size(av) > 2): t_f = int(av[2])

filename = "data-comp.nc"
plotname = "test"
plottype = "png"
db = True # set debugging mode on or off

# === start calculations  === #

#-- open file and dicover variables
f   = nio.open_file(filename,'r') # Data before March 2020.
ff  = nio.open_file("data-2020.nc",'r') # Data Mar & Apr 2020.

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

# this will count how many `time` tables are available:
time_count = np.shape(f.variables['skt'])[0]

#-- check how many datasets are available under different times
print(np.size(f.variables['time'].attributes['calendar']))
print(f.variables['time'].attributes['calendar'])
print(f.variables['time'])
print('** Date(s):')
for i in range(time_count):
    tt = f.variables['time'][i]
    if db: print(i,":",tt,end=' ')
    print(h2d(tt))


#-- converting time, hours since 1900-01-01

#-- This will convert the time value into a human readable form. The
# time value will also be added to the output file name. Unique names
# help with better understanding the output plots.
if(np.size(av) > 1):
    plotname = "diff" + gettime(t_f) + "from" + gettime(t_i)
else:
    plotname = plotname + gettime(t_i)

#-- Knowing the dimensions, now we can recall useful data:
#var = f.variables['skt'][t_i,0,9,:,:]
if(t_f == None):
    var = getdata(t_i)
else:
    var = getdiff(t_f,t_i)
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

if db : print('** converting time to Date:', gettime(t_i))

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
#plotname = f.variables['skt'].attributes['long_name'] + 'by Pedram, for Dear Saeed.'

#-- create the contour plot
plot = ngl.contour_map(wks,var,res)

#-- write variable long name and units to the plot
txres   = ngl.Resources()
txres.txFontHeightF = 0.012
ngl.text_ndc(wks, plotname + 'In degrees Celsius. Data date: ' + gettime(t_i) , 0.50,0.82,txres)

# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
ngl.frame(wks)

ngl.end()
