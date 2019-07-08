"""
Abstract controller.
"""
from Tasker.helpers.exceptions import ControllerError


class AbstractController(object):
    """
    Abstract controller class.
    """

    __attribute = None
    _model = None
    _object = None
    _entity_id = None
    _entity_type = None

    def load(self, id_):
        """
        Get a model by the id

        :param str id_: an object id
        :raises: ControllerError if modelId was not found
        :rtype: A Controller instance
        """
        if id_ is not None:
            _object = self._model.objects(id=id_).first()

            if not _object:
                raise ControllerError(f'Cannot find {self._model.__name__} #{id_}')
            self._object = _object

        return self

    def set_entity(self, entity):
        """
        Set the entity who initiate the controller
        :param obj entity: represents the user
        """
        if 'id' in entity and 'type' in entity:
            self._entity_id = entity['id']
            self._entity_type = entity['type']
