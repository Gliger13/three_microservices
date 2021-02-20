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

    @pytest.mark.parametrize(
        'test_data,expected', [
            ({'command_name': 'get_data'}, True),
            ({'command_name': 'wrong_command_name'}, False),
            ({'command_name': 'run_web_parser', 'data': 111111}, True),
            ({'command_name': 'run_web_parser', 'data': {'data': 'useless data'}}, True),
            ({'data': '12345'}, False),
            ({}, False),
        ]
    )
    def test_post_request(self, test_data, expected):
        r = requests.post(settings.url, data=test_data)
        assert r.ok == expected
