import json
import random

import pytest
import requests


class TestKeeperGET:
    @pytest.mark.dependency(
        depends=["test_connection.py::test_keeper_connection"],
        scope="session",
    )
    def test_get_request(self, keeper_url):
        assert requests.get(keeper_url).ok, "The status of the request code is not 200, it should only be 200"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_keeper.py::TestKeeperGET::test_get_request"
        ],
        scope="session",
    )
    @pytest.mark.parametrize('test_input', [('save_data', 'get_data')])
    def test_get_content(self, test_input, keeper_url):
        available_commands = requests.get(keeper_url).json()['available_commands']
        is_same_commands = sorted(available_commands.keys()) == sorted(test_input)
        assert is_same_commands, "Expected commands are not the same as actual available commands, should be same"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_keeper.py::TestKeeperGET::test_get_request"
        ],
        scope="session",
    )
    def test_get_content_help(self, keeper_url):
        available_commands = requests.get(keeper_url).json()['available_commands']
        is_all_help_is_str = all((isinstance(help_content, str) for help_content in available_commands.values()))
        assert is_all_help_is_str, "Help on command is not of str type, should be str"


class TestKeeperAPI:
    @pytest.mark.dependency(
        depends=["test_connection.py::test_keeper_connection"],
        scope="session",
    )
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
    def test_get_data(self, test_input, expected, keeper_url):
        response = requests.post(keeper_url, json=test_input)
        assert response.ok == expected, "Status code of request should be 200 or 400"

    @pytest.mark.dependency(
        depends=["test_connection.py::test_keeper_connection"],
        scope="session",
    )
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
    def test_save_data(self, test_input, expected, keeper_url):
        response = requests.post(keeper_url, json=test_input)
        assert response.ok == expected, "Status code of request should be 200 or 400"
