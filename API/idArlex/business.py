from flask import jsonify
from flask_restplus import abort
from bdd.db_connection import session, IdArlex, to_dict
from API.Utilities.HttpResponse import *


def post_id_arlex(request):
    if not request:
        abort(400)
    existing = session.query(IdArlex).filter(IdArlex.patch_id == request.json['patch_id']).first()
    if existing:
        return HttpResponse(403).error(ErrorCode.PATCH_ID_USED)
    new_id_arlex = IdArlex(
        patch_id=request.json['patch_id']
    )

    try:
        session.begin()
        session.add(new_id_arlex)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        raise Exception(e)
    return HttpResponse(201).custom({'id_arlex': to_dict(new_id_arlex)})
