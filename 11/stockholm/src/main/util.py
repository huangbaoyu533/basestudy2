# coding:utf-8
__author__ = 'wlw'

import pyproj, math
from shapely.ops import transform
from shapely.geometry import Point
from functools import partial

# 将(x,y)p(lon, lat)投影为p(lon, lat)
def untrans(p):
    point1 = Point(p)
    # print 'point1: ', point1
    project = partial(
        pyproj.transform,
        # pyproj.Proj(init='epsg:4814'),  # source coordinate system
        pyproj.Proj(init='epsg:3011'),
        pyproj.Proj(init='epsg:4326'))  # destination coordinate system

    point2 = transform(project, point1)
    #print (point2.x)
    res = [point2.x, point2.y]
    print 'res: ', res
    # res.extend(p[2:])




    return res


def transPoly(polys):
    res = []
    for poly in polys:
        npoly = []
        for p in poly:
            npoly.append(trans(p))
        res.append(npoly)
    return res


# 将p(lon, lat)投影为(x,y)
def trans(p):
    point1 = Point(p)
    print 'point1: ', point1
    project = partial(
        pyproj.transform,
        # source coordinate system
        # epsg:4326是整个世界的bounds
        # 传入[lon, lat]
        pyproj.Proj(init='epsg:4326'),
        # destination coordinate system
        # epsg:3068是柏林的bounds
        # 输出[x, y], 单位是米
        # pyproj.Proj(init='epsg:3068')
        # World - N hemisphere - 12°E to 18°E - by country
        # pyproj.Proj(init='epsg:4814')
        pyproj.Proj(init='epsg:32633')
    )

    point2 = transform(project, point1)
    res = [point2.x, point2.y]
    print 'res: ', res
    return res


def compareUpper(up, upper):
    if up[0] > upper[0]:
        upper[0] = up[0]
    if up[1] > upper[1]:
        upper[1] = up[1]


def compareLower(low, lower):
    if low[0] < lower[0]:
        lower[0] = low[0]
    if low[1] < lower[1]:
        lower[1] = low[1]


def extendBox(upper, lower):
    x1 = upper[0] - lower[0]
    y1 = upper[1] - lower[1]
    x2 = math.ceil(x1/1000.0)
    y2 = math.ceil(y1/1000.0)
    upper[0] += (x2*1000-x1)
    lower[1] -= (y2*1000-y1)





