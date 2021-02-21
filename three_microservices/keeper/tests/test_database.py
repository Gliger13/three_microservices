import json

import pytest


@pytest.fixture(autouse=True)
def clear_db(keeper_db):
    keeper_db.collection.delete_many({})


class TestKeeperDB:
    def test_save_data(self, keeper_db):
        keeper_db.save_data({
            'test_data': 'data'
        })
        assert keeper_db.collection.find({'test_data': 'data'})

    @pytest.mark.parametrize('test_data', [
        {
            'test_data': 'data',
            'data1': 'data',
            'data2': 'data',
        },
    ])
    def test_get_data(self, test_data, keeper_db):
        keeper_db.save_data(test_data)
        assert json.loads(keeper_db.get_data({'test_data': 'data'})).pop().get('data1') == test_data.get('data1')
