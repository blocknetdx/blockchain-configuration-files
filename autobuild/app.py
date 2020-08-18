#!/usr/bin/env python3
from jinja2 import Template
import json
import os, sys, os.path
import random
import string
import urllib.request
import argparse
import configparser

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


from jinja2 import Environment, FileSystemLoader, Template

COIN_LIST='Bitcoin'
J2_ENV = Environment(loader=FileSystemLoader(''),
                     trim_blocks=True)


with open('../manifest.json') as json_file:
    data = json.load(json_file)


for chain in data:
    #print (chain['blockchain'])
    if chain['blockchain'] in COIN_LIST:
        
        print('start: {}'.format(chain['ver_id']))
        #print(chain)
        # load base config for specific coin
        base_config_fname = 'configs/{}.base.j2'.format(chain['ticker'].lower())
        base_config_template = J2_ENV.get_template(base_config_fname)
        base_config = json.loads(base_config_template.render())
        #print(base_config['BTC'])
        merged_dict = (Merge(chain,base_config[chain['ticker']]))
        #print(json.dumps(merged_dict, indent=2))
        # get version data
        coin_title, p, this_coin_version = chain['ver_id'].partition('--')
        print(this_coin_version)
        #print(json.dumps(merged_dict['versions'], indent=2))
        version_data = merged_dict['versions'][this_coin_version]
        # load xb j2
        print(version_data)
        custom_template_fname = 'templates/xbridge.conf.j2'
        custom_template = J2_ENV.get_template(custom_template_fname)
        updated_dict = Merge(version_data,merged_dict) 
        #print(updated_dict)
        rendered_data = custom_template.render(updated_dict)

        #print(rendered_data)

        
        custom_template_wallet_conf = 'templates/wallet.conf.j2'
        custom_template_wallet = J2_ENV.get_template(custom_template_wallet_conf)
        wallet_rendered_data = custom_template_wallet.render(updated_dict) 
        print(wallet_rendered_data)

