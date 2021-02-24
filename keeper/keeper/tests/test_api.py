import contextlib

import pytest
import requests

import settings
from api.validator import KeeperValidation


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


class TestKeeperAPI:
    @pytest.mark.dependency()
    def test_connection(self):
        is_ok_connection = False
        try:
            requests.head(settings.url)
            is_ok_connection = True
        except (requests.ConnectionError, requests.Timeout):
            pass
        assert is_ok_connection, "Connection error, should be no connection problems"

    @pytest.mark.dependency(depends=["TestKeeperAPI::test_connection"])
    def test_get_request(self):
        assert requests.get(settings.url).ok, "The status of the request code is not 200, it should only be 200"

    @pytest.mark.dependency(depends=["TestKeeperAPI::test_connection", "TestKeeperAPI::test_get_request"])
    @pytest.mark.parametrize('test_input', [('save_data', 'get_data')])
    def test_get_content(self, test_input):
        available_commands = requests.get(settings.url).json()['available_commands']
        is_same_commands = sorted(available_commands.keys()) == sorted(test_input)
        assert is_same_commands, "Expected commands are not the same as actual available commands, should be same"

    @pytest.mark.dependency(depends=["TestKeeperAPI::test_connection", "TestKeeperAPI::test_get_request"])
    def test_get_content_help(self):
        available_commands = requests.get(settings.url).json()['available_commands']
        is_all_help_is_str = all((isinstance(help_content, str) for help_content in available_commands.values()))
        assert is_all_help_is_str, "Help on command is not of str type, should be str"

    @pytest.mark.dependency(depends=["TestKeeperAPI::test_connection"])
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
        response = requests.post(settings.url, json=test_input)
        assert response.ok == expected, "Status code of request should be 200 or 400"

    @pytest.mark.dependency(depends=["TestKeeperAPI::test_connection"])
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
        response = requests.post(settings.url, json=test_input)
        assert response.ok == expected, "Status code of request should be 200 or 400"
