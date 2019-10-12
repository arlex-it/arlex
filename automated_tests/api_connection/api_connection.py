import requests


def try_connection_to_api():
	try:
		r = requests.get('http://127.0.0.1:5000/api/')
		return r.status_code
	except:
		return 0


def connection_to_api():
	status_code = try_connection_to_api()
	while int(status_code) != 200:
		status_code = try_connection_to_api()
	return 0
