import jsonschema

from commands.api_commands import ReaperCommands


class ReaperValidation:
    def __init__(self):
        self.reaper_commands = ReaperCommands()
        self.command_name = None

    def valid_command_name(self, value):
        if value not in self.reaper_commands.available_commands:
            raise ValueError(f'Microservice Reaper has no command with name {value}')
        self.command_name = value
        return value

    def valid_data_to_parsing(self, value):
        json_schema = {
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
        jsonschema.validate(value, json_schema)

    def valid_data(self, value):
        if self.command_name == 'start_scraping':
            self.valid_data_to_parsing(value)
        return value

