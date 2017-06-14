# coding:utf-8
from xml.etree import ElementTree as ET
rootElement = ET.parse("./citygml_data/Berlin_Pariser_Platz_v1.0.0/b1_lod2_ms_w_sem.xml").getroot()
points = []
pos=[]
poslist=[]
for subelement in rootElement.getiterator():
    for subsub in subelement:
        if subsub.tag == "{http://www.opengis.net/gml}pos":
            pos = subsub.text.split(' ')
            # print "pos", pos
            poslist.extend(pos)
print "poslist:",poslist

for i in xrange(len(poslist)/3-1):
    point = [float(poslist[3*i]), float(poslist[3*i+1]), float(poslist[3*i+2])]
    # 在一个list末尾一次性追加另一个list中的多个值(结果还是一个list)
    points.extend(point)


print "pionts:",points
