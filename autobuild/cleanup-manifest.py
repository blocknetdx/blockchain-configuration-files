#!/usr/bin/env python3
import json
import os, sys, os.path
from shutil import copyfile

XBRIDGE_SRC_BASE_DIR = os.getcwd() + '\\xbridge-confs\\'
WALLET_SRC_BASE_DIR = os.getcwd() + '\\wallet-confs\\'

def write_file(filename, data):
    with open(filename, "w") as fname:
        json.dump(data, fname, indent = 4)
    return

with open('manifest.json') as json_file:
    data = json.load(json_file)

for chain in data:
    # get latest version
    latest_ver_id = chain['versions'][-1]    

    sep = '--'
    chain['ver_id'] = chain['ver_id'].split(sep, 1)[0] + sep + latest_ver_id

    old_xbridge_conf_ver = chain['xbridge_conf']
    new_xbridge_conf_ver = old_xbridge_conf_ver.split(sep, 1)[0] + sep + latest_ver_id + '.conf'
    chain['xbridge_conf'] = new_xbridge_conf_ver

    old_walletconf_ver = chain['wallet_conf']
    new_wallet_conf_ver = old_walletconf_ver.split(sep, 1)[0] + sep + latest_ver_id + '.conf'
    chain['wallet_conf'] = new_wallet_conf_ver

    if old_xbridge_conf_ver.split('.conf', 1)[0].lower() != chain['ver_id'].lower():
        copyfile(XBRIDGE_SRC_BASE_DIR + old_xbridge_conf_ver, XBRIDGE_SRC_BASE_DIR + new_xbridge_conf_ver)

    if old_walletconf_ver.split('.conf', 1)[0].lower() != chain['ver_id'].lower():
        copyfile(WALLET_SRC_BASE_DIR + old_walletconf_ver, WALLET_SRC_BASE_DIR + new_wallet_conf_ver)
        
write_file(os.getcwd() + '\\manifest.json', data)
