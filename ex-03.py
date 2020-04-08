"""
Contour Fill on Maps, Pedram. 
"""

import numpy as np
import Ngl as ngl
import Nio as nio

#-- open file and read variables 

f   = nio.open_file('data.nc','r')
var = f.variables['skt'][0,:,:]
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

#-- start the graphics

#wks = ngl.open_wks('pdf','ss_skt_plt')
wks = ngl.open_wks('png','ss_skt_plt')

#-- resource settings

res = ngl.Resources()
res.nglFrame    = False

res.cnFillOn    = True
res.cnFillPalette   = "NCL_default"
res.cnLineLabelsOn  = False

res.lbOrientation   = "horizontal"

res.sfXArray    = lon
res.sfYArray    = lat

### Set the plot name

plotname = f.variables['skt'].attributes['long_name'] + ' by Pedram, for Dear Saeed'

### Check the data type

if(var.dtype != 'float64'):
	print('\nCaution! Current data type:','(',var.dtype,')\n> Changing to: ( float64 )')
	var = var.astype('float64')
	if(var.dtype == 'float64'):
		print('Success! Data type:',var.dtype)
		
### Check if there are scale factors involved

print('\nChecking for scale factors ...')
sf = f.variables['skt'].attributes['scale_factor']
if(sf != None):
	print('> scale factor:',sf)
	print('> scale factor type:', type(sf))
	var = var * np.array(sf)

### Check if there are offset values available

print('\nChecking for offset values ...')
os = f.variables['skt'].attributes['add_offset']
if(os != None)

print('> offset type:',type(os))
print('> offset value:',os)

print(' ################### debugging ################### ')
print('\nChecking available variables:\n')
#print('# variable\t: attributes')
for vt in f.variables:
	for at in f.variables[vt].attributes:
		print('> f.variables[',vt,'].attributes[',at,']',sep='')
	print('')
print('Done!\n')
print(f.variables['skt'].attributes['long_name'])
print(f.variables['skt'].attributes['units'])
print(type(wks),type(var),type(res))
print(f.variables['skt'])
print(' ################### done ################### ')
#"""
#-- create the contour plot
plot = ngl.contour_map(wks,var,res)

#-- write variable long name and units to the plot
txres   = ngl.Resources()
txres.txFontHeightF = 0.012

ngl.text_ndc(wks, plotname, \
        0.30,0.82,txres)
ngl.text_ndc(wks, 'Degrees Celsius', \
        0.90,0.82,txres) # Hard coded this because of inconsistency in data structure: f.variables['skt'].attributes['units']

#-- advance the frame
ngl.frame(wks)

ngl.end()
#"""
