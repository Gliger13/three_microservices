import pytest
import requests


class TestMasterGET:
    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_master_connection"
        ],
        scope="session",
    )
    def test_get_request(self, master_url):
        assert requests.get(master_url).ok, "The status of the request code is not 200, it should only be 200"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_master.py::TestMasterGET::test_get_request"
        ],
        scope="session",
    )
    @pytest.mark.parametrize('test_input', [('run_web_parser', 'get_data')])
    def test_get_content(self, test_input, master_url):
        available_commands = requests.get(master_url).json()['available_commands']
        is_same_commands = sorted(available_commands.keys()) == sorted(test_input)
        assert is_same_commands, "Expected commands are not the same as actual available commands, should be same"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_master.py::TestMasterGET::test_get_request"
        ],
        scope="session",
    )
    def test_get_content_help(self, master_url):
        available_commands = requests.get(master_url).json()['available_commands']
        is_all_help_is_str = all((isinstance(help_content, str) for help_content in available_commands.values()))
        assert is_all_help_is_str, "Help on command is not of str type, should be str"


class TestMasterAPI:
    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_master_connection",
            "test_connection.py::test_reaper_connection",
            "test_connection.py::test_keeper_connection",
        ],
        scope="session",
    )
    @pytest.mark.parametrize('test_data,expected', [
        ({
             'command_name': 'run_web_parser',
             'data': {
                 'first_paginator_url_template': 'https://rabota.by/search/vacancy?text=Python&page={page_number}',
                 'words_to_find': ['python'],
                 'request_headers': {'user-agent': 'job_parser/1.1.1'},
                 'block_link_class': 'bloko-link HH-LinkModifier',
                 'start_page': 0,
                 'end_page': 1,
             }
         }, True),
        ({
             'command_name': 'run_web_parser',
             'data': {
                 'first_paginator_url_template': 'https://rabota.by/search/vacancy?text=Python&page={page_number}',
                 'words_to_find': ['Linux'],
                 'request_headers': {'user-agent': 'job_parser/1.1.1'},
                 'classes_to_exclude': ['recommended-vacancies', 'related-vacancies-wrapper'],
                 'block_link_class': 'bloko-link HH-LinkModifier',
                 'start_page': 0,
                 'end_page': 1,
             }
         }, True),
    ])
    def test_run_web_parser(self, test_data, expected, master_url):
        response = requests.post(master_url, json=test_data)
        assert response.ok == expected
