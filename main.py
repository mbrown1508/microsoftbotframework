import microsoftbotframework.runcelery
from microsoftbotframework import MsBot
from tasks import *

import logging
log_format = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
formatter = logging.Formatter(log_format)

streamHandler = logging.StreamHandler()
streamHandler.setLevel(logging.INFO)
streamHandler.setFormatter(formatter)

logging.basicConfig(
    level=logging.INFO,
    format=log_format)

bot = MsBot(verify_jwt_signature=False)
bot.add_process(respond_to_conversation_update)
bot.add_process(synchronous_response)
bot.add_process(asynchronous_response)
#
log = bot.logger
log.setLevel(logging.INFO)
log.addHandler(streamHandler)

if __name__ == '__main__':
    bot.run()
