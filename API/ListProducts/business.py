from flask import jsonify
from flask_restplus import abort
import requests


def get_list_products(request):
    if not request:
        abort(400)
    j = requests.get('http://35.210.200.125:5000/').json()
    return jsonify(j)
