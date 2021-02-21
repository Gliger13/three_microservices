import requests

import settings


class MasterCommands:
    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        return [arg for arg in dir(MasterCommands) if not arg.startswith('_') and arg not in not_commands]

    def run_command(self, command_name, data):
        return getattr(self.__class__, command_name)(self, data)

    def get_data(self, data):
        request_data = {
            'command_name': 'get_data',
            'data': data
        }
        return requests.post(settings.KEEPER_URL, json=request_data).json()

    def run_web_parser(self, data):
        request_data = {
            'command_name': 'start_scraping',
            'data': data
        }
        return requests.post(settings.REAPER_URL, json=request_data).json()
