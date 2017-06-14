# coding:utf-8
import xmltodict
import time
import json
from lxml import etree



# 将指定tag的对象提取，写入json文件。
def process_element(elem):
    elem_data = etree.tostring(elem)
    elem_dict = xmltodict.parse(elem_data, attr_prefix="", cdata_key="")
    # print(elem_dict)

    if (elem.tag == "node"):
        elem_jsonStr = json.dumps(elem_dict["node"])
        fnode.write(elem_jsonStr + "\n")
    elif (elem.tag == "way"):
        elem_jsonStr = json.dumps(elem_dict["way"])
        fway.write(elem_jsonStr + "\n")
    elif (elem.tag == "relation"):
        elem_jsonStr = json.dumps(elem_dict["relation"])
        frelation.write(elem_jsonStr + "\n")


# 遍历所有对象，然后调用process_element处理。
# 迭代处理，func为迭代的element处理函数。
def fast_iter(context, func, maxline):
    placement = 0
    try:
        for event, elem in context:
            placement += 1
            if (maxline > 0):  # 最多的转换对象限制，大数据调试时使用于抽样检查。
                print(etree.tostring(elem))
                if (placement >= maxline): break

            func(elem)  # 处理每一个元素,调用process_element.
            elem.clear()
            while elem.getprevious() is not None:
                del elem.getparent()[0]
    except Exception as ex:
        #print(time.strftime(ISOTIMEFORMAT), ", Error:", ex)
        pass

    del context


# 需要处理的osm文件名，自行修改。
osmfile = './osm_data/nantong.osm'
maxline = 0  # 抽样调试使用，最多转换的对象，设为0则转换文件的全部。
# ISOTIMEFORMAT = "%Y-%m-%d %X"
# print(time.strftime(ISOTIMEFORMAT), ", Process osm XML...", osmfile, " =>MaxLine:", maxline)

fnode = open(osmfile + "_node.json", "w+")
fway = open(osmfile + "_way.json", "w+")
frelation = open(osmfile + "_relation.json", "w+")

context = etree.iterparse(osmfile, tag=["node", "way", "relation"])
fast_iter(context, process_element, maxline)

fnode.close()
fway.close()
frelation.close()

#print(time.strftime(ISOTIMEFORMAT), ", OSM to JSON, Finished.")