import datetime
import re
import requests

from flask import jsonify
from flask_restplus import abort

from API.Utilities.EanUtilities import EanUtilities
from API.Utilities.HttpResponse import HttpResponse
from API.Products.business import post_products, link_product_to_user_with_id_rfid, get_product_name_with_rfid
from API.Utilities.Levenshtein import calc_similarity
from bdd.db_connection import session, AccessToken, Product, to_dict, IdArlex, Sensor
from API.Utilities.OpenFoodFactsUtilities import OpenFoodFactsUtilities
from API.Products.business import post_product
from API.Utilities.ErrorEnum import *
from API.Utilities.SuccesEnum import *


class SensorBusiness:
    def __init__(self, header_token=None):
        if not header_token:
            raise Exception("Token undefined")

        reg = re.compile('Bearer ([A-Za-z0-9-=]+)')
        result = reg.findall(header_token)

        if not result:
            raise Exception("Token undefined")

        token = result[0]

        user_connected = session.query(AccessToken).filter(AccessToken.token == token).first()
        users = to_dict(user_connected)
        self.user_connected = users["id_user"]

    def get_list_of_product(self, request):
        old_products_list = session.query(Product).filter(Product.id_user == self.user_connected).all()
        name_new_element = []
        for element in old_products_list:
            name_new_element.append(element.product_name)
        state_res = 'Dans votre armoire il y a : '
        product = ", ".join(name_new_element)
        state_res += product

        return HttpResponse(200).custom({'state': state_res})

    # def get_list_of_product(self, request):
    # res = requests.get('http://35.210.200.125:5000/').json()
    #
    # if len(res['product_list']) == 0:
    #     state_res = 'Il n y a rien dans votre armoire'
    # else:
    #     name_new_element = []
    #     for element in res['product_list']:
    #         name_new_element.append(get_product_name_with_rfid(element))
    #     state_res = 'Dans votre armoire il y a : '
    #     product = ", ".join(name_new_element)
    #     state_res += product

    # TODO : EN cas de nouveau produits gérer, ce cas

    # return HttpResponse(200).custom({'state': state_res})

    def post_products(self, request):
        # ip serveur benjamin
        res = requests.get('http://35.210.200.125:5000/').json()

        old_products_list = session.query(IdArlex).join(Product, Product.id == IdArlex.product_id).filter(
            Product.id_user == self.user_connected).all()

        id_rfid_list = [id_rfid.id for id_rfid in old_products_list]

        converted_list = [str(i) for i in id_rfid_list]
        res_list = [str(i) for i in res["product_list"]]
        new_elements = [item for item in res_list if item not in converted_list]
        if len(new_elements) == 0:
            return HttpResponse(200).custom({'state': "J'ai déjà enregistrer tout les produits dans votre armoire."})

        name_new_element = []
        for element in new_elements:
            if link_product_to_user_with_id_rfid(element, self.user_connected) != -1:
                name_new_element.append(get_product_name_with_rfid(element))

        name_to_return = ', '.join(name_new_element)
        if not name_to_return:
            return HttpResponse(200).custom({'state': "Je n'ai pas trouvé le produit."})
        return HttpResponse(200).custom({'state': f'Vous avez ajouté: {name_to_return}'})

    def change_name(self, request):
        data = request.json
        old_name = data["old_name"]
        new_name = data["new_name"]

        sensors = session.query(Sensor).filter(Sensor.id_user == self.user_connected).all()
        best_score = -1
        sensor = None
        for s in sensors:
            if s.name.lower() == old_name.lower():
                sensor = s
                break
            score = calc_similarity(s.name, old_name)
            if score > 0.95 and score >= best_score:
                best_score = score
                sensor = s

        if sensor is None:
            return HttpResponse(200).custom(
                {"state": f"Le capteur: {old_name}, n'a pas été trouvé. Veuillez réessayer."})
        old_name = sensor.name
        id_sensor = sensor.id
        new_infos = {
            'name': new_name,
            'date_update': datetime.datetime.now()
        }

        try:
            session.begin()
            session.query(Sensor).filter(Sensor.id == id_sensor).update(new_infos)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(404).custom(
                {"state": "{}. Veuillez réessayer. (Erreur détaillée : {})".format(ErrorCode.DB_ERROR, e.args)})

        return HttpResponse(202).custom({"state": f"Le nouveau nom du capteur: {old_name}, est maintenant: {new_name}"})

    def get_product_position(self, request):
        product_name = request.args.get('product_name')
        sensors_list = session.query(Sensor).filter(Sensor.id_user == self.user_connected).all()
        # TODO = Appeler les capteurs pour qu'ils mettent à jour la position (et le status) des produits
        # TODO = Appeler les capteurs pour qu'ils mettent à jour la position (et le status) des produits
        # TODO = Appeler les capteurs pour qu'ils mettent à jour la position (et le status) des produits

        products_list = session.query(Product).filter(Product.id_user == self.user_connected).all()
        ean_list = EanUtilities().search_product(products_list, product_name)
        if len(ean_list) == 0:
            return HttpResponse(200).custom(
                {'state': f'Nous n\'avons pas trouvé de produit correspondant à votre recherche: {product_name}.'})
        first = ean_list[0]
        product = products_list[[i for i, _ in enumerate(products_list) if _.__dict__['id'] == first['id']][0]]
        return HttpResponse(200).custom(
            {'state': f'Nous avons trouvé: {product.product_name}, dans: {product.position}'})

    # lie un sensor à un user uniquement s'il n'existe déjà pas
    def link_sensor_user(self, request, id_sensor, id_user):
        if not request:
            abort(400)
        elif id_sensor <= 0 or id_user <= 0:
            return HttpResponse(403).error(ErrorCode.UNK)

        sensor = session.query(Sensor).filter(Sensor.id == id_sensor).first()
        if sensor:
            return HttpResponse(403).error(ErrorCode.SENSOR_EXISTS)

        new_sensor = Sensor(
            id=id_sensor,
            date_insert=datetime.datetime.now(),
            date_update=datetime.datetime.now(),
            is_active=True,
            id_user=id_user,
            type=False,
            name=False,
            sensorcol=False
        )
        try:
            session.begin()
            session.add(new_sensor)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
        return HttpResponse(201).success(SuccessCode.SENSOR_LINKED, {})

    # permet de (re)nommer un sensor s'il est déjà lié à un utilisateur
    def name_sensor(self, request, id_sensor, name):
        if not request:
            abort(400)
        elif id_sensor <= 0 or len(name) == 0:
            return HttpResponse(403).error(ErrorCode.UNK)

        sensor = session.query(Sensor).filter(Sensor.id == id_sensor).first()
        if not sensor:
            return HttpResponse(403).error(ErrorCode.SENSOR_NFIND)

        try:
            session.begin()
            session.query(Sensor).filter(Sensor.id == id_sensor).update({'name': name})
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(500).error(ErrorCode.DB_ERROR, e)
        return HttpResponse(201).success(SuccessCode.SENSOR_NAME_UPDATED, {})
