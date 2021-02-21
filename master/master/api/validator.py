from api.api_commands import MasterCommands


class MasterValidation:
    def __init__(self):
        self.master_commands = MasterCommands()

    def valid_command_name(self, value):
        if value not in self.master_commands.available_commands:
            raise ValueError(f'Microservice Master has no command with name {value}')
        return value
