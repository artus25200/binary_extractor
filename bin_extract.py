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

if(len(sys.argv) < 2):
    print("not enough arguments")
    sys.exit(1)


bin_parts = []
bin_parts_text = []
config_json = []

if(not os.path.exists(config) or sys.argv[1]=="config"):
    binary_file = input("binary file : ")
    while(True):
        name = input("Name of part (\"stop\" when enough) : ")
        if(name == "stop"): break
        offset = input("offset : ")
        size = input("size : ")
        bin_parts.append(BinPart(name, offset, size))
        bin_parts_text.append({"name":f"{name}","offset":f"{offset}","size":f"{size}"})
    cfg = open(config,"w")
    text = f"{{\"binary\":\"{binary_file}\",\"parts\":{json.dumps(bin_parts_text)}}}"
    cfg.write(text)
    cfg.close()


config_json = json.loads(open(config,"r").read())
print(config_json) #for debug purposes

binary_file = config_json["binary"]
print(binary_file) #same

bin_parts_text = config_json["parts"]
print(bin_parts_text) #same

for parts in bin_parts_text:
    bin_parts.append(BinPart(parts["name"],parts["offset"],parts["size"]))

if(sys.argv[1]=="unpack"):
    f = open(binary_file, "rb")
    for part in bin_parts:
        outfile = open(part.name, "wb")
        f.seek(int(part.offset,16), 0)
        data = f.read(int(part.size,16))
        outfile.write(data)
        outfile.close()
        print(f"Wrote {part.name} - {hex(len(data))} bytes")











