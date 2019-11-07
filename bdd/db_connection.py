#!env/bin/python

import mysql.connector
from mysql.connector import errorcode
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


def to_dict(model_instance, query_instance=None):
    if hasattr(model_instance, '__table__'):
        return {c.name: str(getattr(model_instance, c.name)) for c in model_instance.__table__.columns}
    else:
        cols = query_instance.column_descriptions
        return {cols[i]['name']: model_instance[i]  for i in range(len(cols)) }


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, unique=True)
    date_insert = Column(DateTime, nullable=False)
    date_update = Column(DateTime, nullable=False)
    is_active = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    gender = Column(Integer, nullable=False)
    lastname = Column(String(45), nullable=False)
    firstname = Column(String(45), nullable=False)
    mail = Column(String(45), nullable=False)
    password = Column(String(45), nullable=False)
    country = Column(String(45), nullable=False)
    town = Column(String(45), nullable=False)
    street = Column(String(255), nullable=False)
    street_number = Column(String(45), nullable=False)
    region = Column(String(45), nullable=False)
    postal_code = Column(String(45), nullable=False)




engine = db.create_engine('mysql+pymysql://corentin_local:corentinlocal@127.0.0.1/Arlex', pool_recycle=3600, echo=True)
#engine.echo = True
#metadata = db.MetaData(engine)
#game = db.Table('user', metadata)

Session = sessionmaker(bind=engine)
session = Session()
try:
    session.query("1").from_statement("SELECT 1").all()
    print("\033[92mConnected to the Database !\033[0m")
except:
    print("\033[91mError with Database!\033[0m")
    exit(1)

""",
                Column('id', Integer, primary_key=True),
                Column('trait_p', Integer),
                Column('trait_e', Integer),
                Column('trait_t', Integer),
                Column('sante_p', Integer),
                Column('sante_e', Integer),
                Column('sante_t', Integer),
                Column('mdv', Integer),
                """


"""try:
    conn = mysql.connector.connect(host="127.0.0.1", user="corentin_local", password="corentinlocal",
                                   database="Arlex")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    cursor = conn.cursor(dictionary=True)
    print("\033[92mConnected to the Database !\033[0m")
"""

#cursor.execute("""SELECT * FROM user;""")
#rows = cursor.fetchall()
#for row in cursor:
#    print(row['id'], row['lastname'], row['mail'])
#conn.close()
