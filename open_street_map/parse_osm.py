import xml.etree.cElementTree as ET
tree = ET.parse('./osm_data/map.osm')
root = tree.getroot()
allnodes=root.findall('node')
lats=[]
lons=[]
for node in allnodes:
    lat=float(node.get('lat'))
    lats.append(lat)
    lon=float(node.get('lon'))
    lons.append(lon)
lst=[[i,j]for i in lats for j in lons]
#points store in list
print "lst:",lst

for tag in node.getiterator():
    print  "tag.attrib:",tag.attrib
    # add code here to get the cityname
# count=0
# for way in root.findall('way'):
#     id = way.get('id')
#     count = count+1
# print "count:",count