#!/usr/bin/python3
""" """
import os
import unittest
from tests.test_models.test_base_model import test_basemodel
from models.city import City

STORAGE_TYPE = os.getenv('HBNB_TYPE_STORAGE')


class test_City(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "City"
        self.value = City

    @unittest.skipIf(STORAGE_TYPE == 'db', 'file storage test')
    def test_state_id(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.state_id), str)

    @unittest.skipIf(STORAGE_TYPE == 'db', 'file storage test')
    def test_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.name), str)
