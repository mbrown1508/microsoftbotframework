from flask import Flask, request
from celery.local import PromiseProxy
import os

class MsBot:
    def __init__(self):
        self.processes = []

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
        port = int(os.environ.get("PORT", 5000))
        self.app.run(host='0.0.0.0', port=port)
