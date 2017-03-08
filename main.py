import microsoftbotframework.runcelery
from microsoftbotframework.msbot import MsBot
from tasks import *

bot = MsBot()
bot.add_process(RespondToConversationUpdate)
bot.add_process(ChatBotRespond)
bot.run()
