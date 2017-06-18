from microsoftbotframework import Response
from microsoftbotframework import Activity
import celery


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        response = Response()
        message_response = 'Have fun with the Microsoft Bot Framework'
        response.reply_to_activity(Activity(fill=message,
                                            text=message_response))


def echo_response(message):
    if message["type"] == "message":
        response = Response()
        message_response = message["text"]
        response.reply_to_activity(Activity(fill=message,
                                            text=message_response,
                                            reply_to_activity=True))




# This is a asynchronous task
@celery.task()
def echo_response_async(message):
    if message["type"] == "message":
        response = Response()
        message_response = message["text"]
        response_info = response.reply_to_activity(Activity(fill=message,
                                            text=message_response,
                                            reply_to_activity=True))

        from time import sleep

        sleep(5)
        response.delete_activity(Activity(fill=message,
                                          activityId=response_info.json()['id']))

        sleep(2)
        response.create_conversation(Activity(fill=message,
                                              topicName='Starting a conversation',
                                              text='Lets have a conversation'))
