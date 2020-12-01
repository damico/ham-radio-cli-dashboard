import json
import os

import requests


def read_json_url(url):
    jsonResponse = None
    code = 0
    try:
        r = requests.get(url)
        code = r.status_code
        jsonResponse = r.json()
    except Exception as e:
        if code == 403:
            print(code, url)
            raise Exception(e)
    return jsonResponse


def read_json_io(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data



