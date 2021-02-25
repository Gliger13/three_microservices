import pytest
import requests


class TestReaperGET:
    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
        ],
        scope="session",
    )
    def test_get_request(self, reaper_url):
        assert requests.get(reaper_url).ok, "The status of the request code is not 200, it should only be 200"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_reaper.py::TestReaperGET::test_get_request"
        ],
        scope="session",
    )
    @pytest.mark.parametrize('test_input', [('start_scraping',)])
    def test_get_content(self, test_input, reaper_url):
        available_commands = requests.get(reaper_url).json()['available_commands']
        is_same_commands = sorted(available_commands.keys()) == sorted(test_input)
        assert is_same_commands, "Expected commands are not the same as actual available commands, should be same"

    @pytest.mark.dependency(
        depends=[
            "test_connection.py::test_reaper_connection",
            "test_reaper.py::TestReaperGET::test_get_request"
        ],
        scope="session",
    )
    def test_get_content_help(self, reaper_url):
        available_commands = requests.get(reaper_url).json()['available_commands']
        is_all_help_is_str = all((isinstance(help_content, str) for help_content in available_commands.values()))
        assert is_all_help_is_str, "Help on command is not of str type, should be str"


class TestReaperAPI:
    test_data_scraping = [
        ({
            'command_name': 'start_scraping'
        }, False),
        ({
            'command_name': 'start_scraping',
            'data': {}
        }, False),
        ({
             'command_name': 'start_scraping',
             'data': {
                 'first_paginator_url_template': 111,
                 'words_to_find': 'Linux',
                 'block_link_class': 'bloko-link HH-LinkModifier',
             }
         }, False),
        ({
             'command_name': 'start_scraping',
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
             'command_name': 'start_scraping',
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
    ]

    @pytest.mark.dependency(
        depends=["test_connection.py::test_reaper_connection", "test_connection.py::test_keeper_connection"],
        scope="session",
    )
    @pytest.mark.parametrize('test_data,expected', test_data_scraping)
    def test_start_scraping(self, test_data, expected, reaper_url):
        assert requests.post(reaper_url, json=test_data).ok == expected
