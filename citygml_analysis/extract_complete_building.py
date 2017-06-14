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
            # print "poslist:",poslist
            for i in xrange(len(poslist)/3-1):
                point = [float(poslist[3*i]), float(poslist[3*i+1]), float(poslist[3*i+2])]
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                points.extend(point)
                # print 'points:', points

        self.ps = points
        # print 'points:', points


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
    building_count=0
    for event, element in context:
        flag = False
        if element.tag.endswith('Building'):
            building_count = building_count+1
            if 8>=building_count>7:
                building = Building(element)
                building_ps = building.getPolygon()
                print 'buildingcount:',building_count
                print  'building.id:', element.get('{http://www.opengis.net/gml}id')
                total_ps.append(building_ps)

            # print "total_ps:",total_ps
            # print one building
            # if building_count==5:
            #     break

                del building
                flag = True

                if flag:
                    element.clear()
            else:
                continue

    # buildingcount: 192
    # print "buildingcount:",building_count

    del context
    util.saveobj(total_ps, './citygml_data/obj/8-8_complete_building.obj')
    # print 'total_ps: ', total_ps
    # print "len(total_ps):" ,len(total_ps)

    # util.savex3d(total_ps, 'obj/0_hammarby2.x3d')


def readcity(file):
    context = etree.iterparse(file, events=('end',))
    fast_iter(context)


if __name__ == '__main__':
    start = time.time()
    # path = './citygml_data/Berlin_Pariser_Platz_v1.0.0/b1_lod2_ms_w_sem.xml'
    # readzip(path)
    file="./citygml_data/Stadt-Ettenheim-LoD3_edited_v1.0.0.gml"
    readcity(file)
    total = time.time() - start
    print 'total time: ', total
