# coding:utf-8
__author__ = 'hadoop'
import time, os, zipfile
from lxml import etree
import util
import math


class Surface:
    def __init__(self, elem):
        points = []
        pointds = []
        d=[]
        ds=[]
        for e in elem.iter('{http://www.opengis.net/gml}posList'):
            poslist = e.text.split(' ')
            # print "poslist:",poslist
            # clockwise
            for i in xrange(len(poslist)/3-1):
                point = [float(poslist[3*i]), float(poslist[3*i+1]), float(poslist[3*i+2])]
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                points.extend(point)
                # print 'points:', points
            for m in xrange(len(poslist)/3):
                pointd = [float(poslist[3*m]), float(poslist[3*m+1]), float(poslist[3*m+2])]
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                pointds.extend(pointd)
            # print 'pointds:', pointds #changdu 15 mei you qu diao zui hou yi ge dian de poslist
            for n in range(len(pointds)/3-1):
                x2=(pointds[3*(n+1)]-pointds[3*n])**2
                y2=(pointds[3*(n+1)+1]-pointds[3*n+1])**2
                z2=(pointds[3*(n+1)+2]-pointds[3*n+2])**2
                # print 'x,y,z',x2,y2,z2
                d=math.sqrt(x2+y2+z2)
                ds.extend([d])
            # print 'len pointds:', len(pointds)
            print " ds:",ds  #dian yu dian zhi jian de ju li
            print " ds:", min(ds)# one poslist min bian
        self.minds = min(ds)
        self.ps = points
        # print 'points:', points


class Building:
    def __init__(self, element):
        self.element = element

    def getPolygon(self):
        ps = []
        c=0
        c1=0
        minds_all=[]

        for elems in self.element.iter('{http://www.opengis.net/citygml/building/1.0}WallSurface'):
            c += 1

            for elem in elems.iter('{http://www.opengis.net/gml}surfaceMember'):
                # filter the interior points

                for e in elem.iter('{http://www.opengis.net/gml}exterior'):
                    # sur_ps = Surface(e).ps
                    # ps.append(sur_ps)
                    mindss=Surface(e).minds
                    minds_all.extend([mindss])

            # print "minds_all:", len(minds_all)
            sort_ds_all = sorted(minds_all)
            print "sort_ds_all:", sort_ds_all
            for elem in elems.iter('{http://www.opengis.net/gml}surfaceMember'):
                # filter the interior points
                c1+=1
                for e in elem.iter('{http://www.opengis.net/gml}exterior'):
                    mindss = Surface(e).minds
                    print 'mindss:',mindss

                    if mindss<0.4:
                        continue
                    sur_ps = Surface(e).ps
                    ps.append(sur_ps)

            # break

        self.ps = ps
        # print 'self.ps: ', self.ps
        print 'surface num: ', len(ps)
        print 'c: ', c
        print 'c1: ', c1
        print "ps:",ps
        return ps


def fast_iter(context):
    total_ps = []
    building_count=0
    for event, element in context:
        flag = False
        if element.tag.endswith('Building'):
            building_count = building_count+1
            building = Building(element)
            building_ps = building.getPolygon()
            print  'building.id:',element.get('{http://www.opengis.net/gml}id')
            total_ps.append(building_ps)
            # print one building
            if building_count==2:
                break

            del building
            flag = True

        if flag:
            element.clear()

    # buildingcount: 192
    print "buildingcount:",building_count

    del context
    util.saveobj(total_ps, './citygml_data/obj/twobuilding_wall_0.4_5.obj')
    # print 'total_ps: ', total_ps
    # print "len(total_ps):" ,len(total_ps)


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
