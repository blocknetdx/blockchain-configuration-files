#!/usr/bin/env python3
import requests
import json
import os, sys, os.path

BASE_GITHUB_API_URL = 'https://api.github.com/repos/'

GITHUB_PERSONAL_ACCESS_TOKEN = 'token-here'

with open('manifest.json', encoding='utf-8') as json_file:
    data = json.load(json_file)

for chain in data:
    # get latest version

    latest_ver_id = chain['versions'][-1]

    account_name, repo_name = chain['repo_url'].split("/")[-2:]

    repo_latest_url = BASE_GITHUB_API_URL + account_name + "/" + repo_name + "/releases/latest"
    repo_tags_url = BASE_GITHUB_API_URL + account_name + "/" + repo_name + "/tags"

    try:
        response = requests.get(repo_latest_url, headers={"content-type":"application/json", "Authorization": "token " + GITHUB_PERSONAL_ACCESS_TOKEN})

        if response.status_code != 404:
            release_tag = response.json()["tag_name"]

        else:
            response = requests.get(repo_tags_url, headers={"content-type":"application/json", "Authorization": "token " + GITHUB_PERSONAL_ACCESS_TOKEN})
            release_tag = response.json()[0]["name"]
                        

        if release_tag != latest_ver_id:
            
            print(chain["ticker"] + " Version inconsistency. Old: " + latest_ver_id + ". New: " + release_tag)
            #TODO: Build new Docker Image

            #TODO: Start XB Unit tests
            
            #TODO: Update manifest.
        else:
            print(chain["ticker"] + " No Version inconsistency")
            
    except Exception as e: 
        print(e)
    
