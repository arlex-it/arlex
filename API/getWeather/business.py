from flask import jsonify
from flask_restplus import abort
import requests
import json


def get_weather(request):
    if not request:
        abort(400)
    r = requests.get('http://api.openweathermap.org/data/2.5/weather?q='+request.json.get('city')+'&APPID=c14ca5995bc9dbb8ef3f7b0abbb3be6e&units=metric')
    res = json.loads(r.text)
    print(res["cod"])
    if int(res["cod"]) == 404:
        abort(404, "Can't find the city")
        return
    j = {
        'main_weather': res['weather'][0]['main'],
        'description': res['weather'][0]['description'],
        'temperature': res['main']['temp']
    }
    return jsonify(j)
