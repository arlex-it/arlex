from bdd.db_connection import session, Product


class EanUtilities:
    def __init__(self):
        pass

    def calc_similarity(self, name, asked):
        # todo Simon mets ton calcul de similarité ici :) bisou <3 j'en ai utilisé un temporaiement
        # todo Simon mets ton calcul de similarité ici :) bisou <3 j'en ai utilisé un temporaiement
        # todo Simon mets ton calcul de similarité ici :) bisou <3 j'en ai utilisé un temporaiement
        # todo Simon mets ton calcul de similarité ici :) bisou <3 j'en ai utilisé un temporaiement
        # todo Simon mets ton calcul de similarité ici :) bisou <3 j'en ai utilisé un temporaiement

        from difflib import SequenceMatcher
        return SequenceMatcher(None, name, asked).ratio()

    def search_product(self, product_list, asked):
        ean_list = []
        for product in product_list:
            similarity = self.calc_similarity(product.product_name, asked)
            ean_list.append([product.product_name, product.id_ean, similarity])
        best = ean_list[0]
        for ean in ean_list:
            if ean[2] > best[2]:
                best = ean
            print(ean)
        almost = []
        for ean in ean_list:
            if ean != best and ean[2] >= best[2] - best[2] / 10:
                almost.append(ean)
        print("le plus gros est : ", best)
        print("Il y a ", almost, "\nqui est peut etre bon egalement")
        return best

if __name__ == '__main__':
    list = session.query(Product).filter(Product.id_user == 1).all()
    EanUtilities().search_product(list, "chocol")