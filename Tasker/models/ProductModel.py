"""
Product modelization.
"""

from mongoengine import StringField

from Tasker.helpers.generic import load_config
from Tasker.models.AbstractModel import AbstractModel


class ProductModel(AbstractModel):
    """
    Product model.
    """

    meta = {'collection': 'product'}
    id = StringField(primary_key=True)

    def create(self, product_name, wardrobe, stage, expiration_date):
        super(ProductModel, self).create()

        self.product_name = product_name
        self.wardrobe = wardrobe
        self.stage = stage
        self.expiration_date = expiration_date
        return self
