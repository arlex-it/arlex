from API.Utilities.Levenshtein import calc_similarity


class EanUtilities:
    def __init__(self):
        pass

    def search_product(self, product_list, asked):
        """
        search a product in a list of product by similarity and sort it by best result to worst
        """
        ean_list = []
        best = {'product_name': "", 'product_name_gen': "", 'id_ean': "", 'similarity': 0, 'id': 0}
        for product in product_list:
            # get similarity of product name
            name = product.product_name.lower().split(',')[0]
            similarity = calc_similarity(name, asked.lower())

            # get similarity of product by its description
            name = product.product_name_gen.lower().split(',')[0]
            similarity_gen = calc_similarity(name, asked.lower())

            # determine the best result
            similarity = similarity_gen if similarity_gen > similarity else similarity
            ean = {'product_name': product.product_name, 'product_name_gen': product.product_name_gen, 'id_ean': product.id_ean, 'similarity': similarity, 'id': product.id}

            if ean['similarity'] >= 0.40:
                ean_list.append({'product_name': product.product_name, 'product_name_gen': product.product_name_gen, 'id_ean': product.id_ean, 'similarity': similarity, 'id': product.id})
                if ean['similarity'] > best['similarity']:
                    best = ean
        # get potential result
        almost = []
        for ean in ean_list:
            if ean != best and ean['similarity'] >= best['similarity'] - best['similarity']/5:
                almost.append(ean)
        if best == {'product_name': "", 'product_name_gen': "", 'id_ean': "", 'similarity': 0, 'id': 0}:
            return ean_list
        ean_list = [best] + almost
        # sort from best result to worse
        ean_list.sort(key = lambda x: x['similarity'], reverse=True)
        ean_list = ean_list[:4]
        return ean_list