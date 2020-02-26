from flask_restplus import abort

from API.Utilities.HttpResponse import HttpResponse


def get_test_vocal_assistant(request):
    if not request:
        abort(400)
    res = {
        'state': 'Hello, Tout les services arlex sont disponible !'
    }
    return HttpResponse(200).custom(res)
