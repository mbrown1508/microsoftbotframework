import microsoftbotframework.runcelery
from microsoftbotframework import MsBot
from tasks import *


bot = MsBot(verify_jwt_signature=False, debug=True)
bot.add_process(respond_to_conversation_update)
bot.add_process(synchronous_response)
bot.add_process(asynchronous_response)
bot.run()
