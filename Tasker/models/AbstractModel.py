"""
Abstract model.
"""
import arrow
from bson import ObjectId
from mongoengine import DynamicDocument

from Tasker.helpers.generic import sub_key

class AbstractModel(DynamicDocument):
    """
    Abstract model class.
    """
    meta = {
        'abstract': True
    }
    id = None

    def create(self):
        """
        Do initialization on model.

        :returns: an instance of the model
        """
        self.id = self.gen_id()
        self.createdAt = arrow.now().datetime

        return self

    @staticmethod
    def gen_id():
        """Generate a unique id."""
        return str(ObjectId())

    def get(self, value, default=None):
        """
        Retrieve a nested value through attributes
        :param value:
        :rtype: * or None
        """

        values = value.split(".")

        # Unknown attribute
        if not hasattr(self, values[0]):
            return default

        attribute = getattr(self, values[0])
        # Single attribute
        if len(values) == 1:
            return attribute

        # Pointed sub attribute
        return sub_key(
            dictionary=attribute,
            key='.'.join(values[1:]),
            default=default
        )