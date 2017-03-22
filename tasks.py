from microsoftbotframework import Response
import celery


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        response = Response(message)
        message_response = 'Have fun with the Microsoft Bot Framework'
        response.reply_to_activity(message_response, recipient={"id": response["conversation"]["id"]})


# If you have setup a celery backend then you can uncomment the line below.
@celery.task()
def echo_response(message):
    if message["type"] == "message":
        response = Response(message)
        message_response = message["text"]
        response.reply_to_activity(message_response)
