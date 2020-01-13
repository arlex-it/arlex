import datetime


def get_product_model(param=None):
    product = {
        "expiration_date": "2019-11-30 00:00:00",
        "id_rfid": 123,
        "id_ean": "3017620424403",
        "position": "placard sous evier"
    }
    if param:
        for key in param:
            if key in product:
                product[key] = param[key]
    return product
