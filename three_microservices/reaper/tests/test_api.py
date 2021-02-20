import contextlib
import logging

import pytest
import requests

import settings
from api import ReaperValidation


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


class TestMasterAPI:
    def test_connection(self):
        r = requests.head(settings.url)
        assert r.ok

    def test_get_request(self):
        r = requests.get(settings.url)
        assert r.ok

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

    @pytest.mark.parametrize('test_data,expected', test_data_scraping)
    def test_start_scraping(self, test_data, expected):
        result = requests.post(settings.url, json=test_data)
        assert result.ok == expected
