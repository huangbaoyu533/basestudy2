#!/usr/bin/python
# -*- coding: UTF-8 -*-
# this is a py to read shapefile and mapinfo file
# maobo@njue 20170306


# This is used to read shape files and save to geojson

import os
import os.path
import tempfile
import zipfile
import ogr
# doc: https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html

import geojson
import json

from shapely.geometry import Point
from functools import partial
import pyproj
from shapely.ops import transform

class icmapinfo:
    'mapinfo file class contain MAP,tab,ID,DAT'


    def __init__(self, name):
        self.name = name
        self.attrs = {}
        self.datatype = None
        self.prj = ''
        self.geos = []

    def set(self, attr,val):
        # print 'set:',attr,val #RESULT:shp ../../data/3D_Block/Farsta_Utskr-3D-Kuber_shp
        # print self.name
        # print self.attrs     #  空字典{}
        self.attrs[attr] = val

    def getmapinfo(self):
        dn = ''
        tb = ''
        if self.datatype=='mapinfo':
            dn = "MapInfo File"
            tb = 'tab'
        elif self.datatype=='arcgis':
            dn = "ESRI Shapefile"
            tb = 'shp'

        driver = ogr.GetDriverByName(dn)
        datasource = driver.Open(self.attrs[tb])
        layer = datasource.GetLayer()
        spatialRef = layer.GetSpatialRef()
        # print spatialRef  #读出.prj文件
        # multipoint = ogr.Geometry(ogr.wkbMultiPoint)

        bbox = []
        ps = []
        layerDefinition = layer.GetLayerDefn()
        for i in range(layerDefinition.GetFieldCount()):
            print layerDefinition.GetFieldDefn(i).GetName()
        for feature in layer:
            geom = feature.GetGeometryRef()  #Fetch pointer to feature geometry.
            # print dir(feature)
            # print 'attrs:',feature.GetFieldCount()
            props = {}
            props['title'] = self.name
            for i in range(feature.GetFieldCount()):
                props[layerDefinition.GetFieldDefn(i).GetName()]=feature.GetField(i)
                # print "props",props  # props {'KATEGORI': 'Vattentorn', 'BYGG_H': None, 'KOM_ID': 56045, 'KOMPONENT': 'gyS3D', 'title': 'Sk\xd0\x94rholmen_Utskr-3D-Kuber'}
            gt = geom.GetGeometryType()
            # print 'type(gt): ', type(gt)
            # gn = geom.GetGeometryName()
            # print 'type(gn): ', gn
            gps = []
            print "gt",gt
            # print "geom",geom #-2147483645 POLYGON ((151613.40106 6577443.73464 7.545,151613.19646 6577443.25545 7.545,151613.19646 6577443.25545 65.315,151613.40106 6577443.73464 65.315,151613.40106 6577443.73464 7.545))
            if gt == 1: # Point
                gps = geom.GetPoints()
                gps = trans(gps)
                print "gps:",gps
                fp = geojson.Feature()
                op = geojson.Point(gps[0])
                fp.properties = props
                #op.id = 'id'
                fp.geometry = op
                #fp.type = 'Feature'
                self.geos.append(fp)
                # ring = geom.GetGeometryRef(0)
                # print "type(ring),ring",type(ring),ring
            elif gt == 2:#LINESTRING
                gps = geom.GetPoints()
                gps = trans(gps)
                fp = geojson.Feature()
                op = geojson.LineString(gps)
                #fp.type = 'Feature'
                fp.geometry = op
                #op.type = 'polyline'
                fp.properties = props
                #fp.id = 'id'
                self.geos.append(fp)


            for p in gps:
                ps.append(p)
                if p[0]<1000:
                    print p
                if len(bbox)<4:
                    bbox = [p[0],p[1],p[0],p[1]]
                else:
                    if p[0]<bbox[0]:
                        bbox[0] = p[0]
                    if p[1]<bbox[1]:
                        bbox[1] = p[1]
                    if p[0]>bbox[2]:
                        bbox[2] = p[0]
                    if p[1]>bbox[3]:
                        bbox[3] = p[1]
            # break
            # print geom.Centroid().ExportToWkt()
        print bbox,len(ps)
        # drawpoints(ps)
        pass

    def savegeojson(self):
        gc = geojson.GeometryCollection(self.geos[:10])
        fc = geojson.FeatureCollection(self.geos[:])
        # print 'gc: ', gc
        # print 'fc: ', fc
        # print 'len(gc): ', len(gc)
        # print 'len(fc): ', len(fc)
        tg = {}
        tg['type'] = 'Topology'

        tg['objects'] = {self.name:gc}

        fl = '../json/'+self.name+'.json'
        with open(fl, 'w') as outfile:
            #dump = geojson.dumps(gc)
            #rtg = (tg).replace('LineString','polyline')

            #json.dump(tg, outfile)
            json.dump(fc, outfile)
        #print dump

    def getInfo(self):
        # print 'info:'
        print self.name
        for a in self.attrs:
            print a,self.attrs[a]


    def getbbox(self):
        shapes = self.sf.shapes()
        #print len(shapes)
        #for s in shapes:
            #print s.points
        return self.sf.bbox

    def getHeigths(self):
        print 'getHegiths'
        res = []
        for sr in self.sf.records():
            res.append(sr)
        return res



