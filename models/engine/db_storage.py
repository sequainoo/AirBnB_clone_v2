#!/usr/bin/python3
'''DBStorage engine.'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

HBNB_ENV = os.getenv('HBNB_ENV')
HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')


class DBStorage:
    '''DBStorage.'''
    __engine = None
    __session = None

    def __init__(self):
        ''' '''
        conn_str = 'mysql+mysqldb://{}:{}@{}/{}'.format(
            HBNB_MYSQL_USER,
            HBNB_MYSQL_PWD,
            HBNB_MYSQL_HOST,
            HBNB_MYSQL_DB
        )
        self.__engine = create_engine(conn_str, pool_pre_ping=True)
        if HBNB_ENV == 'test':
            DBStorage.drop_all_tables()

    def all(self, cls=None):
        '''Gets all objects filtered depending on cls'''
        if cls:
            dictionary = {}


    @staticmethod
    def drop_all_tables():
        ''' Drops all tables if it is a test env'''
        from MySQLdb import connect
        conn = connect(
            user=HBNB_MYSQL_USER,
            passwd=HBNB_MYSQL_PWD,
            host=HBNB_MYSQL_HOST,
            port=3306,
            db=HBNB_MYSQL_DB
        )
        cursor = conn.cursor()
        cursor.execute(
            'DROP DATABASE IF EXISTS %s; CREATE DATABASE IF NOT EXISTS %s;',
            (HBNB_MYSQL_DB, HBNB_MYSQL_DB)
        )
        cursor.execute('COMMIT;')
        cursor.close()
        conn.close()
