import logging

import requests
from jobs_parser.app import App

import settings


module_logger = logging.getLogger('reaper')


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

    @staticmethod
    def _is_keeper_alive() -> bool:
        try:
            response = requests.get(settings.KEEPER_URL)
        except (requests.ConnectionError, requests.Timeout):
            return False
        return response.ok

    def _save_results(self, data: dict):
        if not self._is_keeper_alive():
            module_logger.warning("Keeper doesn't answer. Data saving is not possible")
            return

        request_json = {
            'command_name': 'save_data',
            'data': data,
        }
        response = requests.post(settings.KEEPER_URL, json=request_json)

        if response.ok:
            module_logger.info("Keeper saved parser results")
        else:
            module_logger.warning("Keeper was unable to save parser results")

    def parse(self) -> dict:
        module_logger.info('Start web parser')
        results = self.parser.parse().json()
        module_logger.info('Web parser finished')

        self._save_results(results)
        return results
