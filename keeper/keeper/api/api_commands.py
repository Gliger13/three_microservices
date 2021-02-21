from keeper.database import KeeperDB


class KeeperCommands:
    def __init__(self):
        self.keeper_db = KeeperDB()

    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        available_commands = [arg for arg in dir(self.__class__) if not arg.startswith('_') and arg not in not_commands]
        return {command: getattr(self.__class__, command).__doc__ for command in available_commands}

    def run_command(self, command_name: str, data: dict):
        return getattr(self.__class__, command_name)(self, data)

    def save_data(self, data):
        """
        Save data in MongoDB

        Usage. Example of correct JSON in the POST request:
        {
            "command_name": "save_data",
            "data": {"car_id": 123456}
        }
        """
        self.keeper_db.save_data(data)

    def get_data(self, keys_to_find):
        """
        Save data in MongoDB

        Usage. Example of correct JSON in the POST request:
        {
            "command_name": "get_data",
            "data": {"car_id": 123456}
        }
        """
        return self.keeper_db.get_data(keys_to_find)
