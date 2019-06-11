import os
import yaml
from copy import deepcopy

dir_path = os.path.dirname(os.path.realpath(__file__))

def load_config():
    """
    Read the config file (YAML).
    """
    with open(os.path.join(dir_path, '../config.yml')) as f:
        return yaml.safe_load(f)

def sub_key(dictionary, key, default=None):
    """
    Find a dotted key from a dict.
    It can search in lists too (key.2.subkey)

    :param dict dictionary: where to search
    :param str key: subkey identification (key.sub.subsubkey)
    :param object default: default returned value
    :returns: the value in the dictionary
    """
    suburb = deepcopy(dictionary)
    for k in key.split('.'):
        if isinstance(suburb, list) and k.isdigit() and int(k) < len(suburb):
            suburb = suburb[int(k)]
            continue

        if not isinstance(suburb, dict):
            return default

        suburb = suburb.get(k, None)
        if suburb is None:
            return default

    return suburb

def as_list(item):
    """
    Convert a string or a list to a list.

    :param item: str or list
    :returns: A list composed of str or the list
    :rtype: list
    """

    if item is None:
        return []
    elif isinstance(item, str):
        return [item]
    elif isinstance(item, list):
        return item

    raise ValueError('item should be a string or list')