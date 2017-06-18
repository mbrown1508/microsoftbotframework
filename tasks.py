from microsoftbotframework import ReplyToActivity, SendToConversation, DeleteActivity, CreateConversation
import celery
from time import sleep


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        message_response = 'Have fun with the Microsoft Bot Framework'
        ReplyToActivity(fill=message,
                        text=message_response).send()


def echo_response(message):
    if message["type"] == "message":
        message_response = message["text"]
        ReplyToActivity(fill=message,
                        text=message_response,
                        reply_to_activity=True).send()


# This is a asynchronous task
@celery.task()
def echo_response_async(message):
    if message["type"] == "message":
        message_response = message["text"]
        response_info = ReplyToActivity(fill=message,
                                        text=message_response,
                                        reply_to_activity=True).send()

        sleep(5)

        DeleteActivity(fill=message,
                       activityId=response_info.json()['id']).send()

        sleep(2)

        # The activity passed in the create conversation seems to have no effect.
        response_info = CreateConversation(fill=message,
                                           topicName='Starting a conversation',
                                           text='Lets have a conversation').send()

        send_to_conversation = SendToConversation(fill=message,
                                                  conversation={'id': response_info.json()['id']},
                                                  text=message_response)

        # make sure that we remove and team or channel data from the request when working in teams.
        if send_to_conversation.channelData is not None and 'tenant' in send_to_conversation.channelData:
            send_to_conversation.channelData = {"tenant": {"id": send_to_conversation.channelData["tenant"]["id"]}}

        send_to_conversation.send()
