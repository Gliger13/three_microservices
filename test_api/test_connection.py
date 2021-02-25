import pytest
import requests

def is_connection(url):
    try:
        requests.head(url)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


@pytest.mark.dependency()
def test_keeper_connection():
    url = "http://0.0.0.0:8002"
    assert is_connection(url), f"Connection error with {url}, should be no connection problems"


@pytest.mark.dependency()
def test_reaper_connection():
    url = "http://0.0.0.0:8001"
    assert is_connection(url), f"Connection error with {url}, should be no connection problems"


@pytest.mark.dependency()
def test_master_connection():
    url = "http://0.0.0.0:8000"
    assert is_connection(url), f"Connection error with {url}, should be no connection problems"
