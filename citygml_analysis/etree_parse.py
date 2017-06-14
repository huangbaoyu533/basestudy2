from xml.etree import ElementTree
with open('./citygml_data/Stadt-Ettenheim-LoD3_edited_v1.0.0.gml', 'rt') as f:
    tree = ElementTree.parse(f)
# print tree
#  extract all building wall
# for node in tree.iter():
#     if node.tag.endswith('Building'):
#         print  'node.tag:,node.attrib:',node.tag,node.attrib
#         id=node.get('{http://www.opengis.net/gml}id')
#         print 'id:', id
#         # {http: // www.opengis.net / citygml / building / 1.0}Building
#         # {'{http://www.opengis.net/gml}id': 'GUID_3EEyfL6AX0ofG0QI0fPER3'}





import xml.etree.cElementTree as ET
tree = ET.ElementTree(file='./citygml_data/Berlin_Pariser_Platz_v1.0.0/Berlin_Pariser_Platz_v1.0.0.xml')
# print tree.getroot()
root = tree.getroot()
for node in root.iter():
    # print node.tag, node.attrib
    if node.tag.endswith('Building'):
        id = node.get('{http://www.opengis.net/gml}id')
        print 'id:', id





# {http://www.opengis.net/citygml/building/1.0}WallSurface {'{http://www.opengis.net/gml}id': 'GUID_2X3QojYJv9vg1zDd2L6UBY'}