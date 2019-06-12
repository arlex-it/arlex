"""
Product modelization.
"""

import hashlib
import arrow
from arrow.parser import ParserError
from dateutil.relativedelta import relativedelta
from mongoengine import StringField

from Tasker.helpers.PasswordHelper import PasswordHelper
from Tasker.helpers.exceptions import ModelError
from Tasker.helpers.generic import load_config
from Tasker.models.AbstractModel import AbstractModel

config = load_config()

DEFAULT_KMS_NUMBER = 25

class ProductModel(AbstractModel):
    """
    Product model.
    """

    meta = {'collection': 'product'}
    id = StringField(primary_key=True)
