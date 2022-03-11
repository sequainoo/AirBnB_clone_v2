#!/usr/bin/python3
""" Review module for the HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import os

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class Review(BaseModel, Base):
    """ Review class to store review information """
    if STORAGE_TYPE == 'db':
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(
            String(60),
            ForeignKey('places.id'),
            nullable=False
        )
        place = relationship('Place', back_populates='reviews')
        user_id = Column(
            String(60),
            ForeignKey('users.id'),
            nullable=False
        )
        user = relationship('User', back_populates='reviews')
    else:
        place_id = ""
        user_id = ""
        text = ""
