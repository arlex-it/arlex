from flask import jsonify
from flask_restplus import abort
import os.path
import requests
import hashlib


def get_open_request_cache(request):
    if not request or not request.json or 'url' not in request.json:
        abort(400)
    url = request.json['url']
    if type(url) is not str:
        abort(400)
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
