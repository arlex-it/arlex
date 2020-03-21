from copy import deepcopy


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