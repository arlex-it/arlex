from flask import jsonify
from flask_restplus import abort


def get_test(request):
    if not request:
        abort(400)
    j = {
        'res': True
    }
    return jsonify(j)
