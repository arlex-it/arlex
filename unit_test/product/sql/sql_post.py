from unit_test.product.product_model import product_model_to_sql


class PostSql:
    def __init__(self, engine=None, session=None):
        super().__init__()
        self.engine = engine
        self.session = session

    def create_product(self, product):
        product = product_model_to_sql(product)
        self.session.add(product)
        self.session.commit()
        return product.id

    def get_product_by_id(self, id_product):
        with self.engine.connect() as con:
            rs = con.execute("SELECT * FROM product WHERE product.id = " + str(id_product))
            d, a = {}, []
            for rowproxy in rs:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}
                a.append(d)
            if d:
                return d
            else:
                return None

    def delete_product_by_id(self, id_product):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM product WHERE product.id = " + str(id_product))

    def delete_all_product(self):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM product")

