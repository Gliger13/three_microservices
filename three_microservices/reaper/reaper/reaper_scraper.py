from jobs_parser.app import App


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

    def _save_results(self, data: dict):
        return 'save_process in Keeper'

    def parse(self) -> dict:
        results = self.parser.parse().average_num_of_words_occur()
        self._save_results(results)
        return results
