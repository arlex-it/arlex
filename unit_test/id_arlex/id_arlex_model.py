import datetime
from bdd.db_connection import IdArlex


def get_id_arlex_model(param=None):
    id_arlex = {
        'patch_id': 'BLA-OKA-PAD'
    }
    if param:
        for key in param:
            if key in id_arlex:
                id_arlex[key] = param[key]
    return id_arlex

