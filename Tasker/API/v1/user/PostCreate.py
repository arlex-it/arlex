from flask import g
from flask_expects_json import expects_json


from Tasker.API.core.HTTPReponse import HTTPResponse
from Tasker.API.v1 import AbstractView

from Tasker.controllers.UserController import UserController
from flask import current_app
from flask_assistant import Assistant, ask, tell

SCHEMA = {
    'type': 'object',
    'properties': {
        'firstname': {'type': 'string'},
        'lastname': {'type': 'string'},
        'email': {'type': 'string'},
        'password': {'type': 'string'},
        'phone': {'type': 'string'}
    },
    'required': ['firstname', 'lastname', 'email', 'password', 'phone']
}

class APIV1UserPostCreate(AbstractView):
    """
    API to create a new user.
    """
    #@require_authentication('private')
    def __init__(self):
        self.user_ctrlr = UserController()

    @expects_json(SCHEMA)
    def dispatch_request(self, **kwargs):
        user = self.user_ctrlr.create(
            firstname=g.data['firstname'],
            lastname=g.data['lastname'],
            phone=g.data['phone'],
            email=g.data['email'],
            password=g.data['password'],
        )

        response = HTTPResponse(200).set_content(user.id)
        return response.get_response()