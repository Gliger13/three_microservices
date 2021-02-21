import contextlib

import pytest
import requests

import settings
from api.validator import MasterValidation


@contextlib.contextmanager
def does_not_raise():
    yield


class TestMasterValidation:
    @pytest.mark.parametrize('test_data,expectation', [
        ('get_data', does_not_raise()),
        ('run_web_parser', does_not_raise()),
        ('wrong_command_name', pytest.raises(ValueError)),
        (None, pytest.raises(ValueError)),
    ])
    def test_valid_command_name(self, test_data, expectation):
        with expectation:
            MasterValidation().valid_command_name(test_data)


class TestMasterAPI:
    def test_connection(self):
        r = requests.head(settings.url)
        assert r.ok

    def test_get_request(self):
        r = requests.get(settings.url)
        assert r.ok

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
    def test_run_web_parser(self, test_data, expected):
        response = requests.post(settings.url, json=test_data)
        assert response.ok == expected
