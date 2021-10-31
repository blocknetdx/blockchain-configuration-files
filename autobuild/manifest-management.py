#!/usr/bin/env python3

import json
import os, sys, os.path

MANIFEST_PATH = '.\\manifest.json'

def read_file():
    with open(MANIFEST_PATH) as json_file:
        data = json.load(json_file)
        return data

def write_file(filename, data):
    with open(filename, "w") as fname:
        json.dump(data, fname, indent = 4)
    return

def main():
    menu()

def menu():
    print()
    print("************Manifest Management**************")
    
    choice = input("""
A: Add New Chain  (add new chain to manifest)
U: Update Existing Chain (add or remove sub version)
D: Delete Chain (delete chain from manifest)
Q: Quit

Please enter your choice: """)

    if choice == "A" or choice =="a":
        add()
    elif choice == "U" or choice =="u":
        update()
    elif choice == "D" or choice=="d":
        delete()
    elif choice == "Q" or choice=="q":
        exit()
    else:
        print("You must only select either (A)dd, (U)pdate, (D)elete or (Q)uit")
        menu()

def yes_no_question(question):
    while True:
        is_delete = input(question)
        if is_delete == 'y' or is_delete == 'Y':
            return True
        elif is_delete == 'n' or is_delete == 'N':
            return False
        else:
            print('Not a valid answer. Try again')
            continue

add_input_fields = {
    'blockchain': "Blockchain name (e.g. Bitcoin): \t\t\t\t",
    'ticker': "Ticker (e.g. BTC): \t\t\t\t\t\t",
    'ver_id': "Version Id (e.g. bitcoin--v0.20.0): \t\t\t\t",
    'ver_name': "Name version group (e.g. Bitcoin v0.20.x): \t\t\t",
    'conf_name': "Name Config file (e.g. bitcoin.conf): \t\t\t\t",
    'dir_name_linux': "Name blockchain folder data directory Linux (e.g. bitcoin): \t",
    'dir_name_mac': "Name blockchain folder data directory Mac (e.g. bitcoin): \t",
    'dir_name_win': "Name blockchain folder data directory Windows (e.g. bitcoin): \t",
    'repo_url': "URL Github Repository: \t\t\t\t\t\t",
    'versions': "Comma seperated list of versions (e.g. v0.20.0,v0.20.1): \t",
    'xbridge_conf': "Name XBridge Conf file (e.g. bitcoin--v0.20.1.conf: \t\t",
    'wallet_conf': "Name Wallet Conf file (e.g. bitcoin--v0.20.1.conf: \t\t"
}

def add_edit_input(entry):
    while True:
        edit_field = input('Which field would you like to edit (e.g. blockchain)? ')
        if edit_field not in entry.keys():
            print('Not a valid field. Try again')
            continue
        
        print()
        break

    return edit_field

def add_correct_input(entry):
    entry_json = json.dumps(entry, indent = 4)
    print(entry_json)
    print()

    answer = yes_no_question("Is the input correct? [y/n]: ")

    if answer:
        data = read_file()
        print('Adding {ticker} to manifest.json ...'.format(ticker = entry['ticker']))
        data.append(entry)
        data = sorted(data, key = lambda d: (d['blockchain'].lower()), reverse= False)
        write_file(MANIFEST_PATH, data)
        
    else:
        edit_field = add_edit_input(entry)

        entry[edit_field] = input(add_input_fields[edit_field])
        add_correct_input(entry)


def add():
    blockchain = input(add_input_fields['blockchain'])
    ticker = input(add_input_fields['ticker'])
    ver_id = input(add_input_fields['ver_id'])
    ver_name = input(add_input_fields['ver_name'])
    conf_name = input(add_input_fields['conf_name'])
    dir_name_linux = input(add_input_fields['dir_name_linux'])
    dir_name_mac = input(add_input_fields['dir_name_mac'])
    dir_name_win = input(add_input_fields['dir_name_win'])
    repo_url = input(add_input_fields['repo_url'])
    versions = input(add_input_fields['versions'])
    xbridge_conf = input(add_input_fields['xbridge_conf'])
    wallet_conf = input(add_input_fields['wallet_conf'])

    print()
    entry = {
        'blockchain': blockchain,
        'ticker': ticker,
        'ver_id': ver_id,
        'ver_name': ver_name,
        'conf_name': conf_name,
        'dir_name_linux': dir_name_linux,
        'dir_name_mac': dir_name_mac,
        'dir_name_win': dir_name_win,
        'repo_url': repo_url,
        'versions': versions.split(","),
        'xbridge_conf': xbridge_conf,
        'wallet_conf': wallet_conf
    }

    add_correct_input(entry)

    menu()

