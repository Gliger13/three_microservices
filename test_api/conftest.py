import pytest
import requests


@pytest.fixture(params=[{
    'keeper_url': '0.0.0.0:8002',
    'reaper_url': '0.0.0.0:8001',
    'master_url': '0.0.0.0:8000',
}])
def api_url():
    return 'http://0.0.0.0:8002'


@pytest.fixture
def keeper_url():
    return 'http://0.0.0.0:8002'


@pytest.fixture
def reaper_url():
    return 'http://0.0.0.0:8001'


@pytest.fixture
def master_url():
    return 'http://0.0.0.0:8000'

