# coding: utf-8

from Tasker.controllers.AbstractController import AbstractController
from Tasker.helpers.exceptions import ControllerError
from Tasker.helpers.generic import load_config
from Tasker.models.UserModel import UserModel

config = load_config()

SCHEMA_NOTIFICATION_DAY = {
    "type": "object",
    "properties": {
        "status_afternoon": {"type": "boolean"},
        "status_morning": {"type": "boolean"},
        "nb_day": {"type": "integer"}
    },
    "required": ["status_afternoon", "status_morning", "nb_day"]
}


class UserController(AbstractController):
    """
    User controller class.
    """

    __userId = None
    __user = None

    def create(self, firstname, lastname, phone, email, password,
            sponsor=None):
        """
        Create a new User.

        :param str firstname: user first name
        :param str lastname: user last name
        :param str phone: user phone number
        :param str email: user email
        :param str password: user password
        :param str source: ?
        :param dict source_extra: ?
        :param str sponsor: Sponsor code used by the user
        :returns: a new User (saved) instance
        :rtype: UserModel
        """

        self.__user = UserModel().create(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            email=email,
        )
        self.__user.update_password(password)
        self.__userId = self.__user.id

        if sponsor:
            sponsor_user = UserModel.objects(profile__sponsorCode=sponsor).first()
            if sponsor_user:
               self.__user.set_sponsor(sponsor_code=sponsor, sponsor_user_id=sponsor_user.id)
            else:
                raise ControllerError('Sponsor code is invalid.')

        self.__user.save()

        return self.__user