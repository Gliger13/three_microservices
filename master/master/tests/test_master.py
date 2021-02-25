import contextlib

import pytest

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
