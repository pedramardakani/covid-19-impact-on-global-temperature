import numpy as np

a = np.array([(1,2,3,4),(5,6,7,8)], dtype = float)
print('a =',a)

b = np.ravel(a)
print('b =',b)

c = np.full((1,5),7)
print('c =',c)

d = c.view()
print('d =',d)

e = np.full((1,5),8)
print('e =',e)

f = np.concatenate((d,e,d), axis = 1)
f = print('f = ',f)

lat = np.linspace(90,-90,3)
lon = np.linspace(0,360,5)
print('lat =',lat)
print('lon =',lon)

# ready to transpose
nlat = len(lat)
nlon = len(lon)
#x = np.full((1,nlat),0) # rlon
#x = np.vstack((lat,lat))
#y = np.transpose(x)
x = np.repeat(lat,nlon,axis=0) # rlon
y = np.tile(lon,nlat)
z = np.ravel(np.linspace(0,100,nlat*nlon))
#z = np.transpose(x,y)
print('x =',x)
print('y =',y)
zz = np.vstack((x,y,z))
zz = np.transpose(zz)
print('z = \n',zz)
