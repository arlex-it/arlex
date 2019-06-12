"""
Collection of Flask converters.
"""
import importlib

from pymongo import ReadPreference
from werkzeug.routing import BaseConverter

from Tasker.helpers.exceptions import ConverterError, InvalidParameter


class AbstractConverter(BaseConverter):
    """
    Abstract model converter.
    """
    _model = 'Abstract'  # targeted model name
    _model_suffixe = 'Model'  # suffixe to model filename
    _secondary_preferred = True

    def __init__(self, *args, **kwargs):
        super(AbstractConverter, self).__init__(*args, **kwargs)
        class_name = '{}Model'.format(self._model)
        module_name = 'Tasker.models.{}{}'.format(self._model, self._model_suffixe)

        try:
            module_ = importlib.import_module(module_name)
        except (ImportError, ModuleNotFoundError) as exc:
            raise ConverterError('invalid module: {}'.format(exc))

        try:
            self.class_ = getattr(module_, class_name)
        except AttributeError as exc:
            raise ConverterError('invalid class: {}'.format(exc))

    def to_python(self, object_id):
        """
        Read object_id from url and load corresponding model.

        :param str object_id: a db object id
        :rtype: ObjectModel
        """
        object_ = self.class_.objects(id=object_id)

        if self._secondary_preferred:
            object_ = object_.read_preference(ReadPreference.SECONDARY_PREFERRED)

        object_ = object_.first()
        if object_ is None:
            raise InvalidParameter('wrong {} id'.format(self._model))

        return object_

    def to_url(self, object_):
        """
        Convert a object_ object to an url value.

        :param ObjectModel object_: the targeted object
        :rtype: str
        """
        return object_.id

class UserConverter(AbstractConverter):
    """
    User model converter.
    """
    _model = 'User'

class ProductConverter(AbstractConverter):
    """
    Product model converter.
    """
    _model = 'Product'
