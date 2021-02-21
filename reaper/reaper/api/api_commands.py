from reaper.reaper_scraper import ReaperScraper


class ReaperCommands:
    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        available_commands = [arg for arg in dir(self.__class__) if not arg.startswith('_') and arg not in not_commands]
        return {command: getattr(self.__class__, command).__doc__ for command in available_commands}

    def run_command(self, command_name: str, data: dict):
        return getattr(self.__class__, command_name)(data)

    @staticmethod
    def start_scraping(data: dict) -> dict:
        """
        Launches a web scraper with the specified parameters. Parameters can be specified in json body.

        Example of correct JSON in the POST request:
        {
             "command_name": "start_scraping",
             "data": {
                 "first_paginator_url_template": "https://rabota.by/search/vacancy?text=Python&page={page_number}",
                 "words_to_find": ["Linux"],
                 "request_headers": {"user-agent": "reaper/0.0.0"},
                 "classes_to_exclude": ["recommended-vacancies", "related-vacancies-wrapper"],
                 "block_link_class": "bloko-link HH-LinkModifier",
                 "start_page": 0,
                 "end_page": 1,
             }
         }

        JSON schema of data in POST request is:
        data: {
            "type": "object",
            "properties": {
                "first_paginator_url_template": {
                    "description": "URL to the first page of the paginator as str like https://site/page={page_number}",
                    "type": "string"
                },
                "words_to_find": {
                    "description": "The list of words to find in pages",
                    "type": "array",
                    "items": {
                        "type": "string"
                    },
                },
                "request_headers": {
                    "description": "The headers of request",
                    "type": "object"
                },
                "classes_to_exclude": {
                    "description": "Exclude blocks of text by the name of their class divs",
                    "type": "array"
                },
                "block_link_class": {
                    "description": "The name of the class of urls to get them",
                    "type": "string",
                    "items": {
                        "type": "string"
                    },
                },
                "start_page": {
                    "description": "Starting page number of paginator",
                    "type": "integer"
                },
                "end_page": {
                    "description": "Paginator end page number",
                    "type": "integer"
                },
            },
            "required": ["first_paginator_url_template", "words_to_find", 'block_link_class']
        }
        """
        return ReaperScraper(**data).parse()
