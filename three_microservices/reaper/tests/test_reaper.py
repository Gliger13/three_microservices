from ..reaper.reaper_scraper import ReaperScraper


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
        ).parse().popitem()[1]
        assert 2 > result > 0
