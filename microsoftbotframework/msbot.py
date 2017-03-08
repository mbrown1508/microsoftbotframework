__author__ = 'Matthew'
from flask import Flask, request
from microsoftbotframework.helpers import ConfigSectionMap
from celery.local import PromiseProxy

class MsBot:
    def __init__(self):
        self.config = ConfigSectionMap('CELERY')
        self.processes = []

        self.app = Flask(__name__)

        @self.app.route('/api/messages', methods=['POST'])
        def message_post():
            #TODO: Verfiy if message is from microsoft or Emulator

            json_message = request.get_json()
            for process in self.processes:
                if isinstance(process, PromiseProxy):
                    process.delay(json_message)
                elif callable(process):
                    process(json_message)
            return "Success"


    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        self.app.run()

    def auto_load(self):
        pass
        # TODO: Check for any methods in tasks and autoload them