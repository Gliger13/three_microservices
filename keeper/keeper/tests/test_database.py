import json
import random

import pymongo
import pytest

import settings


@pytest.fixture(params=[
    {
        "test_data1": "data1",
        "test_data2": "data2",
        "test_data3": "data3",
    }
])
def test_data_to_save(request):
    return request.param


class TestKeeperDB:
    @pytest.mark.dependency
    def test_db_connection(self):
        is_ok_connection = False
        try:
            pymongo.MongoClient(settings.BD_STRING).server_info()
            is_ok_connection = True
        except pymongo.errors.ServerSelectionTimeoutError:
            pass
        assert is_ok_connection, "Database connection error, should be no connection problems"

    @pytest.mark.dependency(depends=["TestKeeperDB::test_db_connection"])
    def test_save_data(self, keeper_db, test_data_to_save):
        keeper_db.save_data(test_data_to_save)

        random_key, random_value = random.choice(list(test_data_to_save.items()))
        find_result = keeper_db.collection.find_one({random_key: random_value})
        find_result.pop('_id')

        assert find_result == test_data_to_save, "Saved and test data does not match, should be the same"

    @pytest.mark.dependency(depends=["TestKeeperDB::test_db_connection"])
    def test_get_data(self, keeper_db, test_data_to_save):
        keeper_db.save_data(test_data_to_save.copy())

        random_key, random_value = random.choice(list(test_data_to_save.items()))
        data_from_keeper = json.loads(keeper_db.get_data({random_key: random_value})).pop()
        data_from_keeper.pop('_id')

        is_same_data = test_data_to_save == data_from_keeper
        assert is_same_data, "Saved and received data does not match, should be the same"
