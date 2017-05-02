from microsoftbotframework import Response
import celery


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        response = Response(message)
        message_response = 'Have fun with the Microsoft Bot Framework'
        response.reply_to_activity(message_response, recipient={"id": response["conversation"]["id"]})


def echo_response(message):
    if message["type"] == "message":
        response = Response(message)
        message_response = message["text"]
        response_info = response.reply_to_activity(message_response)

#        from time import sleep

#        sleep(2)
#        response.delete_activity(activity_id=response_info.json()['id'])

#        sleep(2)
#        response.create_conversation('lets talk about something really interesting')


# This is a asynchronous task
@celery.task()
def echo_response_async(message):
    if message["type"] == "message":
        response = Response(message)
        message_response = message["text"]
        response.send_to_conversation(message_response)

