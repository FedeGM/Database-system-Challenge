from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from database_connection import SQLconnection as SQL
from config import config_data

azure_db = SQL(server= config_data['SERVER'],
                database= config_data['DATABASE'],
                user= config_data['DB_USERNAME'],
                password= config_data['DB_PASSWORD'],
                port= config_data['PORT'])

engine = create_engine(azure_db.conn_str, echo= True)
db = scoped_session(sessionmaker(autocommit = False,
                                 autoflush = False,
                                 bind = engine))

Base = declarative_base()
Base.query = db.query_property()

