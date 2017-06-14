__author__ = 'wlw'
import os, sqlite3
# import outx3d
from lxml import etree as ET


def getIdxPoints(way_ps):
    b_coordidx = ''
    b_points = ''
    k = 0
    for sur_ps in way_ps:
        sur_ps.append(30)
        sur_ps = list(map(str, sur_ps))
        b_points = b_points + reduce(outx3d.concatenate, sur_ps) + ' '

        for i in xrange(len(sur_ps)/3):
            b_coordidx = b_coordidx + str(k) + ' '
            k += 1

    b_coordidx += '-1 '
    return b_coordidx, b_points


def generateWay(total_ps, x3dpath):
    n = 1
    for way_ps in total_ps:
        way_coordidx, way_points = getIdxPoints(way_ps)

        tree = ET.parse(x3dpath)
        root = tree.getroot()
        group = root.find('.//Group')
        shape = ET.SubElement(group, 'Shape')
        apr = ET.SubElement(shape, 'Appearance')
        matr = ET.SubElement(apr, 'Material')
        matr.set('emissiveColor', '0 0 1')
        ils = ET.SubElement(shape, 'IndexedLineSet')
        ils.set('DEF', 'way_'+str(n))
        ils.set('coordIndex', way_coordidx)
        ils.set('solid', 'true')
        coord = ET.SubElement(ils, 'Coordinate')
        coord.set('point', way_points)
        tree.write(x3dpath)

        n += 1

if __name__ == '__main__':
    conn = sqlite3.connect('city.db')
    cur = conn.cursor()
    path = './app/static/x3d/Spandau/'
    for x3dfile in os.listdir(path):
        print 'x3dfile: ', x3dfile
        bId = x3dfile[:-4]
        cur.execute('select lowerCorner, upperCorner from building where bId=?', (bId,))
        low_up = cur.fetchall()
        low = eval(low_up[0][0])
        up = eval(low_up[0][1])

        result = []
        for boundary in cur.execute('select berlinosm.boundary from berlinosm, berlinosm_rt where berlinosm.id=berlinosm_rt.id and minX>=? and maxX<=? and minY>=? and maxY<=?', (low[0], up[0], low[1], up[1])):
            points = eval(boundary[0])
            result.append(points)

        print 'len result: ', len(result)
        x3dpath = os.path.join(path, x3dfile)
        generateWay(result, x3dpath)

    conn.close()





