'''
I use this file to test the library on heroku.
'''

from microsoftbotframework import Response
import celery
from tasks import *
from microsoftbotframework.msbot import MsBot
import os


if __name__ == "__main__":
    import microsoftbotframework.runcelery
    import logging
    log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    formatter = logging.Formatter(log_format)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.INFO)
    streamHandler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        format=log_format)

    bot = MsBot()
    bot.add_process(respond_to_conversation_update)
    bot.add_process(synchronous_response)
    bot.add_process(asynchronous_response)
    #
    log = bot.logger
    log.setLevel(logging.INFO)
    log.addHandler(streamHandler)

    bot.run(port=int(os.environ['PORT']))
