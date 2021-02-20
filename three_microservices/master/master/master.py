from flask_restful import Resource, reqparse

from api.api_commands import MasterCommands
from api.validator import MasterValidation


class Master(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.validator = MasterValidation()
        self.commands = MasterCommands()

    def get(self):
        return {'available_commands': self.commands.available_commands}

    def _post_parser(self):
        self.parser.add_argument('command_name', type=self.validator.valid_command_name, required=True)
        self.parser.add_argument('data')
        return self.parser.parse_args()

    def post(self):
        args = self._post_parser()
        command_name = args.get('command_name')
        data = args.get('data')
        return self.commands.run_command(command_name, data)
