#!/usr/bin/env python3
import os, sys, os.path
import json

if len(sys.argv) < 2:
    print('Provide a xbridge file name as argument (e.g. xbridgep2p_20200716.log')
    exit()

FILE_NAME = sys.argv[1]

order_id = input("Order id: ")

def parse_line(line):
    sep = '{'
    if sep in line:
        splitted_line = line.split(sep, 1)
        parsed_json = json.loads(sep + splitted_line[1].rstrip())
        return (splitted_line[0], json.dumps(parsed_json, indent = 4))
    sep = ']'
    if sep in line:
        splitted_line = line.split(sep, 2)
        return (splitted_line[0] + sep + splitted_line[1] + sep, splitted_line[2])
    return ('*** TODO ****', line)

with open('{filename}'.format(filename = FILE_NAME),'r') as f:
    outputs = [parse_line(line) for line in f if order_id in line]

for output in outputs:
    print()
    print(output[0])
    print(output[1])
