from flask import Flask
from flask_restful import Api

import settings
from master.master import Master


class MasterAPI:
    def __init__(self):
        self.app = Flask('Master')
        self.api = Api(self.app)

    def run(self):
        self.api.add_resource(Master, '/')
        self.app.run(host=settings.HOST, port=settings.PORT, debug=settings.DEBUG)


if __name__ == '__main__':
    MasterAPI().run()
