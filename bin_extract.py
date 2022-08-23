#!/usr/bin/env python3

import sys
import os
import json
from string import Template

config = "bin_extract.config.json"
binary_file = ""
class BinPart:
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size
    def __str__():
        return {"name":f"{self.name}","offset":f"{self.offset}","size":f"{self.size}"}

if(len(sys.argv) < 2):
    print("not enough arguments")
    sys.exit(1)


bin_parts = []
bin_parts_json = []
if(not os.path.exists(config) or sys.argv[1]=="config"):
    binary_file = input("binary file : ")
    while(True):
        name = input("Name of part (\"stop\" when enough) : ")
        if(name=="stop"): break
        offset = input("offset : ")
        size = input("size : ")
        bin_parts.append(BinPart(name, offset, size))
        bin_parts_json.append({"name":f"{name}","offset":f"{offset}","size":f"{size}"})
        print(bin_parts_json)
    cfg = open(config,"w")
    text = f"{{\"binary\":\"{binary_file}\",\"parts\":{json.dumps(bin_parts_json)}}}"
    cfg.write(text)
    cfg.close()


bin_parts_json = json.loads(open(config,"r").read())
print(bin_parts_json)
binary_file=bin_parts_json["binary"]
print(binary_file)

if(sys.argv[1]=="unpack"):
    f = open(binary_file, "rb")
    for part in firmware_parts:
        outfile = open(part.name, "wb")
        f.seek(part.offset, 0)
        data = f.read(part.size)
        outfile.write(data)
        outfile.close()
        print(f"Wrote {part.name} - {hex(len(data))} bytes")











