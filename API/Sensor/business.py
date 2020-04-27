from flask import jsonify
from flask_restplus import abort
from API.Utilities.HttpResponse import HttpResponse


def get_list_of_product(request):
    if not request:
        abort(400)
    res = {
        'state': 'Dev dans cette fonction !!'
    }
    return HttpResponse(200).custom(res)
