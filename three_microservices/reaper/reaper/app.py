from flask import Flask
from flask_restful import Api

import settings
from api.reaper import Reaper


class ReaperApp:
    def __init__(self):
        self.app = Flask('Reaper')
        self.api = Api(self.app)

    def run(self):
        self.api.add_resource(Reaper, '/')
        self.app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    ReaperApp().run()
