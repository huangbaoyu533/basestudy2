#coding:utf-8

import matplotlib.pyplot as plt
import shapefile,util


shpFilePath = "/home/huangby/PycharmProjects/basestudy2/11/stockholm/data/3D_Block/Farsta_Utskr-3D-Kuber_shp/Byggnad_area.shp"
listx=[]
listy=[]
test = shapefile.Reader(shpFilePath)
for sr in test.shapeRecords():
    for p in sr.shape.points:
        p = list(p)  # 将点以list存储
        # print 'p: ', p
        res = util.untrans(p)
        listx.append(res[0])
        listy.append(res[1])
plt.plot(listx,listy)
plt.show()