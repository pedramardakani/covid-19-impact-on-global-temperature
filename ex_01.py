import Ngl as ngl

#-- open workstation
wks_type = "pdf"
wks = ngl.open_wks(wks_type, 'hello')

#-- which projection do we want to plot
projections = ['CylindricalEquidistant', 'Mollweide',\
				'Robinson','Orthographic']

#-- projection settings
mpres = ngl.Resources()

mpres.vpWidthF	= 0.8	#-- viewport width
mpres.vpHeightF = 0.8	#-- viewport height

mpres.mpFillOn	= True
mpres.mpOceanFillColor	= 'Transparent'
mpres.mpLandFillColor	= 'Gray90'
mpres.mpInlandWaterFillColor	= 'Gray90'

for proj in projections:
	mpres.mpProjection = proj
	# mpres.tiMainString = proj
	mpres.tiMainString = proj+' For Dear Saeed'
	map = ngl.map(wks,mpres)
	
ngl.end()
