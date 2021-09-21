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


def write_file(filename, rendered_data):
    #logging.info('Creating File: {}'.format(filename))
    with open(filename, "w") as fname:
        fname.write(rendered_data)
    return


from jinja2 import Environment, FileSystemLoader, Template

COIN_LIST='ABET,ABS,AEX,AGM,APR,ATB,AUS,BAD,BCD,BCH,BCZ,BIT,BITG,BLAST,BLOCK,BSD,BTC,BTDX,BTG,BTX,BZX,CARE,CDZC,CHC,CHN,CIV,CNMC,COLX,CRAVE,D,DASH,DGB,DIVI,DMD,DOGE,DOGEC,DSR,DVT,DYN,ECA,EMC,EMC2,ENT,FAIR,FGC,FJC,FLO,GALI,GBX,GEEK,GIN,GMCN,GXX,HASH,HATCH,HLM,HTML,INN,IOP,IXC,JEW,JIYOX,KLKS,KREDS,KYDC,KZC,LBC,LTC,LUX,LYNX,MAC,MLM,MNP,MONA,MUE,N8V,NIX,NMC,NOR,NORT,NYEX,NYX,ODIN,OHMC,OPCX,ORE,PAC,PHL,PHR,PIVX,POLIS,PURA,QBIC,QTUM,RAP,REEX,RPD,RVN,SCN,SCRIBE,SEND,SEQ,SIB,SPK,STAK,SUB1X,SYS,TRB,TRC,UFO,UNO,VIA,VITAE,VIVO,VSX,VTC,WAGE,WGR,XC,XMCC,XMY,XN,XP,XVG,XZC'

WALLETCONFPATH='wallet_confs/'
XBRIDGECONFPATH='xbridge_confs/'

if not os.path.isdir(WALLETCONFPATH):
    os.mkdir(WALLETCONFPATH)
print('checking walletconfpath: {}'.format(os.path.isdir(WALLETCONFPATH)))
if not os.path.isdir(XBRIDGECONFPATH):
    os.mkdir(XBRIDGECONFPATH)

print('checking xb: {}'.format(os.path.isdir(XBRIDGECONFPATH)))

J2_ENV = Environment(loader=FileSystemLoader(''),
                     trim_blocks=True)


with open('../manifest.json') as json_file:
    data = json.load(json_file)


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

