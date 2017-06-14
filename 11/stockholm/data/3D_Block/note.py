# coding:utf-8
import matplotlib.pyplot as plt
import shapefile

shpFilePath = "/home/huangby/PycharmProjects/basestudy2/11/stockholm/data/3D_Block/Farsta_Utskr-3D-Kuber_shp/Byggnad_area.shp"
listx=[]
listy=[]
test = shapefile.Reader(shpFilePath)
print "sr:",test.shapeRecord()
for sr in test.shapeRecords():
    for xNew,yNew in sr.shape.points:
        listx.append(xNew)
        listy.append(yNew)
plt.plot(listx,listy)
plt.show()


