from API.Utilities.Levenshtein import calc_similarity
from bdd.db_connection import session, Product


class EanUtilities:
    def __init__(self):
        pass

    def search_product(self, product_list, asked):
        ean_list = []
        best = {'product_name': "", 'product_name_gen': "", 'id_ean': "", 'similarity': 0, 'id': 0}
        for product in product_list:
            name = product.product_name.lower().split(',')[0]
            similarity = calc_similarity(name, asked.lower())

            name = product.product_name_gen.lower().split(',')[0]
            similarity_gen = calc_similarity(name, asked.lower())

            similarity = similarity_gen if similarity_gen > similarity else similarity
            ean = {'product_name': product.product_name, 'product_name_gen': product.product_name_gen, 'id_ean': product.id_ean, 'similarity': similarity, 'id': product.id}

            print(ean)
            if ean['similarity'] >= 0.25:
                ean_list.append({'product_name': product.product_name, 'product_name_gen': product.product_name_gen, 'id_ean': product.id_ean, 'similarity': similarity, 'id': product.id})
                if ean['similarity'] > best['similarity']:
                    best = ean
        # print("\n\n\nle plus gros est : ", best)
        almost = []
        for ean in ean_list:
            if ean != best and ean['similarity'] >= best['similarity'] - best['similarity']/5:
                almost.append(ean)
        # print("Il y a ", almost, "\nqui est peut etre bon egalement")
        if best == {'product_name': "", 'product_name_gen': "", 'id_ean': "", 'similarity': 0, 'id': 0}:
            return ean_list
        ean_list = [best] + almost
        # print("non sortedf: ", ean_list)
        ean_list.sort(key = lambda x: x['similarity'], reverse=True)
        # print("sorted :", ean_list)
        ean_list = ean_list[:4]
        print("sorted limited:", ean_list)
        return ean_list

#import sys
#if __name__ == '__main__':
#    list = session.query(Product).filter(Product.id_user == 1).all()
#    EanUtilities().search_product(list, sys.argv[1])
