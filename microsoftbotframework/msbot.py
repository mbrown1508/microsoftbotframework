from flask import Flask, request
from celery.local import PromiseProxy
from .config import Config


class MsBot:
    def __init__(self, host=None, port=None, debug=None):
        self.processes = []
        config = Config()
        self.host = config.get_config(host, 'HOST', root='flask')
        self.port = config.get_config(port, 'PORT', root='flask')
        self.debug = config.get_config(debug, 'DEBUG', root='flask')

        self.app = Flask(__name__)

        @self.app.route('/api/messages', methods=['POST'])
        def message_post():
            # TODO: Confirm that it is from microsoft

            json_message = request.get_json()

            self.app.logger.info('message.headers: {}'.format(request.headers))
            self.app.logger.info('message.body: {}'.format(json_message))

            for process in self.processes:
                if isinstance(process, PromiseProxy):
                    self.app.logger.info('Processing task {} asynchronously.'.format(type(process).__name__))
                    process.delay(json_message)
                elif callable(process):
                    self.app.logger.info('Processing task {} synchronously.'.format(process.__name__))
                    process(json_message)
            return "Success"

    def add_process(self, process):
        self.processes.append(process)

    def run(self):
        self.app.run(host=self.host, port=self.port, debug=self.debug)
