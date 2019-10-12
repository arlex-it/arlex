import requests
import json

get_weather_url = "http://127.0.0.1:5000/api/getweather/"


def get_weather_request(param):
	r = requests.post(get_weather_url, {}, param)
	get_weather_check(r)


def get_weather_check(r):
	status_code = [200, 404]
	if r.status_code not in status_code:
		exit(1)


def get_weather_process():
	get_weather_request({"city": "London"})
	get_weather_request({"city": "dshqj"})
	get_weather_request({"city": "167"})
	get_weather_request({"city": "167ds:;d"})
	get_weather_request({})


if __name__ == '__main__':
	get_weather_process()
