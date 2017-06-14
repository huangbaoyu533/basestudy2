#coding:utf-8
import os
import os.path
import tempfile
import zipfile
import ogr


import geojson
import json
from shapely.geometry import Point
from functools import partial
import pyproj
from shapely.ops import transform


class MapInfo:
    def __init__(self, name):
        self.name = name
        self.attrs = {}
        self.datatype = None
        self.prj = ''
        self.geos = []
    #attr是文件名的后缀,val是它的路径
    def setAttr(self, attr, val):
        self.attrs[attr] = val
        # print "self.attrs[attr]:", self.attrs[attr]

    def getmapinfo(self):
        dn = ""
        tb = ""
        if self.datatype == "arcgis":
            dn = "ESRI Shapefile"
            tb = 'shp'
        # print "dn,tb",dn,tb

        # driver = ogr.GetDriverByName(dn)
        # datasource = driver.Open(self.attrs[tb])
        print "self.attrs[tb]:",self.attrs[tb]
        # datasource = driver.Open(abs_path)
        # layer = datasource.GetLayer()
        # layerDefinition = layer.GetLayerDefn()
        #
        # for feature in layer:
        #     geom = feature.GetGeometryRef()
        #     props = {}
        #     props['title'] = self.name
        #     # get shapefile fields
        #     for i in range(feature.GetFieldCount()):
        #         props[layerDefinition.GetFieldDefn(i).GetName()] = feature.GetField(i)
        #     # print 'props: ', props
        #
        #     gt = geom.GetGeometryType()
        #     gps = []
        #     if gt==1:
        #         gps=geom.GetPoints()
        #         gps=untrans(gps)
        #         fp=geojson.Feature
        #         op=geojson.Point(gps[0])
        #         fp.properties= props
        #         fp.geometry=op
        #         self.geos.append(fp)
        #     elif gt==2:
        #         gps=geom.GetPoints()
        #         gps=untrans(gps)
        #         fp=geojson.Feature()
        #         op=geojson.LineString(gps)
        #         fp.properties=props
        #         fp.geometry=op
        #         self.geos.append(fp)

    def generateJson(self):
        fc = geojson.FeatureCollection(self.geos)
        # print"fc:",fc     fc: {"features": [], "type": "FeatureCollection"}
        fl = './stockholm/data/grid/testjson/'+self.name + '.json'
        with open(fl, 'w') as outfile:
            json.dump(fc, outfile)

def untrans(gps):
    result=[]
    for p in gps:
        point1=Point[:2]
        project=partial(
            pyproj.transform,
            pyproj.Proj(init='epsg:3021'),
            pyproj.Proj(init='epsg:4326'))

        point2 = transform(project, point1)
    result.append([point2.x, point2.y])

    return result

def readdir(pt):
    res = {}
    # print os.listdir(pt)
    # ['Nstationer.shx', '12_kV.shx', 'Nstationer.shp', '04_kV.prj', 'Nstationer.dbf', '12_kV.prj', 'Nstationer.prj','12_kV.shp', '12_kV.dbf', '04_kV.shx', '04_kV.shp', '04_kV.dbf']
    for ff in os.listdir(pt):
        if ff[-3:] in["shp","prj","dbf","shx"]:
            name = ff[:-4]
            # print "name:", name
            # name: Nstationer name: 12_kV name: Nstationer
            zf=os.path.join(pt,ff)
            # print "zf:",zf
            # zf:./ stockholm / data / grid / Nstationer.shx
            # print "res:", res
            if name in res:
                # print "name:", name
                res[name].setAttr(ff[-3:], zf)
            else:
                res[name] = MapInfo(name)
                res[name].datatype = 'arcgis'
                res[name].setAttr(ff[-3:], zf)

    # print "res:", res   #res: {'Nstationer': <__main__.MapInfo instance at 0x7f41249235f0>, '04_kV': <__main__.MapInfo instance at 0x7f41249236c8>, '12_kV': <__main__.MapInfo instance at 0x7f4124923680>}
    print 'res: ', res
    for key in res:
        # pass
        print 'attrs2: ', res[key].attrs
        # print "res[key]:", res[key]
        res[key].getmapinfo()
        # res[key].generateJson()





def main():
    readdir("./stockholm/data/grid")


if __name__ == '__main__':
    main()
