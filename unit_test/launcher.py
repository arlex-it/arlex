import sqlalchemy as db
from pyngrok import ngrok
from user.tests import tests_post


class UnitTestInit():
    public_url = None
    engine = None
    user_route = tests_post.UserRoute()

    def connect_to_db(self):
        self.engine = db.create_engine('mysql+pymysql://unit_test:password@127.0.0.1/arlex_db', pool_recycle=3600, echo=False)

    def create_tunnel(self):
        self.public_url = ngrok.connect(5000)

    def call_user_tests(self):
        self.user_route.testPostRoute(public_url=self.public_url)


if __name__ == '__main__':
    init = UnitTestInit()
    init.connect_to_db()
    init.create_tunnel()
    init.call_user_tests()
