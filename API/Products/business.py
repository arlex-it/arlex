import requests
from flask import jsonify
from flask_restplus import abort
from bdd.db_connection import session, Product, to_dict
from API.Utilities.HttpResponse import *
import datetime

urlopenfoodfact = 'https://world.openfoodfacts.org/api/v0/product/{}.json'


def post_product(request, id_user=None):
    if not request:
        abort(400)

    if id_user is None:
        id_user = 1
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

    try:
        created_product = create_product(request.json, id_user)
    except Exception as e:
        return HttpResponse(407).error(ErrorCode.ID_RFID_NOK, e)

    return HttpResponse(201).success(SuccessCode.PRODUCT_CREATED, {'id': created_product.id})

def create_product(product, id_user):

    # TODO : APPELEZ LA FONCTION get_open_request_cache dans OPen food facts utilities
    product_info = requests.get(urlopenfoodfact.format(product['id_ean'])).json()
    if not "product" in product_info:
        raise Exception("Erreur sur lors de la creation du produit")


    name = product_info['product']['product_name_fr'][:100]
    name_gen = product_info['product']['generic_name_fr'][:100]

    new_product = Product(
        date_insert=datetime.datetime.now(),
        date_update=datetime.datetime.now(),
        expiration_date=product['expiration_date'],
        status=0,
        id_rfid=product['id_rfid'],
        id_ean=product['id_ean'],
        position=product['position'],
        id_user=id_user,
        product_name=name,
        product_name_gen=name_gen
    )

    try:
        session.begin()
        session.add(new_product)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        raise Exception("Erreur lors de la création du produit")

    return new_product

def get_product_name_with_rfid(id_rfid):
    """
    return the product name with rfid
    :param param:
    :param name_colomn_to_search:
    :return:
    """

    product = session.query(Product).filter(Product.id_rfid == id_rfid).first()
    return product.product_name


def link_product_to_user_with_id_rfid(id_rfid, id_user):
    """
    Link a product to with a user by id rfid
    :param id_rfid:
    :param id_user:
    :return: True if the modification    is ok
            False if not
    """
    product = session.query(Product).filter(Product.id_rfid == id_rfid).first()
    info = {
        "date_update": datetime.datetime.now(),
        "id_user": id_user
    }
    try:
        session.begin()
        session.query(Product).filter(Product.id_rfid == id_rfid).update(info)
        session.commit()
    except Exception as e:
        session.rollback()
        session.flush()
        raise e

def post_products(list_ean, id_user):
    product_added = []
    for elem in list_ean:
        try:
            product_added.append(create_product(elem, id_user))
        except Exception as e:
            raise Exception(e)
    return product_added

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
