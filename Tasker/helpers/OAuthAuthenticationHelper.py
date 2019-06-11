# coding: utf-8
"""
OAuth authentication helper.
"""
import arrow

from Tasker.helpers.exceptions import ModelError
from Tasker.models.APIOAuthTokenModel import APIOAuthTokenModel
from models.UserModel import UserModel
from Tasker.models.enum import OAuthEntityType


class OAuthAuthenticationTokenHelper(object):
    """
    Helper for OAuth authentification.
    """

    def __init__(self, token):
        """
        :param str token:
        """
        self.token = token
        print(self.token)
        self._model = APIOAuthTokenModel.objects(token=self.token).first()
        if self._model is None:
            raise ValueError(f'Cannot find token {self.token}')

    @property
    def entity(self):
        """
        Shortcut for entity.

        :rtype: dict
        """
        return self._model.entity

    def is_valid_token(self):
        """
        :rtype: bool
        """
        if self._model and self._model.is_valid():
            if hasattr(self._model, 'app_id'):
                # app_id = self._model.app_id

                # app = APIOAuthApplicationModel.objects(id=app_id).first()
                # print(app)
                # TODO Check app availability + enabled

                return True

        return False

    def has_entity(self):
        """
        Check if linked entity is valid.

        :rtype: bool
        """
        return (hasattr(self._model, 'entity')
                and self.entity
                and 'type' in self.entity
                and 'id' in self.entity)

    def get_entity(self):
        """
        :rtype: UserModel or None
        """
        if self.has_entity():
            if self.entity['type'] == OAuthEntityType.user:
                return UserModel.objects(id=self.entity['id']).first()

    def can_access_user(self, model):
        """:rtype: bool"""
        return model.is_admin() or self.entity['id'] == model.id

    def get_token_infos(self):
        if self._model and self._model.is_valid():
            return {
                'token': self._model.token,
                'expiration_date': arrow.get(self._model.expiresAt).isoformat()
            }

    def validate_models(self, kwargs):
        """
        Validate that url models are linked to the used token.

        :param dict kwargs: converted url arguments
        :rtype: bool
        """
        entity = self.get_entity()
        if entity is None:
            raise ModelError('Malformed entity for model validation')

        if entity.is_admin():
            return True

        for model in kwargs.values():
            if (isinstance(model, UserModel)
                    and not self.can_access_user(model)):
                return False

        return True

    def has_scopes(self, required_scopes=[]):
        """
        :rtype: bool
        """
        if not required_scopes or len(required_scopes) <= 0:
            return True

        for scope in required_scopes:
            if not self._model.has_scope(scope):
                return False

        return True
