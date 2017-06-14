# coding:utf-8
__author__ = 'hadoop'
import time, os, zipfile
from lxml import etree
import util


class Surface:
    def __init__(self, elem):
        points = []
        points2 = []
        poslist=[]
        for e in elem.iter('{http://www.opengis.net/gml}pos'):
            print "e:", e.text
            pos = e.text.split(' ')
            # print "pos[0],pos[1],pos[2]:",pos[0],pos[1],pos[2]
            point = [float(pos[0]), float(pos[1]), float(pos[2])]
            # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
            poslist.extend(point)
        print "poslist:",poslist
        for i in xrange(len(poslist)/3-1):
            point = [poslist[3*i], poslist[3*i+1], poslist[3*i+2]]
            points.extend(point)

        # print 'points:',points

        # anti-clockwise
        for i in range(len(poslist) / 3 - 1, 0, -1):
            point = [poslist[3 * i - 3], poslist[3 * i - 2], poslist[3 * i - 1]]
            points2.extend(point)
            points.extend(point)


        self.ps = points
        # print 'self.ps: ', self.ps




class Building:
    def __init__(self, element):
        self.element = element

    def getPolygon(self):
        ps = []
        for elem in self.element.iter('{http://www.opengis.net/gml}surfaceMember'):
            # filter the interior points
            for e in elem.iter('{http://www.opengis.net/gml}exterior'):
                sur_ps = Surface(e).ps
                ps.append(sur_ps)
        # print "ps",ps

        self.ps = ps
        # print 'self.ps: ', self.ps
        # print 'surface num: ', len(ps)
        return ps

def fast_iter(context):
    total_ps = []
    building_count = 0
    for event, element in context:
        flag = False
        if element.tag.endswith('Building'):
            building_count = building_count + 1
            building = Building(element)
            building_ps = building.getPolygon()
            total_ps.append(building_ps)
            # print one building
            if building_count == 5:
                break

            del building
            flag = True

        if flag:
            element.clear()
    print "buildingcount:", building_count

    del context
    util.saveobj(total_ps, './citygml_data/obj/lod332.obj')
    # print 'len(total_ps)',len(total_ps)
    # print 'total_ps',total_ps
    # util.savex3d(total_ps, 'obj/0_hammarby2.x3d')


def readcity(file):
    context = etree.iterparse(file, events=('end',))
    fast_iter(context)


if __name__ == '__main__':
    start = time.time()
    file = "./geoRES_testdata_v1.0.0/geoRES_testdata_v1.0.0.xml"
    readcity(file)
    total = time.time() - start
    print 'total time: ', total