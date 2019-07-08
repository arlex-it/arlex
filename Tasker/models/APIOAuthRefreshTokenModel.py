import arrow
import uuid
from bson import ObjectId
from mongoengine import StringField
from Tasker.models.AbstractModel import AbstractModel


class APIOAuthRefreshTokenModel(AbstractModel):
    meta = {'collection': 'APIOAuthRefreshToken'}
    id = StringField(primary_key=True)

    def create(self):
        self.id = str(ObjectId())
        self.enabled = True
        self.token = uuid.uuid4().hex[:35]
        self.createdAt = arrow.now().datetime
        self.updatedAt = arrow.now().datetime
        return self

    def is_valid(self):
        return True if self.get('enabled') else False