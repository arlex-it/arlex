from unit_test.sensor.sensor_model import *


class PutSql:
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

    def create_sensor(self, sensor):
        sensor = sensor_model_to_sql(sensor)
        self.session.add(sensor)
        self.session.commit()
        return sensor.id

    def delete_sensor_by_id(self, id_sensor):
        with self.engine.connect() as con:
            rs = con.execute("DELETE FROM sensor WHERE sensor.id = " + str(id_sensor))
