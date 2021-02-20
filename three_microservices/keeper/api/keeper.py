from flask_restful import reqparse, Resource

from .api_commands import KeeperCommands
from .validator import KeeperValidation


class Keeper(Resource):
    def __init__(self):
        self.validator = KeeperValidation()
        self.reaper_commands = KeeperCommands()

    def get(self):
        return {'available_commands': self.reaper_commands.available_commands}

    def _post_parser(self):
        args_parser = reqparse.RequestParser()
        args_parser.add_argument('command_name', type=self.validator.valid_command_name, required=True)
        args_parser.add_argument('data', type=self.validator.valid_date, location='json', required=True)
        return args_parser.parse_args()

    def post(self):
        args = self._post_parser()
        command_name = args.get('command_name')
        data = args.get('data')
        print(data)
        return self.reaper_commands.run_command(command_name, data)
