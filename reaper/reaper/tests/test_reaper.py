import contextlib

import pytest
from reaper.reaper_scraper import ReaperScraper

from api.validator import ReaperValidation


@contextlib.contextmanager
def does_not_raise():
    yield


class TestReaperValidation:
    @pytest.mark.parametrize('test_data,expectation', [
        ('start_scraping', does_not_raise()),
        ('wrong_command_name', pytest.raises(ValueError)),
        (None, pytest.raises(ValueError)),
    ])
    def test_valid_command_name(self, test_data, expectation):
        with expectation:
            ReaperValidation().valid_command_name(test_data)


class TestReaperScraper:
    def test_parse(self):
        url_template = 'https://rabota.by/search/vacancy?text=Python&page={page_number}'
        words = ['Linux']
        request_headers = {'user-agent': 'job_parser/1.1.1'}
        classes_to_exclude = ['recommended-vacancies', 'related-vacancies-wrapper']
        block_class = 'bloko-link HH-LinkModifier'
        result = ReaperScraper(
            url_template,
            words,
            block_link_class=block_class,
            classes_to_exclude=classes_to_exclude,
            request_headers=request_headers,
            start_page=0, end_page=1
        ).parse().get('parse_results').get('Linux')
        assert 100 > result > 0
