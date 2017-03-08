from microsoftbotframework.response import Response
import celery

@celery.task()
def RespondToConversationUpdate(message):
    if message["type"]=="conversationUpdate":
        response = Response(message)
        message_response = 'Have fun with the Microsoft Bot Framework'
        response.reply_to_activity(message_response,recipient={"id":response["conversation"]["id"]})
    elif message["type"]=="message":
        response = Response(message)
        message_response = message["text"]
        response.reply_to_activity(message_response)

# TODO: Method to respond using a chaterbot library
def ChatBotRespond(message):
    pass

