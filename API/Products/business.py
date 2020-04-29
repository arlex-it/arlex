import requests
from flask import jsonify
from flask_restplus import abort
from bdd.db_connection import session, Product, to_dict
from API.Utilities.HttpResponse import *
import datetime

urlopenfoodfact = 'https://world.openfoodfacts.org/api/v0/product/{}.json'


def create_products(request):
    if not request:
        abort(400)

    id_user = 1
    user_id = 1
    try:
        datetime.datetime.strptime(request.json['expiration_date'], "%Y-%m-%d")
    except ValueError:
        return HttpResponse(400).custom({
            "errors": {
                "expiration_date": "'{}' is not of type 'date'".format(request.json['expiration_date'])
            },
            "message": "Input payload validation failed"
        })

    if request.json['id_rfid'] < 0:
        return HttpResponse(403).error(ErrorCode.ID_RFID_NOK)

    new_product = Product(
        date_insert=datetime.datetime.now(),
        date_update=datetime.datetime.now(),
        expiration_date=request.json['expiration_date'],
        status=0,
        id_rfid=request.json['id_rfid'],
        id_ean=request.json['id_ean'],
        position=request.json['position'],
        id_user=id_user,
    )

    try:
        session.begin()
        session.add(new_product)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)

    return HttpResponse(201).success(SuccessCode.PRODUCT_CREATED, {'id': new_product.id})


def get_products(request, product_id):
    if not request:
        abort(400)

    products = session.query(Product).filter(Product.id == product_id).first()
    if not products:
        return HttpResponse(403).error(ErrorCode.PRODUCT_NFIND)

    product = requests.get(urlopenfoodfact.format(products.id_ean))
    return HttpResponse(200).custom({
        'success': 'On a retrouvé le produit.',
        'position': products.position,
        'expiration_date': products.expiration_date,
        'id_ean': products.id_ean,
        'informations': product.json()
    })


def delete_products(request, product_id):
    """
    Delete a product
    :param request:
    :param product_id:
    :return:
    """
    if not request:
        abort(400)

    product = session.query(Product).filter(Product.id == product_id).first()
    if not product:
        return HttpResponse(403).error(ErrorCode.PRODUCT_NFIND)
    try:
        session.begin()
        session.query(Product).filter(Product.id == product_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
    return HttpResponse(202).success(SuccessCode.PRODUCT_DELETED)
