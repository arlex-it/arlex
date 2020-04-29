from unit_test.user.user_model import user_model_to_sql


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

    def delete_all_user(self):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM user")

            
    def add_application_auth(self):
        with self.engine.connect() as con:
            con.execute("INSERT INTO `arlex_db`.`auth_application` "
                        "(`app_name`,`client_id`,`project_id`) "
                        "VALUES"
                        " ('google_assistant', '12151855473-vq1t07i4mg3m05jq7av9j6fh53e3eoc1.apps.googleusercontent.com', 'arlex-ccevqe');")


