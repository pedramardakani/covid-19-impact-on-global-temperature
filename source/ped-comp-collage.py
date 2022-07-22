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

#-- convert data to float64 for numpy compatiblility
### and get the product from scale factor
def getdata(time):
    var = f.variables['skt'][time,0,:,:]
    var = var.astype('float64') # change to float64
    sf = f.variables['skt'].attributes['scale_factor'] # check scale
    var = var * np.array(sf) # scale the data
    return var

#-- get the difference between two dates
### pay attention to argument placements
def getdiff(t_f,t_i):
    # check if available (later)
    return getdata(t_f) - getdata(t_i)

# === set variables  === #

#-- set filename to read the data from
filename = "data-comp.nc"
plotname = "collage"
plottype = "pdf"

# === start calculations  === #

#-- open file
f   = nio.open_file(filename,'r')

for i in f.variables['time']:
    print('i =',i,'Date:',h2d(i))

time3, time2, time1 = 6, 3, 0
plottitle = plotname + str(gettime(time3)) + "vs" \
    + str(gettime(time2)) + "vs" + str(gettime(time1))

#-- start the graphics
wks = ngl.open_wks(plottype,plottitle)

lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

#-- resource settings
res = ngl.Resources()
res.nglDraw         = False         # don't draw plots
res.nglFrame        = False         # don't advance the frame
res.cnFillOn        = True          # contour fill
res.cnFillPalette   = "cmp_b2r"     # choose color map
res.lbLabelBarOn    = False         # don't draw a label bar
res.cnLineLabelsOn  = False         # no line labels
res.sfXArray        = lon           # coords for x axis
res.sfYArray        = lat           # coords for y axis

#-- create the contour plots
plot = []
p = ngl.contour_map(wks,getdiff(time3,time2),res)
plot.append(p)
p = ngl.contour_map(wks,getdiff(time3,time1),res)
plot.append(p)

#-- panel resources
pnlres = ngl.Resources()
pnlres.nglFrame = False # don't advance the frame
pnlres.nglPanelLabelBar = True # common label bar
pnlres.txstring = str(plottitle) # panel title
pnlres.txFontHeightF = 0.02 # text font size

#-- create the panel plot
ngl.panel(wks,plot[:],[2,1],pnlres)

#-- Set the plot name
plotname = f.variables['skt'].attributes['long_name'] + 'by Pedram, for Dear Saeed.'

#-- add title string, long_name and units string to panel
### horrible text placement, let's do it later!
"""
txres   = ngl.Resources()
txres.txFontHeightF = 0.020
ngl.text_ndc(wks, plottitle, 0.5, 0.825, txres)

txres.txFontHeightF = 0.012
ngl.text_ndc(wks, plotname+ 'In degrees Celsius. Date: ' + str(gettime(t_f)) + " vs " + str(gettime(t_i)) , 0.50,0.82,txres)
# Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']
"""
ngl.frame(wks)

ngl.end()
