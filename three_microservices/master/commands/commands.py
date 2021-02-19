
class MasterCommands:
    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        return [arg for arg in dir(MasterCommands) if not arg.startswith('_') and arg not in not_commands]

    def run_command(self, command_name, data):
        return getattr(self.__class__, command_name)(self, data)

    def get_data(self, *args, **kwargs):
        return 'some_data'

    def run_web_parser(self, data, *args, **kwargs):
        return 'run parser'
