"""
Collection of Flask converters.
"""
import importlib

from werkzeug.routing import BaseConverter

from Tasker.helpers.exceptions import ConverterError


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
        module_name = 'models.{}{}'.format(self._model, self._model_suffixe)

        try:
            module_ = importlib.import_module(module_name)
        except (ImportError, ModuleNotFoundError) as exc:
            raise ConverterError('invalid module: {}'.format(exc))

        try:
            self.class_ = getattr(module_, class_name)
        except AttributeError as exc:
            raise ConverterError('invalid class: {}'.format(exc))

class UserConverter(AbstractConverter):
    """
    User model converter.
    """
    _model = 'User'
