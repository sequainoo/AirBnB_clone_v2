#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import os

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')

if STORAGE_TYPE == 'db':
    place_amenity = Table(
        'place_amenity',
        Base.metadata,
        Column(
            'place_id',
            String(60),
            ForeignKey('places.id'),
            primary_key=True,
            nullable=False
        ),
        Column(
            'amenity_id',
            String(60),
            ForeignKey('amenities.id'),
            primary_key=True,
            nullable=False
        )
    )


class Place(BaseModel, Base):
    """ A place to stay """
    if STORAGE_TYPE == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        user = relationship('User', back_populates='places')
        name = Column(String(128), nullable=False)
        description = Column(String(1024))
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float)
        longitude = Column(Float)
        city = relationship('City', back_populates='places')
        reviews = relationship(
            'Review',
            cascade='all, delete, delete-orphan',
            back_populates='place'
        )
        amenities = relationship(
            'Amenity',
            secondary=place_amenity,
            viewonly=False,
            back_populates='place_amenities'
        )
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            '''Gets all related reviews for the place'''
            from models.review import Review
            from models import storage

            reviews = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    reviews.append(review)
            return reviews

        @property
        def amenities(self):
            '''Gets all related amenities for the place'''
            from models.amenity import Amenity
            from models import storage

            amenities = []
            for amenity in storage.all(Amenity).values():
                if amenity.id in self.amenity_ids:
                    amenities.append(amenity)
            return amenities

        @amenities.setter
        def amenities(self, amenity):
            '''Sets amenity id for the place'''
            from models.amenity import Amenity

            if type(amenity) is Amenity:
                self.amenity_ids.append[amenity.id]
