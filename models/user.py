#!/usr/bin/python3
"""This module defines a class User"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class User(BaseModel, Base):
    """This class defines a user by various attributes"""
    if STORAGE_TYPE == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        places = relationship(
            'Place',
            back_populates='user',
            cascade='all, delete, delete-orphan'
        )
        reviews = relationship(
            'Review',
            cascade='all, delete, delete-orphan',
            back_populates='user'
        )
    else:
        email = ''
        password = ''
        first_name = ''
        last_name = ''
