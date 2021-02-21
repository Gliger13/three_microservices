from flask_restful import reqparse, Resource

from .api_commands import ReaperCommands
from .validator import ReaperValidation


class Reaper(Resource):
    def __init__(self):
        self.validator = ReaperValidation()
        self.reaper_commands = ReaperCommands()

    def get(self):
        return {'available_commands': self.reaper_commands.available_commands}

    def _post_parser(self):
        args_parser = reqparse.RequestParser()
        args_parser.add_argument('command_name', type=self.validator.valid_command_name, required=True)
        args_parser.add_argument('data', type=self.validator.valid_data, location='json', required=True)
        return args_parser.parse_args()

    def post(self):
        args = self._post_parser()
        command_name = args.get('command_name')
        data = args.get('data')
        return self.reaper_commands.run_command(command_name, data)
