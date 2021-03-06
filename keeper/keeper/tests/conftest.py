import pytest

from keeper.database import KeeperDB


@pytest.fixture
def keeper_db():
    return KeeperDB()


@pytest.fixture
def clear_db(keeper_db):
    keeper_db.collection.delete_many({})
