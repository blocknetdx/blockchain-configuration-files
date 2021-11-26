#!/usr/bin/env python3
import json
import os, sys, os.path
import argparse
from jinja2 import Environment, FileSystemLoader

def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def write_file(filename, rendered_data):
    #logging.info('Creating File: {}'.format(filename))
    with open(filename, "w") as fname:
        fname.write(rendered_data)
    return

parser = argparse.ArgumentParser()
parser.add_argument('--coins', help='List of coins. Eg.: BTC, LTC, DASH', default=False)
args = parser.parse_args()
list_coins = args.coins

if list_coins:
    COIN_LIST = []
    list_coins = list_coins.split(',')
    for coin in list_coins:
        ticker = coin.strip().upper()
        COIN_LIST.append(ticker)
        
WALLETCONFPATH='../wallet-confs/'
XBRIDGECONFPATH='../xbridge-confs/'

if not os.path.isdir(WALLETCONFPATH):
    os.mkdir(WALLETCONFPATH)
print('checking walletconfpath: {}'.format(os.path.isdir(WALLETCONFPATH)))
if not os.path.isdir(XBRIDGECONFPATH):
    os.mkdir(XBRIDGECONFPATH)

print('checking xb: {}'.format(os.path.isdir(XBRIDGECONFPATH)))

J2_ENV = Environment(loader=FileSystemLoader(''),
                     trim_blocks=True)


with open('../manifest-latest.json') as json_file:
    data = json.load(json_file)
    if not list_coins:
        COIN_LIST = list(set([chain['ticker'] for chain in data]))
        COIN_LIST.sort(key = lambda t:t, reverse = False)

for chain in data:
    #print (chain['blockchain'])
    if chain['ticker'] in COIN_LIST:
        
        print('start: {}'.format(chain['ver_id']))
        #print(chain)
        # load base config for specific coin
        base_config_fname = 'configs/{}.base.j2'.format(chain['ticker'].lower())
        base_config_template = J2_ENV.get_template(base_config_fname)
        base_config = json.loads(base_config_template.render())
        #print(base_config['BTC'])
        print(base_config)
        merged_dict = (Merge(chain,base_config[chain['ticker']]))
        #print(json.dumps(merged_dict, indent=2))
        # get version data
        coin_title, p, this_coin_version = chain['ver_id'].partition('--')
        print(this_coin_version)
        #print(json.dumps(merged_dict['versions'], indent=2))
        try:
            version_data = merged_dict['versions'][this_coin_version]
        except Exception as e:
            print('error, check manifest: {}'.format(chain['ticker']))
            print(merged_dict['versions'])
            raise Exception
        # load xb j2
        print(version_data)
        custom_template_fname = 'templates/xbridge.conf.j2'
        custom_template = J2_ENV.get_template(custom_template_fname)
        updated_dict = Merge(version_data,merged_dict) 
        #print(updated_dict)
        rendered_data = custom_template.render(updated_dict)
        write_file(XBRIDGECONFPATH+chain['ver_id']+'.conf', rendered_data)
        #print(rendered_data)

        
        custom_template_wallet_conf = 'templates/wallet.conf.j2'
        custom_template_wallet = J2_ENV.get_template(custom_template_wallet_conf)
        wallet_rendered_data = custom_template_wallet.render(updated_dict) 
        #print(wallet_rendered_data)
        write_file(WALLETCONFPATH+chain['ver_id']+'.conf', wallet_rendered_data) # writes wallet conf

