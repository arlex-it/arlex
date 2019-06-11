"""
AuthToken model.
"""

import uuid
import arrow
from bson import ObjectId
from mongoengine import StringField

from Tasker.models.AbstractModel import AbstractModel
from Tasker.helpers.exceptions import ModelError

ENTITY_TYPES = ['user', 'pro']

class APIOAuthTokenModel(AbstractModel):
    meta = {'collection': 'APIOAuthToken'}
    id = StringField(primary_key=True)

    def create(self, app_id, entity=None, enabled=True, scope=None, type_='bearer', token=None):
        """
        :param dict entity:
        :param list scope:
        """
        self.id = str(ObjectId())
        self.app_id = app_id
        self.enabled = enabled
        self.token = token or uuid.uuid4().hex[:35]
        if entity is not None and not isinstance(entity, dict):
            raise ModelError(f'Unknown entity format: {entity}')
        self.entity = entity
        if not isinstance(scope, list):
            scope = []
        self.scope = scope
        self.type_ = type_
        self.expiresAt = arrow.now().shift(hours=+10).datetime
        self.createdAt = arrow.now().datetime
        self.updatedAt = arrow.now().datetime

        return self

    def is_expired(self):
        """
        :rtype: bool
        """
        if hasattr(self, 'expiresAt') and self.expiresAt:
            now = arrow.now()
            expiration = arrow.get(self.expiresAt)

            if now < expiration:
                return False

        return True

    def is_valid(self):
        """
        :rtype: bool
        """
        if hasattr(self, 'enabled') and self.enabled and not self.is_expired():
            return True

        return False