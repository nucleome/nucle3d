#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET
def _iterChr(root):
    pass
def main():
    if len(sys.argv) < 4:
        print("Usage: cmm2nucle3d file.cmm genomeVersion Resolution")
        exit(1)
    tree = ET.parse(sys.argv[1])
    genome = sys.argv[2]
    res = sys.argv[3]
    root = tree.getroot()
    lastchr = ""
    print("TITLE\t%s" % root.attrib["name"])
    print("GENOME\t%s" % genome)
    for child in root:
        tag = child.tag
        a = child.attrib
        if tag == "marker":
            if lastchr != a["chrID"]:
                lastchr = a["chrID"]
                print("CHR\t%s\t%s" % (lastchr,res))
            print("%s,%s,%s,%s"  % (a["id"],a["x"],a["y"],a["z"]))
if __name__ == "__main__":
    main()
