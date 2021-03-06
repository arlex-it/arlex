from flask_restplus import abort

from bdd.db_connection import session, User, to_dict
from API.Utilities.HttpResponse import *
from API.Utilities.OAuthAuthenticationToken import *
from API.Utilities.auth import check_user_permission
import datetime
import re
import bcrypt
import uuid

from bdd.db_connection import User, RefreshToken, AuthApplication, session, to_dict

regex_mail = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
regex_name = '^[a-zA-ZÀ-ú\-\s]*$'
regex_postal = '^\d{2}[ ]?\d{3}$'
regex_address = '^[a-zA-ZÀ-ú0-9 ]*$'

def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt(12))


def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password)


def check_user_infos(infos):
    if 'mail' in infos and not re.search(regex_mail, infos['mail']):
        return ErrorCode.MAIL_NOK
    if 'gender' in infos and infos['gender'] < 0:
        return ErrorCode.GENDER_NOK
    if 'firstname' in infos and not re.search(regex_name, infos['firstname']):
        return ErrorCode.NAME_NOK
    if 'lastname' in infos and not re.search(regex_name, infos['lastname']):
        return ErrorCode.NAME_NOK
    if 'postal_code' in infos and not re.search(regex_postal, infos['postal_code']):
        return ErrorCode.POSTAL_NOK
    if 'country' in infos and not re.search(regex_address, infos['country']):
        return ErrorCode.COUNTRY_NOK
    if 'street' in infos and not re.search(regex_address, infos['street']):
        return ErrorCode.STREET_NOK
    if 'town' in infos and not re.search(regex_address, infos['town']):
        return ErrorCode.CITY_NOK
    if 'region' in infos and not re.search(regex_address, infos['region']):
        return ErrorCode.REGION_NOK
    return None


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

    if not check_user_permission(user_id):
        error = {
            'error': 'Action interdite: Tentative d\'action sur un compte non identifié'
        }
        return HttpResponse(403).custom(error)

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return HttpResponse(403).error(ErrorCode.USER_NFIND)
    try:
        session.begin()
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

    verification = check_user_infos(request.json)
    if verification is not None:
        return HttpResponse(403).error(verification)

    existing = session.query(User).filter(User.mail == request.json['mail']).first()

    if existing:
        return HttpResponse(403).error(ErrorCode.MAIL_USED)

    hashed = get_hashed_password(request.json['password'])
    new_user = User(
        date_insert=datetime.datetime.now(),
        date_update=datetime.datetime.now(),
        is_active=1,
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
        session.begin()
        session.add(new_user)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    app_id = session.query(AuthApplication).filter(AuthApplication.project_id == "arlex-ccevqe").first().id
    access_token = AccessToken(
        app_id=app_id,
        type='bearer',
        token=uuid.uuid4().hex[:35],
        date_insert=datetime.datetime.now(),
        id_user=new_user.id,
        expiration_date=datetime.datetime.now() + datetime.timedelta(weeks=2),
        is_enable=1,
        scopes="user"
    )

    try:
        session.begin()
        session.add(access_token)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    refresh_token = RefreshToken(
        app_id=app_id,
        date_insert=datetime.datetime.now(),
        token=uuid.uuid4().hex[:35],
        is_enable=True,
        access_token_id=access_token.id,
    )
    try:
        session.begin()
        session.add(refresh_token)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(201).success(SuccessCode.USER_CREATED, {'id': new_user.id, 'access_token': access_token.token, 'refresh_token': refresh_token.token})


def update_user(request, user_id):
    if not request:
        abort(400)
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return HttpResponse(403).error(ErrorCode.USER_NFIND)

    infos = request.json
    verification = check_user_infos(infos)
    if verification is not None:
        return HttpResponse(403).error(verification)

    if 'mail' in infos:
        existing = session.query(User).filter(User.mail == infos['mail']).first()
        if existing:
            return HttpResponse(403).error(ErrorCode.MAIL_USED)

    if 'password' in infos:
        hashed = get_hashed_password(infos['password'])
        infos['password'] = hashed
    infos['date_update'] = datetime.datetime.now()
    try:
        session.begin()
        session.query(User).filter(User.id == user_id).update(infos)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(202).success(SuccessCode.USER_UPDATED)
