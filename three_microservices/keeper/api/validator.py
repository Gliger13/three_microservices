from api.api_commands import KeeperCommands


class KeeperValidation:
    def __init__(self):
        self.reaper_commands = KeeperCommands()
        self.command_name = None

    def valid_command_name(self, value):
        if value not in self.reaper_commands.available_commands:
            raise ValueError(f'Microservice Keeper has no command with name {value}')
        self.command_name = value
        return value

    @staticmethod
    def valid_date(value, name):
        if not value:
            raise ValueError(f'Data passed through {name} is empty')
        return value
