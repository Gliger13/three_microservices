import contextlib

import pytest

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
