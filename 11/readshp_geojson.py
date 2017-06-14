#!/usr/bin/python
# -*- coding: UTF-8 -*-
# this is a py to read shapefile/mapinfo file, and save to geojson

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
        # {'postfix': abs_path}
        self.attrs = {}
        self.datatype = None
        self.prj = ''
        self.geos = []

    # attr: ff[-3]
    # val: zf
    def setAttr(self, attr, val):
        self.attrs[attr] = val


    def getmapinfo(self):
        dn = ''
        tb = ''
        if self.datatype == 'mapinfo':
            dn = "MapInfo File"
            tb = 'tab'
        elif self.datatype == 'arcgis':
            dn = "ESRI Shapefile"
            tb = 'shp'


        driver = ogr.GetDriverByName(dn)
        abs_path = self.attrs[tb]
        # print "self.attrs[tb]:", self.attrs[tb]   self.attrs[tb]: ./stockholm/data/grid/Nstationer.shp
        datasource = driver.Open(abs_path)
        layer = datasource.GetLayer()
        # print "layer:",layer  layer: <osgeo.ogr.Layer; proxy of <Swig Object of type 'OGRLayerShadow *' at 0x7fadaad271e0> >
        bbox = []
        ps = []
        layerDefinition = layer.GetLayerDefn()
        # print "layerDefinition:", layerDefinition

        for feature in layer:
            geom = feature.GetGeometryRef()
            props = {}
            props['title'] = self.name
            # get shapefile fields
            for i in range(feature.GetFieldCount()):
                props[layerDefinition.GetFieldDefn(i).GetName()] = feature.GetField(i)
            # print 'props: ', props

            gt = geom.GetGeometryType()
            gps = []
            # print 'gt,geom: ', gt, geom
            if gt == 1:  # Point
                gps = geom.GetPoints()
                gps = untrans(gps)
                # print 'gps: ', gps    gps:  [[18.08895918895611, 59.303858524121]]
                fp = geojson.Feature()
                # print 'fp: ', fp           fp:  {"geometry": null, "properties": {}, "type": "Feature"}
                op = geojson.Point(gps[0])
                fp.properties = props
                fp.geometry = op
                self.geos.append(fp)
            elif gt == 2:  # LINESTRING
                gps = geom.GetPoints()
                gps = untrans(gps)
                # print 'gps2: ', gps
                fp = geojson.Feature()
                op = geojson.LineString(gps)
                fp.geometry = op
                fp.properties = props
                self.geos.append(fp)

            # print 'gps: ', gps

            # 得到bbox
        #     for p in gps:
        #         ps.append(p)
        #         if len(bbox) < 4:
        #             bbox = [p[0], p[1], p[0], p[1]]
        #         else:
        #             if p[0] < bbox[0]:
        #                 bbox[0] = p[0]
        #             if p[1] < bbox[1]:
        #                 bbox[1] = p[1]
        #             if p[0] > bbox[2]:
        #                 bbox[2] = p[0]
        #             if p[1] > bbox[3]:
        #                 bbox[3] = p[1]
        #
        # print bbox, len(ps)

    def generateJson(self):
        fc = geojson.FeatureCollection(self.geos)
        # print "fc:",fc
        fl = "./stockholm/data/json/"+self.name+'.json'
        with open(fl, 'w') as outfile:
            json.dump(fc, outfile)
            #文件写到输出文件里


# 将p(x, y)投影为(lon, lat)
def untrans(gps):
    result = []
    for p in gps:
        point1 = Point(p[:2])
        # print (point1)
        project = partial(
            pyproj.transform,
            pyproj.Proj(init='epsg:3021'),
            pyproj.Proj(init='epsg:4326'))

        point2 = transform(project, point1)
        # print (point2.x)
        result.append([point2.x, point2.y])

    return result


def readdir(pt):
    res = {}
    # print os.listdir(pt)
    for ff in os.listdir(pt):
        # 处理mapinfo file
        # if ff[-3:] in ['MAP', 'tab', 'ID', 'DAT']:
        #     name = ff[:-4].split('/')[-1]
        #     zf = os.path.join(pt, ff)
        #     if name in res:
        #         res[name].setAttr(ff[-3:], zf)
        #     else:
        #         res[name] = MapInfo(name)
        #         res[name].datatype = 'mapinfo'
        #         res[name].setAttr(ff[-3:], zf)

        # 处理shapefile
        if ff[-3:] in ['dbf', 'prj', 'shp', 'shx']:
            # print 'ff: ', ff
            name = ff[:-4]
            # print 'name: ', name
            zf = os.path.join(pt, ff)
            # print 'zf: ', zf
            print "res:", res
            if name in res:
                res[name].setAttr(ff[-3:], zf)
            else:
                # value是一个对象
                # {'name': object}
                res[name] = MapInfo(name)
                res[name].datatype = 'arcgis'
                res[name].setAttr(ff[-3:], zf)

    for key in res:
        res[key].getmapinfo()
        res[key].generateJson()


# def getzipfile(path = '/mnt/hgfs/data/geodata/mapinfo/digmap625_bedrock_map.zip'):
#     zip = zipfile.ZipFile(path)
#     tempdir = tempfile.mkdtemp()
#
#     # Copy the zipped files to a temporary directory, preserving names.
#     for name in zip.namelist():
#         data = zip.read(name)
#         outfile = os.path.join(tempdir, name)
#         f = open(outfile, 'w')
#         f.write(data)
#         f.close()
#
#     # data = ogr.Open(os.path.join(tempdir, '625k_V5_BEDROCK_Geology_Polygons.shp'))
#     # More work here...
#     print tempdir
#     readdir(tempdir)
#
#     # Clean up after ourselves.
#     for ff in os.listdir(tempdir):
#         #print ff
#         os.unlink(os.path.join(tempdir, ff))
#     os.rmdir(tempdir)


def main():
    # getzipfile()
    readdir('./stockholm/data/grid')

if __name__ == '__main__':
    main()

