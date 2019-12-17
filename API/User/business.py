from flask_restplus import abort

from bdd.db_connection import session, User, to_dict, Token
from API.Utilities.HttpResponse import *
from API.Utilities.CheckAuthToken import *
import datetime
import re
import bcrypt
from uuid import uuid4

regex_mail = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'


def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(12))


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def get_user(request):
    if not request:
        abort(400)

    if 'mail' in request.args:
        user = session.query(User).filter(User.mail == request.args['mail']).first()
        if not user:
            return HttpResponse(403).error(ErrorCode.USER_NFIND)
        res = {
            'user': to_dict(user)
        }
        return HttpResponse().custom(res)

    users = session.query(User).filter()
    res = {
        'users': [to_dict(x) for x in users]
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

    # token generation for new user
    new_token = Token(
        date_insert=datetime.datetime.now(),
        access_token=uuid4().hex[:35],
        refresh_token=uuid4().hex[:35],
        id_user=new_user.id,
        expiration_date=datetime.datetime.now() + datetime.timedelta(weeks=2)
    )
    print(new_token)
    try:
        session.add(new_token)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(201).success(SuccessCode.USER_CREATED, {'id': new_user.id})


def update_user(request, user_id):
    if not request:
        abort(400)

    infos = request.json
    if not CheckAuthToken.check_user(request=request):
        return HttpResponse(403).error(ErrorCode.BAD_TOKEN)
    infos.pop('access_token')
    infos.pop('refresh_token')

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

    if 'mail' in infos:
        if not re.search(regex_mail, request.json['mail']):
            return HttpResponse(403).error(ErrorCode.MAIL_NOK)

        existing = session.query(User).filter(User.mail == infos['mail']).first()
        if existing:
            return HttpResponse(403).error(ErrorCode.MAIL_USED)

    if 'password' in infos:
        hashed = get_hashed_password(infos['password'])
        infos['password'] = hashed
    infos['date_update'] = datetime.datetime.now()
    try:
        session.query(User).filter(User.id == user_id).update(infos)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(202).success(SuccessCode.USER_UPDATED)
