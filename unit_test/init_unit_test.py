import sqlalchemy as db
from sqlalchemy.orm import sessionmaker


class UnitTestInit():
    public_url = None
    engine = None
    session = None

    def connect_to_db(self):
        self.engine = db.create_engine('mysql+pymysql://unit_test:password@127.0.0.1/arlex_db', pool_recycle=3600, echo=False)
        session_maker = sessionmaker(bind=self.engine)
        self.session = session_maker()
        try:
            self.session.query("1").all()
        except Exception as e:
            print("\033[91mError with Database!\033[0m\n", e.args)
            exit(1)
        return self.engine, self.session

    def create_tunnel(self):
        self.public_url = ngrok.connect(5000)
        return self.public_url

