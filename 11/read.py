import shapefile
reader= shapefile.Reader("/home/huangby/PycharmProjects/basestudy2/11/stockholm/data/3D_Block/Farsta_Utskr-3D-Kuber_shp/Byggnad_area.shp")

# schema of the shapefile
print dict((d[0],d[1:]) for d in reader.fields[1:])

fields = [field[0] for field in reader.fields[1:]]
for feature in reader.shapeRecords():
    geom = feature.shape.__geo_interface__
    atr = dict(zip(fields, feature.record))
    print geom, atr











