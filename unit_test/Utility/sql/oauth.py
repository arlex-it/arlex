import datetime
import uuid

import arrow


class UtilityOauthSQL:
    def __init__(self, engine=None, session=None):
        super().__init__()
        self.engine = engine
        self.session = session

    def get_token_template(self):
        return {'token': uuid.uuid4().hex[:35],
                 'id_user': 0,
                 'expiration_date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                 'app_id': 1,
                 'type': 'bearer',
                 'is_enable': 1,
                 'scopes': 'user'
                 }

    def create_access_token(self, token_data):
        with self.engine.connect() as con:
            con.execute("INSERT INTO `arlex_db`.`access_token` "
                        "(`token`,`id_user`,`expiration_date`, `app_id`, `type`, `is_enable`, `scopes`) "
                        "VALUES"
                        " ('{}', '{}', '{}','{}', '{}', '{}', '{}');"
                        .format(token_data['token'], token_data['id_user'], token_data['expiration_date'],
                                token_data['app_id'], token_data['type'], token_data['is_enable'], token_data['scopes']))

    def create_default_access_token(self, id_user):
        token = self.get_token_template()
        token['id_user'] = id_user
        self.create_access_token(token_data=token)
        return token

    def delete_default_access_token(self, id_user):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM access_token WHERE id_user = " + str(id_user))
