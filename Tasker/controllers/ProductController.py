from Tasker.helpers.exceptions import ControllerError
from Tasker.models.ProductModel import ProductModel


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

    self.__user = ProductModel().create(
        firstname=firstname,
        lastname=lastname,
        phone=phone,
        email=email,
    )
    self.__user.update_password(password)
    self.__userId = self.__user.id

    if sponsor:
        sponsor_user = ProductModel.objects(profile__sponsorCode=sponsor).first()
        if sponsor_user:
            self.__user.set_sponsor(sponsor_code=sponsor, sponsor_user_id=sponsor_user.id)
        else:
            raise ControllerError('Sponsor code is invalid.')

    self.__user.save()

    return self.__user