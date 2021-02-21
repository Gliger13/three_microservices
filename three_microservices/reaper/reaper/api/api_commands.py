from reaper.reaper_scraper import ReaperScraper


class ReaperCommands:
    @property
    def available_commands(self):
        not_commands = ['available_commands', 'run_command']
        return [arg for arg in dir(self.__class__) if not arg.startswith('_') and arg not in not_commands]

    def run_command(self, command_name: str, data: dict):
        return getattr(self.__class__, command_name)(data)

    @staticmethod
    def start_scraping(data: dict) -> dict:
        return ReaperScraper(**data).parse()
