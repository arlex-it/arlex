from flask import jsonify
from flask_restplus import abort
from API.Utilities.HttpResponse import HttpResponse
from API.Utilities.HttpRequest import HttpRequest

def get_list_of_product(request):
    if not request:
        abort(400)
    res = {
        'state': 'Dev dans cette fonction !!'
    }
    httprequest = HttpRequest()
    header_token = httprequest.get_header("Authorization")
    print(header_token)
    return HttpResponse(200).custom(res)
