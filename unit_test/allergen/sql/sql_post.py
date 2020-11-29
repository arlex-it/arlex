from unit_test.allergen.allergen_model import *


class PostSql:
    def __init__(self, engine=None, session=None):
        super().__init__()
        self.engine = engine
        self.session = session

    def create_user(self, user):
        user = user_model_to_sql(user)
        self.session.add(user)
        self.session.commit()
        return user.id

    def get_user_by_id(self, id_user):
        with self.engine.connect() as con:
            rs = con.execute("SELECT * FROM user WHERE user.id = " + str(id_user))

    def delete_user_by_id(self, id_user):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM user WHERE user.id = " + str(id_user))

    def create_product(self, product):
        product = product_model_to_sql(product)
        self.session.add(product)
        self.session.commit()
        return product.id

    def delete_product_by_id(self, id_product):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM product WHERE product.id = " + str(id_product))