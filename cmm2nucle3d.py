#!/usr/bin/env python
import sys
import xml.etree.ElementTree as ET


def _iterChr(root):
    pass


def main():
    if len(sys.argv) < 4:
        print("Usage: cmm2nucle3d file.cmm genomeVersion binsize")
        exit(1)
    tree = ET.parse(sys.argv[1])
    genome = sys.argv[2]
    binsize = sys.argv[3]
    root = tree.getroot()
    lastchr = ""
    index = 0
    print("TITLE\t%s" % root.attrib["name"])
    print("GENOME\t%s" % genome)
    print("BINSIZE\t%s" % binsize)
    for child in root:
        tag = child.tag
        a = child.attrib
        if tag == "marker":
            if lastchr != a["chrID"]:
                lastchr = a["chrID"]
                print("CHR\t%s" % lastchr)
                index = 0
            print("%s,%s,%s,%s" % (index, a["x"], a["y"], a["z"]))
            index += 1


if __name__ == "__main__":
    main()
