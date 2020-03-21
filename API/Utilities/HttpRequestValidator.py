# coding: utf-8
"""
Validator for HTTP requests
"""
from API.Utilities.HttpRequest import HttpRequest

PARAM_NOT_PRESENT='arlex_param_not_present'

class Location(object):
    """Available locations for validator"""
    any = 'any'
    query = 'query'
    form = 'form'
    json = 'json'
    file = 'file'

    @property
    def default(self):
        """Default Location"""
        return self.any

class ValidatorParameter(object):
    """
    A Validator parameter : target a parameter name in a specific location.
    """

    def __init__(self, name, required=True, rules=[], location=Location.any):
        self.name = name
        self.required = required
        self.rules = rules
        if not hasattr(Location, str(location)):
            location = Location.any
        self.location = str(location)


class HttpRequestValidator(object):
    """
    HttpRequestValidator class.
    """
    __params = []
    __request = None
    __throw_on_error = False

    def __init__(self):
        self.__params = []
        self.__request = HttpRequest()
        self.__throw_on_error = False

    def throw_on_error(self, enabled=True):
        """
        Set/unset mode where an error is produced on any validation fail.

        :param bool enabled: activate or desactivate the feature
        """
        self.__throw_on_error = enabled

    def __verify_one_param(self, param):
        """
        Validate a specific rule.

        :param ValidatorParameter param: a parameter validation configuration
        :rtype: bool
        """
        value = PARAM_NOT_PRESENT

        if param.location == Location.any:
            value = self.__request.get_param(name=param.name, default=PARAM_NOT_PRESENT)
        elif param.location == Location.query:
            value = self.__request.get_query_param(name=param.name, default=PARAM_NOT_PRESENT)
        elif param.location == Location.form:
            value = self.__request.get_form_param(name=param.name, default=PARAM_NOT_PRESENT)
        elif param.location == Location.json:
            value = self.__request.get_json_param(name=param.name, default=PARAM_NOT_PRESENT)
        elif param.location == Location.file:
            value = self.__request.get_file_param(name=param.name, default=PARAM_NOT_PRESENT)

        if param.required:
            if value == PARAM_NOT_PRESENT:
                return False

        # TODO : We should check the rules here.

        return True

    def __verify(self):
        """
        Verify all declared rules.

        :returns: the failling parameter name or an empty string
        :rtype: str
        """
        for param in self.__params:
            if not self.__verify_one_param(param):
                return param.name

        return ''

    def __throw_error(self, target=''):
        """
        Raise an error.

        :param str target: name of the failing parameter
        :raises: InvalidParameter
        """
        raise Exception(
            'Invalid parameters {}. Please refer to this method documentation.'
            )

    def verify(self):
        """
        Try to execute all validation rules on current request.

        :raises: InvalidParameter if activated
        :rtype: bool
        """
        param_name = self.__verify()

        if param_name == '':
            return True

        if self.__throw_on_error:
            self.__throw_error(target=param_name)

        return False

    def add_param(self, name, required=True, rules=[], location=Location.any):
        """
        Add a verification on parameter.

        :param str name: name of the parameter
        :param bool required: does the parameter is required ?
        :param list rules: ! unimplemented !
        :param str location: where does the parameter should be present ? (any, query, form or json)
        """
        self.__params.append(
            ValidatorParameter(
                name=name,
                required=required,
                rules=rules,
                location=location
            )
        )