# Parsing XML

import xml.etree.ElementTree as ET

tree = ET.parse(r"C:\Users\SightSpectrum\Desktop\New Text Document.xml")

root = tree.getroot()

for child in root:
    print(child.tag, child.attrib)

