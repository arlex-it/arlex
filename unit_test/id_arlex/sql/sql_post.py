

class PostSql:
    def __init__(self, engine=None, session=None):
        super().__init__()
        self.engine = engine
        self.session = session

    def delete_all_id_arlex(self):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM id_arlex")
