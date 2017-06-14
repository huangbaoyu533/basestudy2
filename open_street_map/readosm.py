# coding:utf-8
__author__ = 'wlw'


import sqlite3, util
from imposm.parser import OSMParser
import time


# 只提取了<tag>标签中k="building"的<way>


class OSMReader(object):
    # 存放投影后的[x, y]
    ocoords = {}
    # 存放[tags, lonlat]
    onodes = {}
    # 存放[tags, refs]
    oways = {}
    # 存放[tags, mems]
    orelations = {}

    # 并没有用到？？？
    #upper = []
    #lower = []

    # 输出不带<tag>标签的<node>
    # [(id, lon, lat)]
    def coords(self, coords):
        for id, lon, lat in coords:
            self.ocoords[id] = util.trans([lon, lat])
            '''
            if len(self.upper) == 0 and len(self.lower) == 0:
                # 仍然还是经纬度，没有投影！！
                self.upper = [lon, lat]
                self.lower = [lon, lat]
            else:
                util.compareUpper([lon, lat], self.upper)
                util.compareLower([lon, lat], self.lower)
            '''

    # 输出带<tag>标签的<node>
    # [(id, {tags}, (lon, lat))]
    def nodes(self, nodes):
        for id, tags, lonlat in nodes:
            self.onodes[id] = [tags, lonlat]

    # [(id, {tags}, [refs])]
    def ways(self, ways):
        for id, tags, refs in ways:
            self.oways[id] = [tags, refs]

    # [(id, {tags}, [(ref, type, role)])]
    # 其中: [(ref, type, role)]是<member>
    def relations(self, relations):
        for id, tags, mems in relations:
            self.orelations[id] = [tags, mems]

    def getRefRect(self, refs):
        coords = []
        upper = []
        lower = []
        for ref in refs:
            x, y = self.ocoords[ref]
            coords.append([x, y])
            if len(upper) == 0 and len(lower) == 0:
                upper = [x, y]
                lower = [x, y]
            else:
                util.compareUpper([x, y], upper)
                util.compareLower([x, y], lower)
        return coords, [lower[0], upper[0], lower[1], upper[1]]

    def getRecIdx(self, building):
        # node building: [id, 'node', [tags, lonlat]]
        # way building: [id, 'way', [tags, refs]]
        id, type, info = building

        if type == 'node':
            tags, lonlat = info
            lon, lat = lonlat
            x, y = util.trans([lon, lat])
            # 作为berlinosm表的一条记录
            rec = [id, 'node', 'building', str(tags), str([x, y])]
            # 作为berlinosm_rt表的一条记录
            idx = [id, x, x, y, y]
            return rec, idx
        elif type == 'way':
            tags, refs = info
            coords, lower_upper = self.getRefRect(refs)
            rec = [id, 'way', 'building', str(tags), str(coords)]
            idx = [id]
            idx.extend(lower_upper)
            return rec, idx
        elif type == 'relation':
            return [], []

    def insertdb(self, buildings, path='city.db'):
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        rec = []
        idx = []
        for building in buildings:
            b_rec, b_idx = self.getRecIdx(building)
            if len(b_idx) > 0:
                rec.append(b_rec)
                idx.append(b_idx)

            # 每1000条数据插入一次
            if len(rec) == 1000:
                try:
                    # rec是[ [], [], [] ]，也可以是[ (), (), () ]
                    # executemany: 一次性插入多条数据，比execut一条一条插入快多了
                    cur.executemany('insert into berlinosm values (?,?,?,?,?)', rec)
                    cur.executemany('insert into berlinosm_rt values (?,?,?,?,?)', idx)
                    conn.commit()
                except sqlite3.IntegrityError, err:
                    conn.rollback()
                    print 'error: ', err

                rec = []
                idx = []

        # 将剩下的未满1000条的数据插入数据库中
        if len(rec) > 0:
            try:
                cur.executemany('insert into berlinosm values (?,?,?,?,?)', rec)
                cur.executemany('insert into berlinosm_rt values (?,?,?,?,?)', idx)
                conn.commit()
            except sqlite3.IntegrityError, err:
                conn.rollback()
                print 'error: ', err

        conn.close()

    def getBuilding(self):
        node_bs = []
        way_bs = []
        relation_bs = []

        for id in self.onodes:
            tags, lonlat = self.onodes[id]
            for tag in tags:
                if tag == 'building':
                    node_bs.append([id, 'node', [tags, lonlat]])

        for id in self.oways:
            tags, refs = self.oways[id]
            for tag in tags:
                if tag == 'building':
                    way_bs.append([id, 'way', [tags, refs]])

        for id in self.orelations:
            tags, mems = self.orelations[id]
            for tag in tags:
                if tag == 'building':
                    relation_bs.append([id, 'relation', [tags, mems]])

        self.insertdb(node_bs)
        self.insertdb(way_bs)


def createdb():
    conn = sqlite3.connect("city.db")
    tbname = 'nantong'
    rtname = tbname + '_rt'

    tbsql = '''
    CREATE TABLE tbname(
      id INTEGER PRIMARY KEY,
      kind TEXT ,
      subKind TEXT,
      tags TEXT,
      boundary TEXT
    );
    '''

    rtsql = '''
    CREATE VIRTUAL TABLE rtname USING rtree(
      id,
      minX, maxX,
      minY, maxY
    );
    '''

    tbsql = tbsql.replace('tbname', tbname)
    rtsql = rtsql.replace('rtname', rtname)
    conn.execute(tbsql)
    conn.execute(rtsql)
    conn.commit()
    conn.close()


def getOSM():
    reader = OSMReader()
    p = OSMParser(concurrency=4, coords_callback=reader.coords, nodes_callback=reader.nodes, ways_callback=reader.ways, relations_callback=reader.relations)
    p.parse('./osm_data/nantong.osm')
    reader.getBuilding()


if __name__ == '__main__':
    # createdb()
    start = time.time()
    getOSM()
    total = time.time() - start
    print 'total time: ', total