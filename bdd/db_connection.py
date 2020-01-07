#!env/bin/python

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
        return {cols[i]['name']: model_instance[i]  for i in range(len(cols))}


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


engine = db.create_engine('mysql+pymysql://root:blind@x2021arlex2995326557000.northeurope.cloudapp.azure.com/arlex_db', pool_recycle=3600, echo=False)

Session = sessionmaker(bind=engine)
session = Session()
try:
    session.query("1").all()
    print("\033[92mConnected to the Database !\033[0m")
except Exception as e:
    print("\033[91mError with Database!\033[0m\n", e.args)
    exit(1)
