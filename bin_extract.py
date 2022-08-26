#!/usr/bin/env python3

import sys
import os
import json

project_file = "bin_extractor.project.config"


class config:
    def __init__(self):
        self.cfg_text = ""
        self.cfg_dict = []
        return

    def write(self):
        with open(project_file, "w") as cfg:
            cfg.write(json.dumps(self.project.toJson()))
            cfg.close()

    def read(self):
        with open(project_file, "r") as cfg:
            self.cfg_text = cfg.read()
            self.cfg_dict = json.loads(self.cfg_text)
            self.project = project(self.cfg_dict["project_name"])
            bin_count = len(self.cfg_dict["bin_files"])
            bins = []
            for item in self.cfg_dict["bin_files"]:
                bin_name = item
                bin_parts = self.cfg_dict["bin_files"][item]["parts"]
                parts_count = len(bin_parts)
                parts = []
                for j in range(parts_count):
                    part_name = bin_parts[j]["name"]
                    part_offset = bin_parts[j]["offset"]
                    part_size = bin_parts[j]["size"]
                    parts.append(bin_part(part_name, part_offset, part_size))
                bins.append(bin_file(bin_name, parts))
            self.project.bin_files = bins
            return json.dumps(self.cfg_dict, indent=4)

    def delete():
        if(os.exist(project_file)):
            os.remove(project_file)

    def init(self):
        self.project = project(input("Project's name : "))
        bins_count = input("How many binaries are in your project ? (1) : ")
        bins = []
        if(bins_count == ""):
            bins_count = 1
        else:
            bins_count = int(bins_count)
        print("") #new line
        for i in range(1, bins_count + 1):
            bin_name = input(f"What is the name (full filename) of binary {i} ? : ")
            parts_count = input(f"How many parts are there in \"{bin_name}\" ? (1) : ")
            parts = []
            if(parts_count == ""):
                parts_count = 1
            else:
                parts_count = int(parts_count)
            previous_size = 0x0
            previous_offset = 0x0
            print("")
            for j in range(1, parts_count + 1):
                print("")
                #try to guess offset
                if(not j == 1):
                    should_be_offset = previous_offset+previous_size
                else:
                    should_be_offset = 0x00

                part_name = input(f"What is the name of part {j} of binary {i} ? (part {j}): ")

                if(part_name == ""):
                    part_name = f"part{j}"

                part_offset = input(f"Offset of part {j} ({part_name}) ? ({hex(should_be_offset)}) : ")

                if(part_offset == ""):
                    part_offset = hex(should_be_offset)

                part_size = input(f"Size of of part {j} ({part_name}) ? : ")

                previous_offset = int(part_offset, 16)
                previous_size = int(part_size, 16)

                parts.append(bin_part(part_name, part_offset, part_size))
            bins.append(bin_file(bin_name, parts))
            print("")
        self.project.bin_files = bins
        self.write()


class project:
    def __init__(self, name):
        self.name = name
        self.bin_files = []

    def toJson(self):
        bin_files_json = {}
        for bin in self.bin_files:
            bin_files_json[bin.name] = bin.toJson()
        return {"project_name": f"{self.name}", "bin_files": bin_files_json}


class bin_file:
    def __init__(self, name, bin_parts):
        self.name = name
        self.bin_parts = bin_parts

    def toJson(self):
        bin_parts_json = []
        for part in self.bin_parts:
            bin_parts_json.append(part.toJson())
        return {"parts": bin_parts_json}


class bin_part:
    def __init__(self, name, offset, size):
        self.name = name
        self.offset = offset
        self.size = size

    def toJson(self):
        return {"name": f"{self.name}", "offset": f"{self.offset}", "size": f"{self.size}"}


def unpack(bin):
    Config.read()
    f = open(bin, "rb")
    bin_files = Config.project.toJson()["bin_files"]
    if(bin not in bin_files):
        print(f"The binary file {bin} does not exist in the config file. Please delete the config and redo it")
        exit(1)
    bin = bin_files[bin]
    for part in bin["parts"]:
        name = part["name"]
        outfile = open(name, "wb")
        f.seek(int(part["offset"], 16), 0)
        data = f.read(int(part["size"], 16))
        outfile.write(data)
        outfile.close()
        print(f"Wrote {name} - {hex(len(data))} bytes")


def pack(bin):
    Config.read()
    f = open(bin, "wb")
    bin_files = Config.project.toJson()["bin_files"]
    if(bin not in bin_files):
        print(f"The binary file {bin} does not exist in the config file. Please delete the config and redo it")
        exit(1)
    bin = bin_files[bin]
    for part in bin["parts"]:
        name = part["name"]
        i = open(name, "rb")
        data = i.read()
        f.write(data)
        padding = (int(part["size"], 16) - len(data))
        print(f"Wrote {name} - {hex(len(data))} bytes")
        print(f"Padding: {hex(padding)}")
        f.write(b'\x00' * padding)


def showHelp():
    print("Bin extractor by artus25200")
    print("Usage :")
    print(f"    {sys.argv[0]} config [init|read|delete]")
    print(f"    {sys.argv[0]} unpack [binary|all]")
    print(f"    {sys.argv[0]} pack   [binary|all]")
    print(f"    {sys.argv[0]} help")
    print("If you did not create a config and attempted to pack or unpack binaries, \
you will be ask to create a config as this tool cannot work without one")
    exit(1)


Config = config()

argv = sys.argv
if(len(argv) < 3):
    showHelp()
    sys.exit(1)
if(argv[1] == "project"):
    if(argv[2] == "init"):
        Config.init()
        exit(0)
    if(argv[2] == "read"):
        print(Config.read());
        exit(0)
    if(argv[2] == "delete"):
        Config.delete()
        exit(0)
if(argv[1] == "unpack"):
    if(argv[2] == "all"):
        exit(0)
    else:
        unpack(argv[2])
        exit(0)
if(argv[1] == "pack"):
    if(argv[2] == "all"):
        exit(0)
    else:
        pack(argv[2])
        exit(0)
showHelp()
