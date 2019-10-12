from flask import request
from flask_restplus import Resource
from Ressources.swagger_api import api
from API.getWeather.business import get_weather
from API.getWeather.models import getweather_input

ns = api.namespace('getweather', description='get the weather')


@ns.route('/')
class GetWeatherCollection(Resource):
    @ns.expect(getweather_input)
    @ns.response(200, '{"main_weather": Clouds, "description": "scattered clouds", "temperature": 11.31}')
    def post(self):
        """
        This is a test route
        """
        return get_weather(request)
