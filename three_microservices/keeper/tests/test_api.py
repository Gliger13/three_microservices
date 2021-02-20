import contextlib

import pytest
import requests

from .. import settings
from ..api.validator import KeeperValidation


@contextlib.contextmanager
def does_not_raise():
    yield


class TestKeeperValidation:
    @pytest.mark.parametrize('test_data,expectation', [
        ('save_data', does_not_raise()),
        ('get_data', does_not_raise()),
        ('wrong_command_name', pytest.raises(ValueError)),
        (None, pytest.raises(ValueError)),
    ])
    def test_valid_command_name(self, test_data, expectation):
        with expectation:
            KeeperValidation().valid_command_name(test_data)


class TestMasterAPI:
    def test_connection(self):
        r = requests.head(settings.url)
        assert r.ok

    def test_get_request(self):
        r = requests.get(settings.url)
        assert r.ok

    @pytest.mark.parametrize('test_input,expected', [
        ({
            'command_name': 'get_data',
        }, False),
        ({
            'command_name': 'get_data',
            'data': {}
        }, False),
        ({
            'command_name': 'get_data',
            'data': {
                'test_data': 'data'
            }
        }, True),
    ])
    def test_get_data(self, test_input, expected, keeper_db, clear_db):
        keeper_db.save_data({'test_data': 'data'})
        assert requests.post(settings.url, json=test_input).ok == expected

    @pytest.mark.parametrize('test_input,expected', [
        ({
             'command_name': 'save_data',
         }, False),
        ({
             'command_name': 'save_data',
             'data': {}
         }, False),
        ({
             'command_name': 'save_data',
             'data': {
                 'test_data': 'data'
             }
         }, True),
    ])
    def test_save_data(self, test_input, expected, clear_db):
        assert requests.post(settings.url, json=test_input).ok == expected