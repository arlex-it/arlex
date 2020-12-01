import datetime
import re
import requests

from flask import jsonify
from flask_restplus import abort

from API.Utilities.EanUtilities import EanUtilities
from API.Utilities.HttpResponse import HttpResponse
from API.Products.business import link_product_to_user_with_id_rfid, get_product_name_with_rfid
from API.Utilities.Levenshtein import calc_similarity
from bdd.db_connection import session, AccessToken, Product, to_dict, IdArlex, Sensor
from API.Utilities.ErrorEnum import *
from API.Utilities.SuccesEnum import *


class SensorBusiness():
    url_capteur_augustin = 'https://415771d98c1c.ngrok.io/'

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

    def post_products(self, request):
        """
        Link new products to a users
        """
        res = requests.get(self.url_capteur_augustin).json()

        old_products_list = session.query(IdArlex).join(Product, Product.id == IdArlex.product_id).filter(
            Product.id_user == self.user_connected).all()

        # get all id_rfid of user's products
        id_rfid_list = [id_rfid.id for id_rfid in old_products_list]

        # convert id_rfid in str
        converted_list = [str(i) for i in id_rfid_list]

        # get all products that are found by the sensor
        res_list = [str(i) for i in res["Product"]]
        # check if there are new products
        new_elements = [item for item in res_list if item not in converted_list]
        if len(new_elements) == 0:
            return HttpResponse(200).custom({'state': "J'ai déjà enregistré tout les produits dans votre armoire."})

        # link all new products to a user and link id_rfid to id_arlex
        name_new_element = []
        for element in new_elements:
            if link_product_to_user_with_id_rfid(element, self.user_connected) != -1:
                name_new_element.append(get_product_name_with_rfid(element))

        name_to_return = ', '.join(name_new_element)
        if not name_to_return:
            return HttpResponse(200).custom({'state': "Je n'ai pas trouvé le produit."})
        return HttpResponse(200).custom({'state': f'Vous avez ajouté: {name_to_return}'})

    def change_name(self, request):
        """
        Rename a sensor
        """
        data = request.json
        if not data or not data["old_name"] or not data["new_name"]:
            return HttpResponse(400).custom(
                {"state": "Il manque des informations pour renommer le capteur"})
        old_name = data["old_name"]
        new_name = data["new_name"]

        sensors = session.query(Sensor).filter(Sensor.id_user == self.user_connected).all()
        best_score = -1
        sensor = None
        # find sensor by calculating  its similarity with sensors in database
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

        new_infos = {
            'name': new_name,
            'date_update': datetime.datetime.now()
        }

        try:
            session.begin()
            session.query(Sensor).filter(Sensor.id == sensor.id).update(new_infos)
            session.commit()
        except Exception as e:
            session.rollback()
            session.flush()
            return HttpResponse(404).custom(
                {"state": "{}. Veuillez réessayer. (Erreur détaillée : {})".format(ErrorCode.DB_ERROR, e.args)})

        return HttpResponse(202).custom({"state": f"Le nouveau nom du capteur: {old_name}, est maintenant: {new_name}"})

    def get_product_position(self, request):
        product_name = request.args.get('product_name')
        if product_name is None:
            return HttpResponse(200).custom({'state': f'Nous n\'avons pas pu récupérer le nom du produit demandé.'})

        # TODO Decommenter cette ligne quand on aura plusieurs capteurs
        # sensors_list = session.query(Sensor).filter(Sensor.id_user == self.user_connected).all()
        sensor = session.query(Sensor).filter(Sensor.id_user == self.user_connected).first()

        if sensor is None:
            return HttpResponse(200).custom({'state': f'Nous n\'avons pas trouvé vos capteurs.'})

        try:
            data = requests.get(self.url_capteur_augustin)
            data = data.json()

            # set all products that were at this position to status 2
            info = {
                "status": 2
            }
            try:
                session.begin()
                session.query(Product).filter(Product.position == sensor.name).update(info)
                session.commit()
            except Exception as e:
                session.rollback()
                session.flush()
                raise e

            info = {
                "status": 1,
                "position": sensor.name
            }
            # set all products found by the sensor to status 1 and set the position
            for id_patch in data['Product']:
                try:
                    session.begin()
                    session.query(Product)\
                        .filter(Product.id == IdArlex.product_id)\
                        .filter(IdArlex.patch_id == id_patch)\
                        .update(info, synchronize_session="fetch")
                    session.commit()
                except Exception as e:
                    session.rollback()
                    session.flush()
                    raise e
        except Exception as e:
            print(f"Cannot refresh product position. {e.args}")

        # get all products found by the sensor
        products_list = session.query(Product).filter(Product.id_user == self.user_connected, Product.status == 1).all()
        ean_list = EanUtilities().search_product(products_list, product_name)

        if len(ean_list) == 0:
            return HttpResponse(200).custom({'state': f'Nous n\'avons pas trouvé de produit correspondant à votre recherche: {product_name}.'})

        # get product with best similarity
        first = ean_list[0]
        product = session.query(Product).filter(Product.id == first['id']).first()
        product = to_dict(product)
        return HttpResponse(200).custom({'state': f"Nous avons trouvé: {product['product_name']}, dans: {product['position']}."})

    def link_sensor_user(self, request, id_sensor, id_user):
        """
        Link a sensor to a user only if this sensor does not exist
        :param id_sensor:
        :param id_user:
        """
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

    def name_sensor(self, request, id_sensor, name):
        """
        Name a sensor if it is already link to a user
        """
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

    def get_list_name(self, request):
        """
        List all user's sensors
        """
        if not request:
            abort(400)
        sensor_list = session.query(Sensor).filter(Sensor.id_user == self.user_connected, Sensor.is_active).all()
        #sensor_list = session.query(Sensor).all()
        if not sensor_list or len(sensor_list) == 0:
            return HttpResponse(500).error(ErrorCode.SENSOR_NDETECTED)

        res = 'Voici la liste des endroits où je peux trouver des produits :'
        for x in sensor_list:
            sensor = to_dict(x)
            if len(res) > 61:
                res += ','
            res += ' ' + sensor['name']
        return HttpResponse(201).custom({'state': res})
