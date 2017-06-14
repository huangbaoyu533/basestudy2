# coding:utf-8
__author__ = 'hadoop'
import time, os, zipfile
from lxml import etree
import util


class Surface:
    def __init__(self, elem):
        points = []
        points2 = []
        for e in elem.iter('{http://www.opengis.net/gml}posList'):
            poslist = e.text.split(' ')
            # clockwise
            for i in xrange(len(poslist)/3-1):
                point = [float(poslist[3*i]), float(poslist[3*i+1]), float(poslist[3*i+2])]
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                points.extend(point)

            # anti-clockwise
            for i in range(len(poslist)/3-1, 0, -1):
                point = [float(poslist[3*i-3]), float(poslist[3*i-2]), float(poslist[3*i-1])]
                # points2.extend(point)
                points.extend(point)

        self.ps = points


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

        self.ps = ps
        # print 'self.ps: ', self.ps
        # print 'surface num: ', len(ps)
        return ps


def fast_iter(context):
    total_ps = []
    for event, element in context:
        flag = False
        if element.tag.endswith('cityObjectMember'):
            building = Building(element)
            building_ps = building.getPolygon()
            total_ps.append(building_ps)


            del building
            flag = True

        if flag:
            element.clear()

    del context
    util.save_hammarby_obj(total_ps, './citygml_data/obj/hammarby_obj.obj')
    print len(total_ps)
    # util.savex3d(total_ps, 'obj/0_hammarby2.x3d')


def readcity(file):
    context = etree.iterparse(file, events=('end',))
    fast_iter(context)


def readzip(path):
    for file in os.listdir(path):
        name = file[:-4]
        if file[-3:] == 'zip':
            with zipfile.ZipFile(path+file, 'r') as unzipfile:
                for f in unzipfile.namelist():
                    if f[-3:] in ['gml', 'xml', 'GML', 'XML']:
                        print 'file name: ', name
                        readcity(unzipfile.open(f))


if __name__ == '__main__':
    start = time.time()
    path = './citygml_data/Berlin_Pariser_Platz_v1.0.0/Berlin_Pariser_Platz_v1.0.0.xml'
    readzip(path)
    total = time.time() - start
    print 'total time: ', total