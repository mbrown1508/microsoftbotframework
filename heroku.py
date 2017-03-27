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

    bot = MsBot(port=int(os.environ['PORT']), debug=True)
    bot.add_process(respond_to_conversation_update)
    bot.add_process(echo_response_async)
    bot.add_process(echo_response)
    bot.run()
