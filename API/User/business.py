from flask import jsonify
from flask_restplus import abort

from bdd.db_connection import session, User, to_dict
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
    row = session.query(User)
    for r in row:
        print(r)
    j = {
        'res': True
    }
    return jsonify(j)

def delete_user(request):
    row = session.query(User)
    print(row)
    session.delete(session.query(User))
    print(User)
    return jsonify(), 201

def create_user(request):
    print("ah")
    if not request:
        abort(400)

    if not re.search(regex_mail, request.json['mail']):
        return jsonify({
            'error': 'Addresse email non valide.'
        }), 403

    existing = session.query(User).filter(User.mail == request.json['mail']).first()

    if existing:
        return jsonify({
            'error': 'Addresse email déjà en utilisation.'
        }), 403

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

    session.add(new_user)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        error = {
            'error': 'Ajout dans la base de donnée',
            'message': e.args
        }
        return jsonify(error), 500

    j = {
        'id': new_user.id,
        'user': to_dict(new_user)
    }
    return jsonify(j), 201
