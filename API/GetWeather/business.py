from flask import jsonify
from flask_restplus import abort
import requests
import json


def get_weather(request):
    if not request or request.json.get('city') is None:
        abort(400)
    city = request.json.get('city')
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+city+'&APPID=c14ca5995bc9dbb8ef3f7b0abbb3be6e&units=metric')
    res = json.loads(r.text)
    if int(res["cod"]) == 200:
        j = {
            'main_weather': res['weather'][0]['main'],
            'description': res['weather'][0]['description'],
            'temperature': res['main']['temp']
        }
        return jsonify(j)
    else:
        abort(int(res["cod"]))
