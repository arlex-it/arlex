import re
import requests

from flask import jsonify
from flask_restplus import abort
from API.Utilities.HttpResponse import HttpResponse
from API.Utilities.HttpRequest import HttpRequest
from bdd.db_connection import session, AccessToken, to_dict
from API.Utilities.ErrorEnum import *

def get_list_of_product(request):
    if not request:
        abort(400)
    httprequest = HttpRequest()
    header_token = httprequest.get_header("Authorization")

    if not header_token:
        return HttpResponse().error(ErrorCode.USER_NFIND)

    reg = re.compile('Bearer ([A-Za-z0-9-=]+)')
    result = reg.findall(header_token)

    if not result:
        return HttpResponse().error(ErrorCode.USER_NFIND)

    token = result[0]

    user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
    user_connected = to_dict(user_connected)
    print(user_connected["id_user"])

    res = requests.get('http://35.210.200.125:5000/').json()
    print(res)

    if len(res['product_list']) == 0:
        state_res = 'Il n\'y a rien dans votre armoire'
    else:
        state_res = 'Dans votre armoire il y a : '
        product = ", ".join(res['product_list'])
        state_res += product

    return HttpResponse(200).custom({'state': state_res})
