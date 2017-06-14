__author__ = 'wlw'
# coding:utf-8
import pyproj, math
from shapely.ops import transform
from shapely.geometry import Point
from functools import partial
from lxml import etree as ET


# 将(x,y)投影为p(lon, lat)
def untrans(p, epsg_code):
    point1 = Point(p[:2])
    # print 'point1: ', point1
    project = partial(
        pyproj.transform,
        # epsg:7405 is suitable for london lidar
        pyproj.Proj(init=epsg_code),
        # epsg:32633 is suitable for berlin citygml
        # pyproj.Proj(init='epsg:32633'),
        # epsg:3068 is suitable for pariser platz citygml
        # pyproj.Proj(init='epsg:3068'),  # source coordinate system
        pyproj.Proj(init='epsg:4326'))  # destination coordinate system

    point2 = transform(project, point1)
    # print (point2.x)
    res = [point2.x, point2.y]
    # print 'res: ', res
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
    # print 'point1: ', point1
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
        pyproj.Proj(init='epsg:32633')
    )

    point2 = transform(project, point1)
    res = [point2.x, point2.y]
    # print 'res: ', res
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


def convertTri(poly):
    res = []
    last_p = []
    # poly = [23304.17, 21202.51, 0.0, 23303.776, 21205.113, 0.0, 23303.776, 21205.113, 4.0, 23304.17, 21202.51, 4.0]
    for i in xrange(2, len(poly)/3):
        if i == 2:
            tmp = poly[:6]
            p = [poly[3*i], poly[3*i+1], poly[3*i+2]]
            last_p = p
            tmp.extend(p)
            res.append(tmp)
            # print tmp
        else:
            tmp = poly[:3]
            tmp.extend(last_p)
            p = [poly[3*i], poly[3*i+1], poly[3*i+2]]
            tmp.extend(p)
            res.append(tmp)
            # print tmp

    # print 'res: ', res
    return res


def save_hammarby_obj(total_ps, path):
    f_obj = open(path, 'w')
    res = ''
    points = ''
    polys = ''
    parent_idx = 1

    # hammarby offset
    dx = 6576741.0
    dy = 155372.0

    for building_ps in total_ps:
        for surface in building_ps:
            vertice = ''
            for i in xrange(len(surface)/3):
                # repr(): can preserve 12 precision
                # (y, x, z)
                vertice = vertice+'v '+repr(surface[3*i+1]-dy)+' '+repr(surface[3*i]-dx)+' '+repr(surface[3*i+2])+'\n'


            points += vertice

            if parent_idx == 1:
                j = parent_idx + 1
                while j < (len(surface)/3):
                    face = 'f '
                    last_idx = j
                    face = face+str(parent_idx)+' '+str(last_idx)+' '+str(j+1)+'\n'
                    polys += face
                    j += 1
                # print polys
                parent_idx = j + 1

            else:
                j = parent_idx + 1
                while j < (len(surface)/3+parent_idx-1):
                    face = 'f '
                    last_idx = j
                    face = face+str(parent_idx)+' '+str(last_idx)+' '+str(j+1)+'\n'
                    polys += face
                    j += 1
                parent_idx = j + 1


    res += points
    res += polys

    f_obj.write(res)
    f_obj.close()


def saveobj(total_ps, path):
    # total_ps = [[[0,0,0, 0,0,1, 0,1,1, 0,1,0], [0,0,0, 0,0,1, 1,0,1, 1,0,0]]]
    f_obj = open(path, 'w')
    res = ''
    points = ''
    polys = ''
    parent_idx = 1

    dx = total_ps[0][0][0]
    dy = total_ps[0][0][1]
    for building_ps in total_ps:
        for surface in building_ps:
            vertice = ''
            for i in xrange(len(surface)/3):
                # repr(): can preserve 12 precision
                # (x, y, z)
                # vertice = vertice+'v '+repr(surface[3*i]-dx)+' '+repr(surface[3*i+1]-dy)+' '+repr(surface[3*i+2])+'\n'
                vertice = vertice+'v '+repr(surface[3*i]-dx)+' '+repr(surface[3*i+2])+' '+repr(surface[3*i+1]-dy)+'\n'

            points += vertice

            if parent_idx == 1:
                j = parent_idx + 1
                while j < (len(surface)/3):
                    face = 'f '
                    last_idx = j
                    face = face+str(parent_idx)+' '+str(last_idx)+' '+str(j+1)+'\n'
                    polys += face
                    j += 1
                # print polys
                parent_idx = j + 1

            else:
                j = parent_idx + 1
                while j < (len(surface)/3+parent_idx-1):
                    face = 'f '
                    last_idx = j
                    face = face+str(parent_idx)+' '+str(last_idx)+' '+str(j+1)+'\n'
                    polys += face
                    j += 1
                parent_idx = j + 1


    res += points
    res += polys

    f_obj.write(res)
    f_obj.close()


def concatenate(x, y):
    return x + ' ' + y


def getIdxPoints(b_ps):
    b_coordidx = ''
    b_points = ''
    k = 0
    for sur_ps in b_ps:
        points = []
        for i in xrange(len(sur_ps)/3):
            point = [float(sur_ps[3*i])-6576741.0, float(sur_ps[3*i+1])-155372.0, float(sur_ps[3*i+2])]
            # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
            points.extend(point)

        points = list(map(str, points))
        # print 'points: ', points
        b_points = b_points + reduce(concatenate, points) + ' '
        # print 'b_points: ', b_points

        for i in xrange(len(sur_ps)/3):
            b_coordidx = b_coordidx + str(k) + ' '
            k += 1

        b_coordidx += '-1 '
    # print 'b_points: ', b_points
    # print b_coordidx
    return b_coordidx, b_points


def savex3d(total_ps, path):
    flag = 0
    for b_ps in total_ps:
        b_coordidx, b_points = getIdxPoints(b_ps)
        if flag == 0:
            tree = ET.parse('base.x3d')
        else:
            tree = ET.parse(path)

        root = tree.getroot()
        group = root.find('.//Group')
        shape = ET.SubElement(group, 'Shape')
        apr = ET.SubElement(shape, 'Appearance')
        matr = ET.SubElement(apr, 'Material')
        matr.set('diffuseColor', '1 0 0')
        ifs = ET.SubElement(shape, 'IndexedFaceSet')
        ifs.set('DEF', 'building_'+str(flag))


        ifs.set('coordIndex', b_coordidx)
        ifs.set('solid', 'true')
        coord = ET.SubElement(ifs, 'Coordinate')
        coord.set('point', b_points)
        tree.write(path)
        flag += 1