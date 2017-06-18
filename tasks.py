from microsoftbotframework import ReplyToActivity, SendToConversation, DeleteActivity, CreateConversation, GetActivityMembers, GetConversationMembers, UploadAttachmentToChannel
import celery
from time import sleep
import re


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        message_response = 'Have fun with the Microsoft Bot Framework'
        ReplyToActivity(fill=message,
                        text=message_response).send()


def echo_response(message):
    if message["type"] == "message":
        ReplyToActivity(fill=message,
                        text=message["text"]).send()


# This is a asynchronous task
@celery.task()
def echo_response_async(message):
    if message["type"] == "message":
        if re.search("Get Members", message['text']):
            conversation_response = GetConversationMembers(fill=message).send()
            activity_response = GetActivityMembers(fill=message).send()

            response_text = 'Conversation: {}; Activity: {}'.format(conversation_response.text, activity_response.text)
            personal_message(message, response_text)

        elif re.search("cat", message['text']):
            UploadAttachmentToChannel(
                fill=message,
                upload_filename='cute cat.jpg',
                upload_file_path='/home/skippy/Desktop/cute cat.jpg',
                upload_type='image/jpeg',
            ).send()
        else:

            response_info = ReplyToActivity(fill=message,
                                            text=message["text"]).send()

            sleep(5)

            # This activity doesn't seem to work in most chat applications.
            DeleteActivity(fill=message,
                           activityId=response_info.json()['id']).send()

            sleep(2)

            personal_message(message, message['text'])


def personal_message(message, response_text):
    # The activity passed in the create conversation seems to have no effect.
    # This also triggers a conversation update. May want to check if your bot is the one joining the conversation.
    response_info = CreateConversation(fill=message,
                                       text=response_text).send()

    send_to_conversation = SendToConversation(fill=message,
                                              conversationId=response_info.json()['id'],
                                              text=response_text)

    # make sure that we remove and team or channel data from the request when working in teams.
    # If the bot is only designed to work in teams this could be passed in the arguments to SendToConversation
    if send_to_conversation.channelData is not None and 'tenant' in send_to_conversation.channelData:
        send_to_conversation.channelData = {"tenant": {"id": send_to_conversation.channelData["tenant"]["id"]}}

    send_to_conversation.send()



