from bdd.db_connection import session, Product
from difflib import SequenceMatcher


class EanUtilities:
    def __init__(self):
        pass

    def calc_similarity(self, name, asked):
        name = name.split(',')[0]
        return SequenceMatcher(None, name, asked).ratio()

    def search_product(self, product_list, asked):
        ean_list = []
        for product in product_list:
            similarity = self.calc_similarity(product.product_name.lower(), asked.lower())
            similarity_gen = self.calc_similarity(product.product_name_gen.lower(), asked.lower())
            similarity = similarity_gen if similarity_gen > similarity else similarity
            ean_list.append([product.product_name, product.product_name_gen, product.id_ean, similarity])
        best = ean_list[0]
        for ean in ean_list:
            if ean[3] > best[3]:
                best = ean
            print(ean)
        # print("\n\n\nle plus gros est : ", best)
        almost = []
        for ean in ean_list:
            if ean != best and ean[3] >= 0.25 and ean[3] >= best[3] - best[3]/5:
                almost.append(ean)
        # print("Il y a ", almost, "\nqui est peut etre bon egalement")
        ean_list = [best] + almost
        # print("non sortedf: ", ean_list)
        ean_list.sort(key = lambda x: x[3], reverse=True)
        # print("sorted :", ean_list)
        ean_list = ean_list[:4]
        print("sorted limited:", ean_list)
        return ean_list

import sys
if __name__ == '__main__':
    list = session.query(Product).filter(Product.id_user == 1).all()
    EanUtilities().search_product(list, sys.argv[1])
