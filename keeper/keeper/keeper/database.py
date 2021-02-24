import logging

from bson import json_util
from pymongo import MongoClient

import settings

module_logger = logging.getLogger('keeper')


class Database:
    """
    Connect with Mongo Database
    """
    _cluster = None

    def _connect(self):
        if not self._cluster:
            module_logger.debug('Database initialization.')
            self._cluster = MongoClient(settings.BD_STRING)[settings.BD_CLUSTER_NAME]
            module_logger.debug('Database connected.')
        return self._cluster

    @property
    def database(self):
        return self._connect()


class KeeperDB:
    def __init__(self):
        self._collection = None

    @property
    def collection(self):
        if not self._collection:
            self._collection = Database().database[settings.DB_COLLECTION_NAME]
            module_logger.debug(f'Collection {settings.DB_COLLECTION_NAME} connected.')
        return self._collection

    def save_data(self, data):
        self.collection.insert_one(data.copy())

    def get_data(self, keys_to_find):
        return json_util.dumps(list(self.collection.find(keys_to_find)))


