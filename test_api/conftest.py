import pytest


@pytest.fixture
def keeper_url():
    return 'http://0.0.0.0:8002'


@pytest.fixture
def reaper_url():
    return 'http://0.0.0.0:8001'


@pytest.fixture
def master_url():
    return 'http://0.0.0.0:8000'

