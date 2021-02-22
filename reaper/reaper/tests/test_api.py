import contextlib

import pytest
import requests

import settings
from api.validator import ReaperValidation


@pytest.fixture
def request_header():
    return {'Content-type': 'application/json'}


@contextlib.contextmanager
def does_not_raise():
    yield


class TestMasterValidation:
    @pytest.mark.parametrize('test_data,expectation', [
        ('start_scraping', does_not_raise()),
        ('wrong_command_name', pytest.raises(ValueError)),
        (None, pytest.raises(ValueError)),
    ])
    def test_valid_command_name(self, test_data, expectation):
        with expectation:
            ReaperValidation().valid_command_name(test_data)


class TestReaperAPI:
    @pytest.mark.dependency()
    def test_connection(self):
        is_ok_connection = False
        try:
            requests.head(settings.url)
            is_ok_connection = True
        except (requests.ConnectionError, requests.Timeout):
            pass
        assert is_ok_connection, "Connection error, should be no connection problems"

    @pytest.mark.dependency(depends=["TestReaperAPI::test_connection"])
    def test_get_request(self):
        assert requests.get(settings.url).ok, "The status of the request code is not 200, it should only be 200"

    @pytest.mark.dependency(depends=["TestReaperAPI::test_connection", "TestReaperAPI::test_get_request"])
    @pytest.mark.parametrize('test_input', [('start_scraping', )])
    def test_get_content(self, test_input):
        available_commands = requests.get(settings.url).json()['available_commands']
        is_same_commands = sorted(available_commands.keys()) == sorted(test_input)
        assert is_same_commands, "Expected commands are not the same as actual available commands, should be same"

    @pytest.mark.dependency(depends=["TestReaperAPI::test_connection", "TestReaperAPI::test_get_request"])
    def test_get_content_help(self):
        available_commands = requests.get(settings.url).json()['available_commands']
        is_all_help_is_str = all((isinstance(help_content, str) for help_content in available_commands.values()))
        assert is_all_help_is_str, "Help on command is not of str type, should be str"

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

    @pytest.mark.dependency(depends=["TestReaperAPI::test_connection"])
    @pytest.mark.parametrize('test_data,expected', test_data_scraping)
    def test_start_scraping(self, test_data, expected):
        assert requests.post(settings.url, json=test_data).ok == expected
