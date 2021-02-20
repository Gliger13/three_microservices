from flask import Flask
from flask_restful import Resource, Api, reqparse
import settings
from commands.commands import MasterCommands


class MasterValidation:
    def __init__(self):
        self.master_commands = MasterCommands()

    def valid_command_name(self, value):
        if value not in self.master_commands.available_commands:
            raise ValueError(f'Microservice Master has no command with name {value}')
        return value


class Master(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.validator = MasterValidation()

    def get(self):
        return {'available_commands': MasterCommands().available_commands}

    def _post_parser(self):
        self.parser.add_argument('command_name', type=self.validator.valid_command_name, required=True)
        self.parser.add_argument('data')
        return self.parser.parse_args()

    def post(self):
        args = self._post_parser()
        command_name = args.get('command_name')
        data = args.get('data')

        master_commands = MasterCommands()
        return master_commands.run_command(command_name, data)


class MasterAPI:
    def __init__(self):
        self.app = Flask('Master')
        self.api = Api(self.app)

    def run(self):
        self.api.add_resource(Master, '/')
        self.app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    MasterAPI().run()
