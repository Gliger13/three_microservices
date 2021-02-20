from flask import Flask
from flask_restful import Api

import settings
from api.keeper import Keeper


class KeeperApp:
    def __init__(self):
        self.app = Flask('Reaper')
        self.api = Api(self.app)

    def run(self):
        self.api.add_resource(Keeper, '/')
        self.app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    KeeperApp().run()
