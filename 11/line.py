from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

map = Basemap(llcrnrlon=18.079217231362385,llcrnrlat=59.30025017186058,urcrnrlon=28.11395240235795,urcrnrlat=39.310241338809746,projection='tmerc',
              lat_0=59.305000000, lon_0=18.080000000)

map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcoastlines()

lons = [18.07942756196004,18.01003306872341, 17.976345761176503, 18.028328251891363, 17.98900634927485, 18.047848235169262]
lats = [59.26396226429699,59.33822167551083, 59.26666684896559, 59.312137248039924, 59.30203176255585, 59.31474246335528]

x, y = map(lons, lats)

map.plot(x, y, marker=None,color='m')

plt.show()

