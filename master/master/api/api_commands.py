import requests

import settings


class MasterCommands:
    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        available_commands = [arg for arg in dir(self.__class__) if not arg.startswith('_') and arg not in not_commands]
        return {command: getattr(self.__class__, command).__doc__ for command in available_commands}

    def run_command(self, command_name, data):
        return getattr(self.__class__, command_name)(self, data)

    @staticmethod
    def _is_service_alive(url) -> bool:
        try:
            response = requests.get(url)
        except (requests.ConnectionError, requests.Timeout):
            return False
        return response.ok

    def get_data(self, data):
        """
        Save data using Keeper

        Usage. Example of correct JSON in the POST request:
        {
            "command_name": "get_data",
            "data": {"car_id": 123456}
        }
        """
        if not self._is_service_alive(settings.KEEPER_URL):
            return {'message': 'Service Keeper is not available'}

        request_data = {
            'command_name': 'get_data',
            'data': data
        }
        return requests.post(settings.KEEPER_URL, json=request_data).json()

    def run_web_parser(self, data):
        """
        Send request to Reaper to start scraping

        Example of correct JSON in the POST request:
        {
             "command_name": "run_web_parser",
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
        if not self._is_service_alive(settings.KEEPER_URL):
            return {'message': 'Service Reaper is not available'}

        request_data = {
            'command_name': 'start_scraping',
            'data': data
        }
        return requests.post(settings.REAPER_URL, json=request_data).json()
