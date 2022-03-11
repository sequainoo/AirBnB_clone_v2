#!/usr/bin/python3
'''DBStorage engine.'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import base_model
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.base_model import Base

HBNB_ENV = os.getenv('HBNB_ENV')
HBNB_MYSQL_USER = os.getenv('HBNB_MYSQL_USER')
HBNB_MYSQL_HOST = os.getenv('HBNB_MYSQL_HOST')
HBNB_MYSQL_PWD = os.getenv('HBNB_MYSQL_PWD')
HBNB_MYSQL_DB = os.getenv('HBNB_MYSQL_DB')


class DBStorage:
    '''DBStorage.'''
    __engine = None
    __session = None

    __CLASSES = {
        # 'Amenity': Amenity,
        'City': City,
        'Place': Place,
        'Review': Review,
        'State': State,
        'User': User
    }

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
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''Gets all objects filtered depending on cls'''
        dictionary = {}
        results_list = []
        if cls:
            cls = DBStorage.__CLASSES[cls]
            query_result = self.__session.query(cls).all()
            results_list.append(query_result)
        else:
            for cls in DBStorage.__CLASSES.values():
                query_result = self.__session.query(cls).all()
                print(query_result)
                results_list.append(query_result)
        for query_result in results_list:
            for obj in query_result:
                dictionary.update({
                    obj.__class__.__name__ + '.' + obj.id: obj
                })
        return dictionary

    def new(self, obj):
        '''add the obj to the current session'''
        self.__session.add(obj)

    def save(self):
        '''Commits chaanges in the current database session'''
        self.__session.commit()

    def delete(self, obj=None):
        '''Deletes the obj from the current database session'''
        if obj:
            self.__session.delete(obj)
            self.save()

    def reload(self):
        ''' '''
        # create all tables in db
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(session_factory)
