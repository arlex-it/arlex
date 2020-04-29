from unit_test.unit_test_template.route_name_model import model_to_sql

"""
/!\ DO NOT forget to rename functions and variables /!\ 
"""


class PostSql:
    def __init__(self, engine=None, session=None):
        super().__init__()
        self.engine = engine
        self.session = session

    def create(self, model):
        model_sql = model_to_sql(model)
        self.session.add(model_sql)
        self.session.commit()
        return model_sql.id

    def get_model_by_id(self, id_model_sql):
        with self.engine.connect() as con:
            rs = con.execute("SELECT * FROM product WHERE model_sql.id = " + str(id_model_sql))
            d, a = {}, []
            for rowproxy in rs:
                for column, value in rowproxy.items():
                    d = {**d, **{column: value}}
                a.append(d)
            if d:
                return d
            else:
                return None

    def delete_model_by_id(self, id_model_sql):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM product WHERE model_sql.id = " + str(id_model_sql))

    def delete_all(self):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM model_sql")

