#!/usr/bin/python3
'''DBStorage engine.'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import base_model, amenity, city, place, review, state, user

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
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
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
                results_list.append(query_result)
        for query_result in results_list:
            for obj in query_result:
                dictionary.update({
                    obj.__class__.__name__ + '.' + obj.id: obj
                })
        return dictionary
