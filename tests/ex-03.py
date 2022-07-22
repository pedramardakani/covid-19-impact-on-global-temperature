"""
Contour Fill on Maps, Pedram. 
"""

#-- no output? check if the last line that contains
#-- the plot function is commented. uncomment for output.

import numpy as np
import Ngl as ngl
import Nio as nio
import datetime

def pedplot():
	#-- create the contour plot
	plot = ngl.contour_map(wks,var,res)

	#-- write variable long name and units to the plot
	txres   = ngl.Resources()
	txres.txFontHeightF = 0.012

	ngl.text_ndc(wks, plotname + \
						'   In degrees Celsius.' + \
						'   Data date: ' + str(t_date) , \
						0.50,0.82,txres)
			# Hard coded this because of inconsistency \
			# in data structure: f.variables['skt'].attributes['units']

	#-- advance the frame
	
	ngl.frame(wks)

#-- open file and read variables 
f   = nio.open_file('data.nc','r')
var = f.variables['skt'][0,:,:]
lat = f.variables['latitude'][:]
lon = f.variables['longitude'][:]

#-- resource settings
res = ngl.Resources()
res.nglFrame    = False

res.cnFillOn    = True
res.cnFillPalette   = "NCL_default"
res.cnLineLabelsOn  = False

res.lbOrientation   = "horizontal"

res.sfXArray    = lon
res.sfYArray    = lat

animate = False
frames = 1

for i in range(frames):
	### start the graphics
	wks = ngl.open_wks('png','ss_skt_plt')

	### converting time, hours since 1900-01-01
	hrs	= f.variables['time'][0]
	print(hrs)
	tstart	= datetime.date(1900,1,1)
	tdelta	= datetime.timedelta(hours=float(hrs))
	t_date	= tstart + tdelta
	print('Date:', t_date)
	
	### Check the data type
	if(var.dtype != 'float64'):
		print('\nCaution! Current data type:','(',var.dtype, \
			')\n> Changing to: ( float64 )')
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
	if(os != None):
		print('> offset type:',type(os))
		print('> offset value:',os)
	
	print('\nChecking available variables:\n')
	for vt in f.variables:
		for at in f.variables[vt].attributes:
			print('> f.variables[',vt,'].attributes[',at,']',sep='')
		print('')
	print('Done!\n')
	
	### Set the plot name
	plotname = f.variables['skt'].attributes['long_name'] + \
		' by Pedram, for Dear Saeed.'
	
	start_time = datetime.datetime.now()
	
	# == save skin temperature in a separate text file == #
	nlat = len(f.variables['latitude'])
	lat = f.variables['latitude'][:]
	nlon = len(f.variables['longitude'])
	lon = f.variables['longitude'][:]
	t = np.ravel(f.variables['skt'][0])
	x = np.repeat(lat,nlon,axis=0) # rlon
	y = np.tile(lon,nlat)
	res = np.vstack((x,y,t))
	res = np.transpose(res)
	end_time = datetime.datetime.now()
	print('time =',end_time - start_time)
	#np.savetxt("skin-temp.txt", res, fmt=['%5.2f','%3.2f','%5d'], delimiter = " ")
	
	# == comment or uncomment next line to get the map outputs == #
	#pedplot()
	ngl.end()
