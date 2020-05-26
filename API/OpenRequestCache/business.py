from flask import jsonify
from flask_restplus import abort

from API.Utilities.OpenFoodFactsUtilities import OpenFoodFactsUtilities

def get_open_request_cache(request):
    if not request or not request.json or 'url' not in request.json:
        abort(400)
    url = request.json['url']
    if type(url) is not str:
        abort(400)
    return OpenFoodFactsUtilities().get_open_request_cache(url)
