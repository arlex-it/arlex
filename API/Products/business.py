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
    return product.json()


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
        session.query(Product).filter(Product.id == product_id).delete()
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
    return HttpResponse(202).success(SuccessCode.PRODUCT_DELETED)
