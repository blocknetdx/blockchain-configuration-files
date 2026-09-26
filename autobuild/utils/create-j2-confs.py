#!/usr/bin/env python3
import json
import os, sys, os.path
import string
import argparse
from configparser import ConfigParser

J2_CONF_PATH='../configs/'
WALLETS_PATH='../../wallet-confs/'
XBRIDGE_PATH='../../xbridge-confs/'

def write_file(filename, data):
    with open(filename, "w") as fname:
        json.dump(data, fname, indent = 4)
    return

def get_wallet_conf(path):
    wallet_conf_parser = ConfigParser()
    with open(path) as wallet_stream:
        wallet_conf_parser.read_string("[top]\n" + wallet_stream.read())

    wallet_conf_data = dict(wallet_conf_parser.items('top'))
    # testnet confs keep port/rpcport (and optionally other overrides) in the
    # [test] section (standard SelectConfigNetwork behavior); surface those so
    # the rpcPort/p2pPort defaults resolve for testnet coins
    if 'testnet' in wallet_conf_data and wallet_conf_parser.has_section('test'):
        for key, value in wallet_conf_parser.items('test'):
            wallet_conf_data.setdefault(key, value)

    return wallet_conf_data

def get_xbridge_conf(path, ticker):
    xbridge_conf_parser = ConfigParser()
    xbridge_conf_parser.read(path)

    return dict(xbridge_conf_parser.items(ticker))

parser = argparse.ArgumentParser()
parser.add_argument('--coins', help='List of coins', default=False)
args = parser.parse_args()
list_coins = args.coins

if list_coins:
    tickers = []
    list_coins = list_coins.split(',')
    for coin in list_coins:
        ticker = coin.strip().upper()
        tickers.append(ticker)

with open('../../manifest-latest.json') as json_file:
    data = json.load(json_file)
    if not list_coins:
        tickers = list(set([chain['ticker'] for chain in data]))
        tickers.sort(key = lambda t:t, reverse = False)

    for ticker in tickers:
        chains = [chain for chain in data if chain['ticker'] == ticker]
        chains.sort(key = lambda c:c['ver_id'], reverse = False)

        template_data = {}
        # get latest version
        latest_version_chain = chains[-1]
        xbridge_conf_data = get_xbridge_conf(XBRIDGE_PATH + latest_version_chain['xbridge_conf'], latest_version_chain['ticker'])
        wallet_conf_data = get_wallet_conf(WALLETS_PATH + latest_version_chain['wallet_conf'])
        template_data['Title'] = xbridge_conf_data['title']
        template_data['Address'] = xbridge_conf_data['address']
        template_data['Ip'] = xbridge_conf_data['ip']
        template_data['rpcPort'] = '{{ rpcPort|default(' + wallet_conf_data['rpcport'] + ')}}'
        template_data['p2pPort'] = '{{ p2pPort|default(' + wallet_conf_data['port'] + ')}}'
        template_data['Username'] = '{{ rpcusername }}'
        template_data['Password'] = '{{ rpcpassword }}'
        if 'addressprefix' in xbridge_conf_data:
            template_data['AddressPrefix'] = xbridge_conf_data['addressprefix']
        if 'scriptprefix' in xbridge_conf_data:
            template_data['ScriptPrefix'] = xbridge_conf_data['scriptprefix']
        if 'secretprefix' in xbridge_conf_data:
            template_data['SecretPrefix'] = xbridge_conf_data['secretprefix']
        if 'coin' in xbridge_conf_data:
            template_data['COIN'] = xbridge_conf_data['coin']
        if 'minimumamount' in xbridge_conf_data:
            template_data['MinimumAmount'] = xbridge_conf_data['minimumamount']
        if 'dustamount' in xbridge_conf_data:
            template_data['DustAmount'] = xbridge_conf_data['dustamount']
        if 'createtxmethod' in xbridge_conf_data:
            template_data['CreateTxMethod'] = xbridge_conf_data['createtxmethod']
        if 'getnewkeysupported' in xbridge_conf_data:
            template_data['GetNewKeySupported'] = xbridge_conf_data['getnewkeysupported']
        if 'importwithnoscansupported' in xbridge_conf_data:
            template_data['ImportWithNoScanSupported'] = xbridge_conf_data['importwithnoscansupported']
        if 'mintxfee' in xbridge_conf_data:
            template_data['MinTxFee'] = xbridge_conf_data['mintxfee']
        if 'blocktime' in xbridge_conf_data:
            template_data['BlockTime'] = xbridge_conf_data['blocktime']
        if 'txversion' in xbridge_conf_data:
            template_data['TxVersion'] = xbridge_conf_data['txversion']
        if 'feeperbyte' in xbridge_conf_data:
            template_data['FeePerByte'] = xbridge_conf_data['feeperbyte']
        if 'confirmations' in xbridge_conf_data:
            template_data['Confirmations'] = xbridge_conf_data['confirmations']
        if 'txwithtimefield' in xbridge_conf_data:
            template_data['TxWithTimeField'] = xbridge_conf_data['txwithtimefield']
        if 'lockcoinssupported' in xbridge_conf_data:
            template_data['LockCoinsSupported'] = xbridge_conf_data['lockcoinssupported']
        if 'cashaddrprefix' in xbridge_conf_data:
            template_data['CashAddrPrefix'] = xbridge_conf_data['cashaddrprefix']
        if 'contenttype' in xbridge_conf_data:
            template_data['ContentType'] = xbridge_conf_data['contenttype']
        if 'jsonversion' in xbridge_conf_data:
            template_data['JSONVersion'] = xbridge_conf_data['jsonversion']
        
        coin_base_j2_data_versions = {}
        for chain in chains:
            wallet_conf_data = get_wallet_conf(WALLETS_PATH + chain['wallet_conf'])
            xbridge_conf_data = get_xbridge_conf(XBRIDGE_PATH + chain['xbridge_conf'], chain['ticker'])
            
            # get first of versions list of chain 
            # version = chain['versions'][0]
            for version in chain['versions']:
                version_data = {
                    'legacy': 'addresstype' in wallet_conf_data,
                    'xbridge_conf': chain['xbridge_conf'],
                    'wallet_conf': chain['wallet_conf']
                }
                if 'deprecatedrpc' in wallet_conf_data:
                    version_data['deprecatedrpc'] = wallet_conf_data['deprecatedrpc']
                if 'testnet' in wallet_conf_data:
                    version_data['testnet'] = True
                for wallet_key in ('txindex', 'debug', 'enableaccounts', 'staking',
                                   'blocksonly', 'walletbroadcast', 'prune', 'daemon'):
                    if wallet_key in wallet_conf_data:
                        version_data[wallet_key] = wallet_conf_data[wallet_key]
                if 'rpcserialversion' in wallet_conf_data:
                    version_data['rpcserialversion'] = int(wallet_conf_data['rpcserialversion'])
                coin_base_j2_data_versions[version] = version_data

        template_data['versions'] = coin_base_j2_data_versions

        template = {}
        template[ticker] = template_data
        
        write_file(J2_CONF_PATH + chain['ticker'].lower() + '.base.j2', template)

    print(','.join(tickers))
