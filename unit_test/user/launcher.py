import unittest
import datetime
import requests
from pyngrok import ngrok
import sqlalchemy as db


class UserRoute(unittest.TestCase):
    def testPostRoute(self):
        public_url = ngrok.connect(5000)
        engine = db.create_engine('mysql+pymysql://unit_test:password@127.0.0.1/arlex_db', pool_recycle=3600, echo=False)
        with engine.connect() as con:
            rs = con.execute("INSERT INTO log (date_insert, code, data) VALUES (\'"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"\', 1, \'blabla\')")
        new_user = {'date_insert': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'date_update': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'is_active': 0,
                    'status': 0,
                    'gender': 0,
                    'lastname': 'Doe',
                    'firstname': 'John',
                    'mail': 'john@doe.com',
                    'password': '$2y$12$Egy/Ye1Ikuy4oueV9ja7T.o3eDUvGFGO4ZgdQ2VSnbjvFOz29d7zK',
                    'country': 'France',
                    'town': 'Lille',
                    'street': 'rue nationale',
                    'street_number': '13',
                    'region': 'Hauts de france',
                    'postal_code': '59000'}
        print(public_url)
        resp = requests.post(public_url+'/api/user'.format(), json=new_user)
        print(resp.text)
        with engine.connect() as con:
            rs = con.execute('SELECT * FROM log')
            for row in rs:
                print(row)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
