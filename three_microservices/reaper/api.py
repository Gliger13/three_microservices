from flask import Flask
from flask_restful import Resource, Api, reqparse

import settings
from commands.api_commands import ReaperCommands
from validator import ReaperValidation


class Reaper(Resource):
    def __init__(self):
        self.validator = ReaperValidation()

    @staticmethod
    def get():
        return {'available_commands': ReaperCommands().available_commands}

    def _post_parser(self):
        args_parser = reqparse.RequestParser()
        args_parser.add_argument('command_name', type=self.validator.valid_command_name, required=True)
        args_parser.add_argument('data', type=self.validator.valid_data, location='json', required=True)
        return args_parser.parse_args()

    def post(self):
        args = self._post_parser()
        command_name = args.get('command_name')
        data = args.get('data')
        return ReaperCommands().run_command(command_name, data)


class ReaperAPI:
    def __init__(self):
        self.app = Flask('Reaper')
        self.api = Api(self.app)

    def run(self):
        self.api.add_resource(Reaper, '/')
        self.app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    ReaperAPI().run()
    # ReaperValidation().valid_data_to_parsing(1, 1)
