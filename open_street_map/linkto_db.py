#coding=utf-8

import sqlite3,util
from imposm.parser import OSMParser
import time

class OSMReader(object):
    onodes={}
    oways={}
    orelations={}
    ocoord={}

    def coords(self,coords):
        for  id,lon,lat in coords:
            self.ocoord[id]=[lon,lat]

    def nodes(self,nodes):
        for id,tags,lonlat in nodes:
            self.onodes[id]=[tags,lonlat]

    def ways(self,ways):
        for  id, tags ,refs in ways:
            self.oways[id]=[tags,refs]

    def relations(self, relations):
        for id, tags, mems in relations:
            self.orelations[id] = [tags, mems]

    def getRefRect(self,refs):
        coords=[]
        upper=[]
        lower=[]
        for ref in refs:
            # print "ref:",ref
            x,y=self.ocoord[ref]
            # print 'x:y ', x,y
            # x:y 120.999148531.8511542
            coords.append([x, y])
            if len(upper)==0 and len(lower)==0:
                upper=[x,y]
                lower=[x,y]
            else:
                util.compareUpper([x,y],upper)
                util.compareLower([x,y],lower)

        return coords, [lower[0],upper[0],lower[1],upper[1]]

    def getRecIdx(self,buliding):
        id,type ,info=buliding
        # print "id:",id
        # print "type:",type
        # print "info:" ,info
        '''
            id: 478971690
            type: way
            info: [{'building': 'yes'}, [4721427389, 4721427288, 4721427287, 4721427286, 4721427389]]
        '''

        if type == "node":
            tag, lonlat = info
            lon, lat = lonlat
            x, y = util.trans([lon, lat])
            rec=[id, "node","buliding",str(tag),str([x,y])]
            idx=[id,x,x,y,y]
            # print "rec:",rec
            return rec, idx
        elif type == 'way':
            tags, refs = info
            # print "refs:",refs
            # refs: [4721427389, 4721427288, 4721427287, 4721427286, 4721427389]
            coords, lower_upper = self.getRefRect(refs)
            # print "coords:",coords
            # print "lower_upper:",lower_upper
            rec = [id, 'way', 'building', str(tags), str(coords)]
            #rec: [478971746, 'way', 'building', "{'building': 'yes'}", '[[120.9972722, 31.8497965], [120.997769, 31.8498175], [120.9977748, 31.849719], [120.9972779, 31.8496981], [120.9972722, 31.8497965]]']
            idx = [id]
            idx.extend(lower_upper)
            # print "idx:", idx
            # idx: [478971695, 120.9990761, 120.9996678, 31.8460168, 31.846198]
            # print "rec:",rec
            return rec, idx
        elif type == 'relation':
            return [], []

    def insertdb(self,bulidings,path="city.db"):
        conn = sqlite3.Connection(path)
        cur = conn.cursor()

        rec=[]
        idx=[]
        # print "bulidings:",bulidings
        for buliding in bulidings:
            # print "buliding:", buliding
            # buliding: [478971660, 'way', [{'building': 'yes'}, [4721427213, 4721427212, 4721427211, 4721427210, 4721427213]]]
            b_rec, b_idx=self.getRecIdx(buliding)
            # print "b_rec:",b_rec
            # print "b_idx:",b_idx
            # b_idx: [478971575, 120.986958, 120.987497, 31.8546064, 31.8547503]
            # b_rec: [478971645, 'way', 'building', "{'building': 'yes'}", '[[120.9996203, 31.8483708], [121.0000932, 31.8484016], [121.0001024, 31.8482991], [120.9996296, 31.8482683], [120.9996203, 31.8483708]]']
            if len(b_idx) > 0:
                rec.append(b_rec)
                idx.append(b_idx)
            print "rec:",rec

            # 每1000条数据插入一次
            if len(rec) == 1000:
                try:
                    # rec是[ [], [], [] ]，也可以是[ (), (), () ]
                    # executemany: 一次性插入多条数据，比execut一条一条插入快多了
                    cur.executemany('insert into nantongosm values (?,?,?,?,?)', rec)
                    cur.executemany('insert into nantongosm_rt values (?,?,?,?,?)', idx)
                    conn.commit()
                except sqlite3.IntegrityError, err:
                    conn.rollback()
                    print 'error: ', err

                rec = []
                idx = []

        # 将剩下的未满1000条的数据插入数据库中
        if len(rec) > 0:
            try:
                cur.executemany('insert into nantongosm values (?,?,?,?,?)', rec)
                cur.executemany('insert into nantongosm_rt values (?,?,?,?,?)', idx)
                conn.commit()
            except sqlite3.IntegrityError, err:
                conn.rollback()
                print 'error: ', err

        conn.close()

    def getBuilding(self):
        node_bs=[]
        way_bs=[]
        relation_bs=[]
        # print "self.onodes:",self.onodes #能打印出node,像这样3472561537: [{'name:en': 'Xingsu Huayuan', 'name': u'\u661f\u82cf\u82b1\u82d1', 'shelter': 'no', 'bench': 'no', 'highway': 'bus_stop', 'network': u'\u5357\u901a\u5e02\u533a\u516c\u4ea4'}
        '''
        for id in self.onodes:
            tags,lonlat=self.onodes[id]
            # print "tags:",tags
            for tag in tags:
                if tag=="building":
                    node_bs.append([id,"node",[tags,lonlat]])
                    # print"node_bs:",node_bs #无符合要求的
        '''


        for id in self.oways:
            tags,refs=self.oways[id]
            for tag in tags:
                # print "tag:", tag
                if tag=="building":
                    way_bs.append([id,"way",[tags,refs]])
                    # print"way_bs:", way_bs #有符合要求的值

        '''
        for id in self.orelations:
            tags, mems = self.orelations[id]
            for tag in tags:
                # print "tag:",tag
                if tag == 'building':
                    relation_bs.append([id, 'relation', [tags, mems]])
                    # print "relation_bs:",relation_bs
        '''
        self.insertdb(node_bs)
        self.insertdb(way_bs)  #way_bs have data










def createdb():
    conn = sqlite3.connect("city2.db")
    tbname = 'nantongosm'
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
    p.parse('/home/huangby/PycharmProjects/basestudy2/open_street_map/osm_data/nantong.osm')
    reader.getBuilding()


if __name__ == '__main__':
    # createdb()
    start = time.time()
    conn = sqlite3.connect("city.db")
    getOSM()
    # cur = conn.cursor()
    # cur.execute("select * from nantongosm")
    # print cur.fetchall()
    total = time.time() - start
    print 'total time: ', total