def trans(gps):
    print 'gps: ', gps
    res = []
    for p in gps:
        np = untrans(p)
        res.append(np)
    return res


def untrans(p):
    point1 = Point(p[:2])
    # print (point1)
    project = partial(
        pyproj.transform,
        pyproj.Proj(init='epsg:3011'),
        pyproj.Proj(init='epsg:4326'))

    point2 = transform(project, point1)
    #print (point2.x)
    res = [point2.x,point2.y]
    res.extend(p[2:])
    return res

def getDriver():
    cnt = ogr.GetDriverCount()
    formatsList = []  # Empty List

    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()
        if not driverName in formatsList:
            formatsList.append(driverName)

    formatsList.sort() # Sorting the messy list of ogr drivers

    for i in formatsList:
         print i


def readdir(pt):
    res = {}
    for ff in os.listdir(pt):
        if ff[-3:] in ['MAP','tab','ID','DAT']:
            name = ff[:-4].split('/')[-1]
            zf = os.path.join(pt,ff)
            if name in res:
                res[name].set(ff[-3:],zf)
            else:
                res[name] = icmapinfo(name)
                res[name].datatype = 'mapinfo'
                res[name].set(ff[-3:],zf)
        if ff[-3:] in ['dbf','prj','shp','shx','lyr']:
            # print 'ffff:',ff
            name = ff[:-4].split('/')[-1]
            zf = os.path.join(pt,ff)
            # print zf
            if name in res:
                res[name].set(ff[-3:],zf)
            else:
                nn = icmapinfo(name)
                res[name] = nn
                res[name].datatype = 'arcgis'
                res[name].set(ff[-3:],zf)
    for r in res:
        # print 'rr:',r
        # print  "res[r].name:",res[r].name
        res[r].getInfo()
        res[r].getmapinfo()
        res[r].savegeojson()
    return res

def getzipfile(path = '../../data/3D_Block.zip'):
    zip = zipfile.ZipFile(path)
    tempdir = tempfile.mkdtemp()
    # print "tempdir:",tempdir    #tempdir: /tmp/tmpdMpfgN
    # Copy the zipped files to a temporary directory, preserving names.
    # print  "namelist" ,zip.namelist()
    for name in zip.namelist():
        data = zip.read(name)
        print "data",data
        outfile = os.path.join(tempdir, name)
        print "outfile:", outfile
        f = open(outfile, 'w')
        f.write(data)
        f.close()

    #data = ogr.Open(os.path.join(tempdir, '625k_V5_BEDROCK_Geology_Polygons.shp'))
    # More work here...
    readdir(tempdir)
    # Clean up after ourselves.
    for ff in os.listdir(tempdir):
        # print ff
        os.unlink(os.path.join(tempdir, ff))
    os.rmdir(tempdir)


def main():
    # getzipfile()
    readdir('../../data/3D_Block/')
    pass

if __name__ == '__main__':
    main()

