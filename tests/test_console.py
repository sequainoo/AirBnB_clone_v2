#!/usr/bin/python3
'''Tests for HBNBConsole.'''

import os
import sys
import unittest
from console import HBNBCommand
from contextlib import contextmanager
from io import StringIO
from models import storage

HBNB_TYPE_STORAGE = os.environ.get('HBNB_TYPE_STORAGE')


@contextmanager
def redirect_streams():
    '''Redirects stdout and stderr streams'''
    output_stream, error_stream = StringIO(), StringIO()
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = output_stream, error_stream
    try:
        yield output_stream, error_stream
    finally:
        sys.stdout, sys.stderr = stdout, stderr


def empty_dictionary(dictionary):
    '''removes every key/value from dictionary.'''
    keys = [key for key in dictionary.keys()]
    for key in keys:
        del dictionary[key]


@unittest.skipIf(HBNB_TYPE_STORAGE == 'db', 'storage is not file')
class TestHBNBCommandCreate(unittest.TestCase):
    '''Tests console create <class> <key1=value1> <key2=value2> ...'''
    @classmethod
    def setUpClass(cls):
        cls.console = HBNBCommand()

    def setUp(self):
        self.console = TestHBNBCommandCreate.console

    def tearDown(self):
        if os.path.exists('file.json'):
            os.remove('file.json')
        empty_dictionary(storage.all())

    def test_create_save_to_storage(self):
        '''Test that storage gets updated.'''
        prev_len = len(storage.all())
        self.console.do_create('State name="Arizona"')
        new_len = len(storage.all())
        self.assertTrue(new_len + prev_len == new_len)
        self.assertEqual(new_len, 1)

    def test_create_save_to_file(self):
        '''Tests that is persisted to file.'''
        exists = os.path.exists('file.json')
        self.console.do_create('State name="California"')
        new_exists = os.path.exists('file.json')
        self.assertFalse(exists == new_exists)

    def test_create_prints_id(self):
        '''Test id is printed to console'''
        with redirect_streams() as (output_stream, error_stream):
            obj_id = ""
            self.console.do_create('State name="California"')
            for obj in storage.all().values():
                obj_id = obj.id
            printed_id = output_stream.getvalue()
            printed_id = printed_id.strip('\n')
            self.assertTrue(printed_id == obj_id)

    def test_create_no_parameter(self):
        '''Test create with no parameter just class.'''
        pass

    def test_create_bad_parameter_key(self):
        '''Test create on param key thats not an attribute.
        Expected to skip param but create obj.
        '''
        self.console.do_create('State nmae="California"')
        obj = None
        for v in storage.all().values():
            obj = v
        self.assertEqual(obj.name, '')

    def test_create_bad_parameter_value_empty(self):
        '''Test for empty value.
        Expected to ignore setting attribute.
        '''
        obj = None
        self.console.do_create('State name=""')
        for v in storage.all().values():
            obj = v
        self.assertEqual(obj.name, '')

    def test_create_bad_parameter_value_wrong_type(self):
        '''Test mismatch key and value.
        That when wrong type of value is assigned to attribute
        it is not set.'''
        place = None
        self.console.do_create('Place '
                               'city_id="0001" '
                               'name=My_little_house '
                               'number_rooms="4" '
                               'number_bathrooms=2 '
                               'max_guest=10 '
                               'price_by_night=300 '
                               'latitude=37773972 '
                               'longitude=-122.431297')
        for v in storage.all().values():
            place = v
        self.assertEqual(place.name, '')
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.city_id, '0001')
        self.assertEqual(place.number_bathrooms, 2)
        self.assertEqual(place.max_guest, 10)
        self.assertEqual(place.price_by_night, 300)
        self.assertEqual(place.longitude, -122.431297)
