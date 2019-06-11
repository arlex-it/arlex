from enum import Enum

"""
Collection of usefull enumarations.
"""


class AbstractEnum(object):

    @classmethod
    def has_member(cls, name):
        """
        :rtype: bool
        """
        return hasattr(cls, name)

class OAuthEntityType(AbstractEnum):
    """
    Distinct OAuth entiyy types
    """
    user = 'user'
