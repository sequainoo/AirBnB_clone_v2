#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
import os

STORAGE_TYPE = os.environ.get('HBNB_TYPE_STORAGE')
if STORAGE_TYPE == 'db':
    from models.engine.db_storage import DBStorage as Storage
else:
    from models.engine.file_storage import FileStorage as Storage

storage = Storage()
storage.reload()
