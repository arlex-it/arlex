import sqlalchemy as db
from pyngrok import ngrok
from unit_test.user.tests import tests_post


class UnitTestInit():
    public_url = None
    engine = None

    def connect_to_db(self):
        self.engine = db.create_engine('mysql+pymysql://unit_test:password@127.0.0.1/arlex_db', pool_recycle=3600, echo=False)

    def create_tunnel(self):
        self.public_url = ngrok.connect(5000)

    def call_user_tests(self):
        user_route = tests_post.UserRoute(self.engine, self.public_url)
        user_route.testPostRoute()


if __name__ == '__main__':
    init = UnitTestInit()
    init.connect_to_db()
    init.create_tunnel()
    init.call_user_tests()
