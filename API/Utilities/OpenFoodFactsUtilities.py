from flask import jsonify
from flask_restplus import abort
import os.path
import requests
import hashlib
import uuid
from googletrans import Translator

urlopenfoodfact = 'https://world.openfoodfacts.org/api/v0/product/{}.json'

class OpenFoodFactsUtilities:
    """
    Class for tools about OpenFoodFacts
    """
    def __init__(self):
        pass

    """
    Add the product in cache. if the product already exist, get and return it.
    ;:param url: url to find
    """
    def get_open_request_cache(self, url):
        name = hashlib.md5(url.encode()).hexdigest() + '.json'
        file_path = 'OpenRequestCache/' + name
        if os.path.isfile(file_path):
            with open(file_path) as f:
                data = f.readline()
        else:
            data = requests.get(url).text
            import io
            with io.open(file_path, "w+", encoding="utf-8") as f:
                f.write(data)
        return data

    def get_multi_products(self, ean_list):

        products = []

        for ean in ean_list:
            products.append(self.get_open_request_cache(urlopenfoodfact.format(ean)))

        return products


class OFFProduct:
    def __init__(self, ean):
        self.uuid = ean + '-' + str(uuid.uuid1())
        self.ean = ean
        self.status = None
        self.request_data = None
        self.data = None
        self.names = []
        self.name_languages = []
        self.ingredients = []
        self.ingredients_languages = []
        self.has_ingredients = True
        self.allergens = []
        self.allergens_languages = []
        self.has_allergens = True
        self.languages = []
        self.translator = Translator()

    def parse_name(self):
        try:
            name_languages = ['product_name_fr', 'product_name_en', 'product_name_es', 'product_name_it', 'product_name_de']
            for name_language in name_languages:
                if name_language in self.data and len(self.data[name_language]) > 0:
                    self.names.append(self.data[name_language])
                    self.name_languages.append(name_language)
        except:
            pass
        try:
            generic_name_languages = ['generic_name_fr', 'generic_name_en', 'generic_name_es', 'generic_name_it',
                                      'generic_name_de']
            for generic_name_language in generic_name_languages:
                if generic_name_language in self.data and len(self.data[generic_name_language]) > 0:
                    self.names.append(self.data[generic_name_language])
                    self.name_languages.append(generic_name_language)
        except:
            pass

    def parse_ingredients(self):
        try:
            ingredients_languages = ['ingredients_text_fr', 'ingredients_text_en', 'ingredients_text_es',
                                     'ingredients_text_it', 'ingredients_text_de']
            for ingredients_language in ingredients_languages:
                if ingredients_language in self.data and len(self.data[ingredients_language]) > 0:
                    self.ingredients.append(self.data[ingredients_language])
                    self.ingredients_languages.append(ingredients_language)
        except:
            pass
        try:
            if 'ingredients_hierarchy' in self.data and len(self.data['ingredients_hierarchy']) > 0:
                self.ingredients.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in
                                                   self.data['ingredients_hierarchy']]))
                self.ingredients_languages.append(self.data['ingredients_hierarchy'][0][:2])
        except:
            pass
        try:
            if 'ingredients_original_tags' in self.data and len(self.data['ingredients_original_tags']) > 0:
                self.ingredients.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in
                                                   self.data['ingredients_original_tags']]))
                self.ingredients_languages.append(self.data['ingredients_original_tags'][0][:2])
        except:
            pass
        try:
            if 'ingredients' in self.data and len(self.data['ingredients']) > 0:
                self.ingredients.append(', '.join([x['text'] for x in self.data['ingredients']]))
                self.ingredients_languages.append(None)
        except:
            pass
        if all([len(x) == 0 for x in self.ingredients]):
            self.has_ingredients = False
            self.ingredients = ['aucun ingrédient']

    def parse_allergenes(self):
        try:
            self.allergens.append(self.data['allergens_from_ingredients'])
            self.allergens_languages.append(None)
        except:
            pass
        try:
            self.allergens.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in self.data['allergens'].split(',')]))
            self.allergens_languages.append('en')
        except:
            pass
        if all([len(x) == 0 for x in self.allergens]):
            self.has_allergens = False
            self.allergens = ['aucun allergène']

    def set_explicit_none(self):
        if self.names is None:
            self.names = 'nom inconnu'
        if self.ingredients is None:
            self.ingredients = 'ingrédients inconnus'
        if self.allergens is None:
            self.allergens = 'allergènes inconnus'

    def parse_language(self):
        try:
            self.languages.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in self.data['languages_hierarchy']]))
        except:
            pass
        try:
            if 'languages' in self.data and len(self.data['languages']) > 0:
                keys = list(self.data['languages'].keys())
                self.languages.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in keys]))
        except:
            pass
        try:
            if 'languages_tags' in self.data and len(self.data['languages_tags']) > 0:
                self.languages.append(', '.join([x[3:] if x[:3] == 'en:' else x for x in self.data['languages_tags']]))
        except:
            pass

    def parse_product_data(self):
        self.parse_name()
        self.parse_language()
        self.parse_ingredients()
        self.parse_allergenes()
        self.set_explicit_none()

    def get_openfoodfacts_data(self):
        try:
            request_data = requests.get('https://world.openfoodfacts.org/api/v0/product/' + self.ean + '.json').json()
            if request_data['status'] == 1:
                self.request_data = request_data
                self.data = request_data['product']
            self.status = request_data['status']
            self.parse_product_data()
        except:
            self.status = -1

    def get_ingredients(self):
        for ingredient, language in zip(self.ingredients, self.ingredients_languages):
            if len(ingredient) > 0:
                res = ingredient
                if 'fr' not in language.lower():
                    res = self.translator.translate(res, dest="fr").text
                return res

    def get_allergens(self):
        for allergen in self.allergens:
            if len(allergen) > 0:
                return allergen

