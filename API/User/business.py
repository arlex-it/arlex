from flask_restplus import abort

from bdd.db_connection import session, User, to_dict
from API.Utilities.HttpResponse import *
import datetime
import re
import bcrypt

regex_mail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(12))


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def get_user(request):
    if not request:
        abort(400)

    if 'mail' not in request.args:
        return jsonify({'error': 'Mail is missing'}), 403
    user = session.query(User).filter(User.mail == request.args['mail']).first()
    if not user:
        return HttpResponse(403).error(ErrorCode.USER_NFIND)

    res = {
        'user': to_dict(user)
    }
    return HttpResponse().custom(res)

def delete_user(request, user_id):
    """
    Delete an user
    :param request:
    :param user_id:
    :return: Httreponse
    """
    if not request:
        abort(400)
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return HttpResponse(403).error(ErrorCode.USER_NFIND)
    infos = request.json
    infos["date_update"] = datetime.datetime.now()
    try:
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
    return HttpResponse(202).success(SuccessCode.USER_DELETED)

def create_user(request):
    if not request:
        abort(400)

    if not re.search(regex_mail, request.json['mail']):
        return HttpResponse(403).error(ErrorCode.MAIL_NOK)

    existing = session.query(User).filter(User.mail == request.json['mail']).first()

    if existing:
        return HttpResponse(403).error(ErrorCode.MAIL_USED)

    hashed = get_hashed_password(request.json['password'])
    new_user = User(
        date_insert=datetime.datetime.now(),
        date_update=datetime.datetime.now(),
        is_active=0,
        status=0,
        gender=request.json['gender'],
        lastname=request.json['lastname'],
        firstname=request.json['firstname'],
        mail=request.json['mail'],
        password=hashed,
        country=request.json['country'],
        town=request.json['town'],
        street=request.json['street'],
        street_number=request.json['street_number'],
        region=request.json['region'],
        postal_code=request.json['postal_code']
    )

    try:
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(201).success(SuccessCode.USER_CREATED, {'id': new_user.id, 'user': to_dict(new_user)})


def update_user(request, user_id):
    if not request:
        abort(400)

    """
    if user_connected_with_token != user_id:
        error = {
            'error': 'Action interdite: Tentative d'action sur un compte non identifié'
        }
        return jsonify(error), 403
    """

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return HttpResponse(403).error(ErrorCode.USER_NFIND)

    infos = request.json
    if 'mail' in infos:
        if not re.search(regex_mail, request.json['mail']):
            return HttpResponse(403).error(ErrorCode.MAIL_NOK)

        existing = session.query(User).filter(User.mail == infos['mail']).first()
        if existing:
            return HttpResponse(403).error(ErrorCode.MAIL_USED)

    infos['date_update'] = datetime.datetime.now()
    try:
        session.query(User).filter(User.id == user_id).update(infos)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(202).success(SuccessCode.USER_UPDATED)
