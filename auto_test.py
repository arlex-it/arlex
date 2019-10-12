import automated_tests.api_connection.api_connection as api_connection
import automated_tests.getWeather.getweather_tests as get_weather


def launcher():
	print("Trying to connect to the API...")
	api_connection.connection_to_api()
	print("Connected to the API !")
	print(">>> TESTS BEGIN <<<")
	errors = 0
	errors += get_weather.get_weather_process()
	print(">>> TESTS END <<<")
	if errors != 0:
		exit(1)
	exit(0)


if __name__ == '__main__':
	launcher()
