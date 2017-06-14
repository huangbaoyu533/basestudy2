# coding:utf-8
__author__ = 'wlw'

import os, shapefile, pyproj
import math, util
from shapely.ops import transform
from shapely.geometry import Point
from functools import partial
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

class Shapefile:
    def __init__(self, name):
        self.name = name

    def setpath(self, path):
        self.path = path

    def getHeight(self, sf):
        res = []
        records = sf.records()
        # print 'records: ', records
        for sr in sf.records():
            res.append(sr)
        return res


    def getshpfiles(self, dirname):
        shapepath = os.path.join(self.path, dirname)
        files = os.listdir(shapepath)
        # print "files:", files
        files.sort()
        # 排序完是['.dbf', '.prj', '.shp', '.shx']的顺序
        n = 0
        shpfiles = []
        shpfile = []
        for file in files:
            # print 'file: ', file
            shpfile.append(file)
            n += 1
            if n == 4:
                shpfiles.append(shpfile)
                n = 0
                shpfile = []
        # print 'shpfiles: ', shpfiles

        sfs = []
        for kind in shpfiles:
            dbf = os.path.join(shapepath, kind[0])
            mydbf = open(dbf, 'rb')
            prj = os.path.join(shapepath, kind[1])
            myprj = open(prj, 'rb')
            shp = os.path.join(shapepath, kind[2])
            myshp = open(shp, 'rb')
            shx = os.path.join(shapepath, kind[3])
            myshx = open(shx, 'rb')

            sf = shapefile.Reader(dbf=mydbf, prj=myprj, shp=myshp, shx=myshx)
            # print 'sf: ', sf        #sf:  <shapefile.Reader instance at 0x7f84f7ec9ab8>
            fields = sf.fields
            # print 'fields: ', fields
            sfs.append(sf)
            self.getHeight(sf)

        return sfs


def getshape2(sf):
    # print "sf:",sf
    # get a list of the shapefile’s geometry
    shapes = sf.shapes()
    # print "shapes",shapes
    polys = []
    for shape in shapes:
        # print 'shape.parts: ', shape.parts
        # print 'shape.points: ', shape.points
        # polys.append(shape.points)
        #
        #print "shape.points" ,shape.points
        # shape.parts
        # 由多个point构成part，再由一或多个part构成shape
        # 如果一个shape有多个part构成，则返回每一个part的第一个point的下标,比如：[0, 5, 10, 15, 20, 25]
        # 如果一个shape只有一个part，则返回[0]
        for i in xrange(len(shape.parts)-1):
            # print 'shape.parts[i]: ', shape.parts[i]
            for p in shape.points[shape.parts[i]:shape.parts[i+1]]:

                p = list(p)  #将点以list存储
                # print 'p: ', p
                util.untrans(p)
                
                break

            break





        break

    # ps是三维的
    return polys


def isinside(poly, box):
    for p in poly:
        if (p[0]>=box[0] and p[0]<=box[2]) and (p[1]>box[1] and p[1]<box[3]):
            return True
    return False



def readfile(path):
    res = {}

    for item in os.listdir(path):

        if item[-3:] == 'xls':
            continue
        else:
            #print 'item: ', item
            name = item[:-4]
            res[name] = Shapefile(name)
            res[name].setpath(path)
            sfs = res[name].getshpfiles(name+'_shp')
            # print 'len(sfs): ', len(sfs)
            # study area
            box = [154513.33223, 6576118.95315, 156490.43356, 6577234.84061]
            for sf in sfs:
                polys = getshape2(sf)
                for poly in polys:
                    # genpoly(poly)
                    if isinside(poly, box):
                        pass
            # break

    return res




def main():
    path = '../../data/3D_Block/'

    shapefiles = readfile(path)
    print 'shapefiles: ', shapefiles

    for sf in shapefiles:
        # print 'sf: ', sf
        shapefiles[sf].getshpfiles(sf+'_shp')



if __name__ == '__main__':
    main()