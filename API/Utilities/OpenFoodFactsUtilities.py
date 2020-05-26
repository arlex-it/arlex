from flask import jsonify
from flask_restplus import abort
import os.path
import requests
import hashlib

class OpenFoodFactsUtilities:
    """
    Class for tools about OpenFoodFacts
    """
    def __init__(self):
        pass

    """
    Add the product in cache. if the product already exist, get and return it.
    ;:param url: url to find
    """
    def get_open_request_cache(self, url):
        name = hashlib.md5(url.encode()).hexdigest() + '.json'
        file_path = 'OpenRequestCache/' + name
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data = f.readline()
        else:
            data = requests.get(url).text
            with open(file_path, 'w+') as f:
                f.write(data)
        return data
