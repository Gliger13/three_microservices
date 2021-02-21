from keeper.database import KeeperDB


class KeeperCommands:
    def __init__(self):
        self.keeper_db = KeeperDB()

    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        return [arg for arg in dir(self.__class__) if not arg.startswith('_') and arg not in not_commands]

    def run_command(self, command_name: str, data: dict):
        return getattr(self.__class__, command_name)(self, data)

    def save_data(self, data):
        self.keeper_db.save_data(data)

    def get_data(self, keys_to_find):
        return self.keeper_db.get_data(keys_to_find)
