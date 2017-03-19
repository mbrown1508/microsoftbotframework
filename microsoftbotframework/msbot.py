from flask import Flask, request
from celery.local import PromiseProxy
from .utils import get_config


class MsBot:
    def __init__(self, host=None, port=None):
        self.processes = []
        self.host = get_config(host, 'HOST', '0.0.0.0')
        self.port = int(get_config(port, 'PORT', 5000))

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
