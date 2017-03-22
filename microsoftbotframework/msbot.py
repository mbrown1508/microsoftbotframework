from flask import Flask, request
from celery.local import PromiseProxy
from .config import Config


class MsBot:
    def __init__(self, host=None, port=None):
        self.processes = []
        config = Config()
        self.host = config.get_config(host, 'HOST', root='flask')
        self.port = config.get_config(port, 'PORT', root='flask')

        self.app = Flask(__name__)

        @self.app.route('/api/messages', methods=['POST'])
        def message_post():
            # TODO: Confirm that it is from microsoft
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
        self.app.run(host=self.host, port=self.port)