def update():
    sep = '--'
    print()
    chain_id = input("Ticker (e.g. BTC): ").upper()
    
    data = read_file()

    if not does_chain_exist(data, chain_id):
        menu()

    chain_configs = [chain for chain in data if chain['ticker'] == chain_id]

    if yes_no_question("Do you want to add a new subversion? [y/n]: "):
        version_ids = get_version_ids_chain(chain_configs)

        question_answer = ("To which ver_id of {ticker} do you want to add a subversion? (e.g. {version}): ","ver_id {version} for {ticker} does not exist in manifest")
        selected_version = ask_version_chain(chain_configs, version_ids, question_answer)

        chain = next((c for c in data if c['ver_id'] == selected_version), None)

        new_subversion = input("New subversion (e.g. v0.20.1): ")
        if yes_no_question("Are you sure you want to add subversion {subversion} to {ticker}? [y/n]: ".format(subversion = new_subversion, ticker = chain['ticker'])):
            chain['versions'].append(new_subversion)

            chain['ver_id'] = selected_version.split(sep, 1)[0] + sep + new_subversion
            write_file(MANIFEST_PATH, data)

    elif yes_no_question("Do you want to delete a subversion? [y/n]: "):
            versions = get_versions_chain(chain_configs)

            question_answer = ("Which subversion do you want to delete from {ticker}? (e.g. {version}): ","Version {version} for {ticker} does not exist")
            selected_version = ask_version_chain(chain_configs, versions, question_answer)
            
            chain = next((c for c in data if c['ver_id'] == selected_version), None)
            
            if yes_no_question("Are you sure you want to delete subversion {subversion} to {ticker}? [y/n]: ".format(subversion = selected_version, ticker = chain['ticker'])):
                chain['versions'].remove(selected_version.split(sep, 1)[1])
                
                latest_version = chain['versions'][-1]
                chain['ver_id'] = selected_version.split(sep, 1)[0] + sep + latest_version
                
                write_file(MANIFEST_PATH, data)
       
    menu()


def delete():
    print()
    chain_id = input("Ticker (e.g. BTC): ").upper()

    data = read_file()
    if not does_chain_exist(data, chain_id):
        menu()

    chain_configs = [chain for chain in data if chain['ticker'] == chain_id.upper()]

    versions = get_version_ids_chain(chain_configs)

    question_answer = ("Which version of {ticker} do you want to delete from manifest? (e.g. {version}): ","Version {version} for {ticker} does not exist in manifest")
    selected_version = ask_version_chain(chain_configs, versions, question_answer)

    answer = yes_no_question("Are you sure you want to delete {version} ? [y/n]: ".format(version=selected_version))
    if answer:
        print('Deleting {version} from manifest.json ...'.format(version = selected_version))
        data = [d for d in data if not d['ver_id'] == selected_version]
        write_file(MANIFEST_PATH, data)
    else:
        print('Not deleting {ticker}'.format(ticker = chain_id))

    menu()
    
def ask_version_chain(chain_configs, versions, question_answer):
    chain_id = chain_configs[0]['ticker']

    sep = '--'
    while True:
        if len(versions) > 1:
            print()
            print(versions)
            print()
            version_input = input(question_answer[0].format(ticker = chain_id, version = versions[0]))
        else:
            version_input = versions[0]

        if does_version_exist(chain_configs, version_input):
            return chain_configs[0]['ver_id'].split(sep, 1)[0] + sep + version_input
        
        print(question_answer[1].format(version = version_input, ticker = chain_id))


def get_version_ids_chain(chain_configs):
    sep = '--'
    if len(chain_configs) > 1:
        version_ids = [config['ver_id'].split(sep, 1)[1] for config in chain_configs]

    else:
        version_ids = [chain_configs[0]['ver_id'].split(sep, 1)[1]]

    return version_ids

def get_versions_chain(chain_configs):
    versions = []
    if len(chain_configs) > 1:
        for chain_config in chain_configs:
            for ver in chain_config['versions']:
                versions.append(ver)
    else:       
        versions = chain_configs[0]['versions']

    return versions

def does_version_exist(chain_configs, version):
    versions = []

    if len(chain_configs) > 1:
        for chain_config in chain_configs:
            for ver in chain_config['versions']:
                versions.append(ver)
    
    else:
        versions = chain_configs[0]['versions']

    version_exists = next((v for v in versions if v == version), None)
    if version_exists is not None:
        return True

    return False


def does_chain_exist(data, chain_id):
    chain_configs = [chain for chain in data if chain['ticker'] == chain_id.upper()]

    if len(chain_configs) == 0:
        print()
        print("Chain not found")
        return False
    
    return True

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)