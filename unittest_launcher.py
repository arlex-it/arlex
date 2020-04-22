import sqlalchemy as db
from pyngrok import ngrok
from unit_test.product.tests import tests_post as tests_post_product
import main
from Ressources import settings
import _thread
from bdd.db_connection import engine as db_engine
import time, signal


class UnitTestInit():
    public_url = None
    engine = None

    def connect_to_db(self):
        self.engine = db_engine
        # self.engine = db.create_engine('mysql+pymysql://unit_test:password@127.0.0.1/arlex_db', pool_recycle=3600, echo=False)

    def create_tunnel(self):
        self.public_url = ngrok.connect(5000)

    def call_product_tests(self):
        product_route = tests_post_product.ProductRoute(self.engine, self.public_url)
        # product_route.testPostRoute()
        product_route.testGetRoute()

    def close_db(self):
        self.engine.dispose()
        print("engine close")


def launch_api():
    print("~~~~~~ Laucnh test ~~~~~")
    # time.sleep(2)
    init = UnitTestInit()
    init.connect_to_db()
    init.create_tunnel()
    init.call_product_tests()
    init.close_db()


if __name__ == '__main__':
    _thread.start_new_thread(launch_api, ())
    main.app.run(port=5000, host='0.0.0.0')
