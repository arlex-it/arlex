import requests

get_weather_url = "http://127.0.0.1:5000/api/getweather/"
get_weather_errors = 0


def get_weather_request(param):
	r = requests.post(get_weather_url, {}, param)
	print("param: ", param, "code: ", r.status_code)
	get_weather_check(r, param)


def get_weather_check(r, param):
	global get_weather_errors
	error_code = [500]
	if r.status_code in error_code:
		print("ERROR GET_WEATHER: param: ", param)
		get_weather_errors += 1


def get_weather_process():
	print("----- BEGIN GET_WEATHER -----")
	get_weather_request({"city": "London"})
	get_weather_request({"city": "dshqj"})
	get_weather_request({"city": "167"})
	get_weather_request({"city": "167ds:;d"})
	get_weather_request({"city": ""})
	get_weather_request({"city": 123})
	get_weather_request({"dkso": ""})
	print(get_weather_errors, "ERROR(S)")
	print("----- END GET_WEATHER -----")
	return get_weather_errors


def launcher():
	errors = 0
	errors += get_weather_process()
	if errors != 0:
		exit(1)


if __name__ == '__main__':
	launcher()

