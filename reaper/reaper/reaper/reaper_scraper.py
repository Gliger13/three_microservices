import requests
from jobs_parser.app import App

import settings


class ReaperScraper:
    def __init__(
            self,
            first_paginator_url_template: str,
            words_to_find: [str],
            block_link_class: str = None,
            classes_to_exclude: [str] = (),
            request_headers: dict = None,
            start_page: int = None, end_page: int = None
    ):
        self.parser = App(
            first_paginator_url_template, words_to_find,
            block_link_class=block_link_class,
            classes_to_exclude=classes_to_exclude,
            request_headers=request_headers,
            start_page=start_page, end_page=end_page
        )

    def _is_keeper_alive(self) -> bool:
        return requests.head(settings.KEEPER_URL).ok

    def _save_results(self, data: dict) -> bool:
        request_json = {
            'command_name': 'save_data',
            'data': data,
        }
        return requests.post(settings.KEEPER_URL, json=request_json).ok

    def parse(self) -> dict:
        results = self.parser.parse().json()
        if self._is_keeper_alive():
            self._save_results(results)
        return results
