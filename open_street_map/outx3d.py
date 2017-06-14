__author__ = 'wlw'
from lxml import etree as ET


def concatenate(x, y):
    return x + ' ' + y


def getIdxPoints(b_ps):
    b_coordidx = ''
    b_points = ''
    k = 0
    for sur_ps in b_ps:
        try:
            sur_ps = list(map(str, sur_ps))
            b_points = b_points + reduce(concatenate, sur_ps) + ' '
        except TypeError:
            continue

        for i in xrange(len(sur_ps)/3):
            b_coordidx = b_coordidx + str(k) + ' '
            k += 1

        b_coordidx += '-1 '
    # print b_points
    # print b_coordidx
    return b_coordidx, b_points


def generateX3D(total_ps, x3dpath, b_ids, partIds_idx):
    flag = 0
    for b_ps in total_ps:
        b_coordidx, b_points = getIdxPoints(b_ps)
        if flag == 0:
            tree = ET.parse('base.x3d')
        else:
            tree = ET.parse(x3dpath)

        root = tree.getroot()
        group = root.find('.//Group')
        shape = ET.SubElement(group, 'Shape')
        apr = ET.SubElement(shape, 'Appearance')
        matr = ET.SubElement(apr, 'Material')
        matr.set('diffuseColor', '1 0 0')
        ifs = ET.SubElement(shape, 'IndexedFaceSet')
        ifs.set('DEF', 'building_'+b_ids[partIds_idx[flag]])


        ifs.set('coordIndex', b_coordidx)
        ifs.set('solid', 'true')
        coord = ET.SubElement(ifs, 'Coordinate')
        coord.set('point', b_points)
        tree.write(x3dpath)
        flag += 1

    # delete buildings' ids
    for i in xrange(len(partIds_idx)):
        del b_ids[partIds_idx[-1-i]-len(b_ids)]


