#!/usr/bin/env python3
import json
import os, sys, os.path
from shutil import copyfile
import glob

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

    old_wallet_conf_ver = chain['wallet_conf']
    new_wallet_conf_ver = old_wallet_conf_ver.split(sep, 1)[0] + sep + latest_ver_id + '.conf'
    chain['wallet_conf'] = new_wallet_conf_ver

    if old_xbridge_conf_ver.split('.conf', 1)[0].lower() != chain['ver_id'].lower():
        copyfile(XBRIDGE_SRC_BASE_DIR + old_xbridge_conf_ver, XBRIDGE_SRC_BASE_DIR + new_xbridge_conf_ver)

    if old_wallet_conf_ver.split('.conf', 1)[0].lower() != chain['ver_id'].lower():
        copyfile(WALLET_SRC_BASE_DIR + old_wallet_conf_ver, WALLET_SRC_BASE_DIR + new_wallet_conf_ver)

    # find xbridge and wallet conf that are stale/old and not in versions array anymore

    versions = []
    #check if there are multiple occurrences of a chain in manifest. for example multiple bitcoin entries
    #then append all those versions into one versions list
    chain_configs = [ch for ch in data if ch['ticker'] == chain['ticker']]
    if len(chain_configs) > 1:
        for chain_config in chain_configs:
            for ver in chain_config['versions']:
                versions.append(ver)
    else:       
        versions = chain['versions']


    xbridge_conf_files_path = os.getcwd() + '\\xbridge-confs\\' + old_xbridge_conf_ver.split(sep, 1)[0] + sep + '*.conf'
    for conf_path in glob.glob(xbridge_conf_files_path):
        conf_file_filename =  os.path.basename(os.path.normpath(conf_path))
        conf_file_version = conf_file_filename.split(sep, 1)[1].split('.conf')[0]
        if conf_file_version not in versions:            
            os.remove(conf_path)
    
    wallet_conf_files_path = os.getcwd() + '\\wallet-confs\\' + old_wallet_conf_ver.split(sep, 1)[0] + sep + '*.conf'
    for conf_path in glob.glob(wallet_conf_files_path):
        conf_file_filename =  os.path.basename(os.path.normpath(conf_path))
        conf_file_version = conf_file_filename.split(sep, 1)[1].split('.conf')[0]
        if conf_file_version not in versions:            
            os.remove(conf_path)

sorted_data = sorted(data, key = lambda d: (d['blockchain'].lower()), reverse= False)
write_file(os.getcwd() + '\\manifest.json', sorted_data)
