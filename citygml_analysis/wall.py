# coding:utf-8
__author__ = 'hadoop'
import time, os, zipfile
from lxml import etree
import util


class Surface:
    def __init__(self, elem):
        points = []
        points2 = []
          # one surface all the postlist gravity


        for e in elem.iter('{http://www.opengis.net/gml}posList'):
            poslist = e.text.split(' ')
            # print "poslist:",poslist
            # clockwise
            long=len(poslist)/3-1 #serval points
            for i in xrange(long):
                point = [float(poslist[3*i]), float(poslist[3*i+1]), float(poslist[3*i+2])]
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                points.extend(point)
                # print 'points:', points



            # # anti-clockwise
            # for i in range(long, 0, -1):
            #     point = [float(poslist[3*i-3]), float(poslist[3*i-2]), float(poslist[3*i-1])]
            #     x.extend([point[0]])
            #     y.extend([point[1]])
            #     z.extend([point[2]])
            #     points2.extend(point)
            #     points.extend(point)
            # gx, gy, gz = self.caculate_gravity(x, y, z, long)
            # gv_total.extend([gx, gy, gz])




            self.ps = points

            print 'points:', points









class Building:
    def __init__(self, element):
        self.element = element

    def caculate_gravity(self, x, y, z, l):
        sumx = 0
        sumy = 0
        sumz = 0
        for x1 in x:
            sumx += x1
        for y1 in y:
            sumy += y1
        for z1 in z:
            sumz += z1
            # print 'z1',z1
        return sumx / l, sumy / l, sumz / l

    def getPolygon(self):
        ps = []
        count = 0
        count1 = 0
        gv_one_wall=[]
        one_wall_points=[]
        x = []
        y = []
        z = []
        xt = []
        yt = []
        zt = []
        gv_total = []
        gv_wall_total=[]
        for elems in self.element.iter('{http://www.opengis.net/citygml/building/1.0}WallSurface'):
            count = count + 1
            for elem in elems.iter('{http://www.opengis.net/gml}surfaceMember'):
                # filter the interior points
                for e in elem.iter('{http://www.opengis.net/gml}exterior'):
                    count1 = count1 + 1
                    sur_ps = Surface(e).ps
                    ps.append(sur_ps)
                    one_wall_points.extend(sur_ps)

            for i in range(len(one_wall_points)/3):
                point = [one_wall_points[3 * i], one_wall_points[3 * i + 1], one_wall_points[3 * i + 2]]
                # print "point ",point
                # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
                x.extend([one_wall_points[3 * i]])
                y.extend([one_wall_points[3 * i + 1]])
                z.extend([one_wall_points[3 * i + 2]])
                # print "x ", x
                # print "y ", y
            print "lenx ", len(x)
            gx, gy, gz = self.caculate_gravity(x, y, z, len(one_wall_points)/3)
            gv_total.extend([gx, gy, gz])
            # gv_total shi yi mian qiang de zhongxin


            if count==1:
                break
        print "gv_total ", len(gv_total)
        for i in range(len(gv_total) / 3):
            point = [gv_total[3 * i], gv_total[3 * i + 1], gv_total[3 * i + 2]]
            print "point ",point
            # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
            xt.extend([gv_total[3 * i]])
            yt.extend([gv_total[3 * i + 1]])
            zt.extend([gv_total[3 * i + 2]])
            print "x;",xt

        gx, gy, gz = self.caculate_gravity(xt, yt, zt, len(gv_total) / 3)
        gv_wall_total.extend([gx, gy, gz])
        print "gv_wall_total ", gv_wall_total   #zhe shi yi ge building de zhongxin

        print "one_wall_points:",len(one_wall_points)
        # print "gv_total:", gv_total


        self.ps = ps
        # print 'self.ps: ', self.ps
        # print 'surface num: ', len(self.ps)
        return ps

def fast_iter(context):
    total_ps = []
    building_count=0
    for event, element in context:
        flag = False
        if element.tag.endswith('Building'):
            building_count = building_count+1
            if element.get('{http://www.opengis.net/gml}id')=='GUID_1TRE8quZ16sRs1mpyCTSpo':
                building = Building(element)
                building_ps = building.getPolygon()
                total_ps.append(building_ps)
            # print one building
            # if building_count==10:
            #     break

                del building
                flag = True

        if flag:
            element.clear()

    # buildingcount: 192
    print "buildingcount:",building_count

    del context
    util.saveobj(total_ps, './citygml_data/obj/building_onewall2.obj')
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
