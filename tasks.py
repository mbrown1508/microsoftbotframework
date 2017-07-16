from microsoftbotframework import ReplyToActivity, SendToConversation, DeleteActivity, CreateConversation, GetActivityMembers, GetConversationMembers
import celery
from time import sleep
from microsoftbotframework import get_state


def respond_to_conversation_update(message):
    if message["type"] == "conversationUpdate":
        for member in message['membersAdded']:
            message_response = 'Conversation Update: Added person was {}'.format(member['name'])
            ReplyToActivity(fill=message,
                            text=message_response).send()

        if len(message['membersAdded']) == 0:
            message_response = 'Conversation Update: No members added'
            ReplyToActivity(fill=message,
                            text=message_response).send()


def synchronous_response(message):
    if message["type"] == "message":
        if 'synchronous' in message["text"] and 'asynchronous' not in message['text']:
            ReplyToActivity(fill=message,
                            text='Synchronous Test: {}'.format(message["text"])).send()

        elif 'history' in message['text']:
            state = get_state('MongodbState')
            ReplyToActivity(fill=message,
                            text='History: {}'.format(state.get_activities(2))).send()


# This is a asynchronous task
@celery.task()
def asynchronous_response(message):
    if message["type"] == "message":
        if "members" in message['text']:
            conversation_response = GetConversationMembers(fill=message).send()
            activity_response = GetActivityMembers(fill=message).send()

            response_text = 'Conversation: {}; Activity: {}'.format(conversation_response.text, activity_response.text)
            personal_message(message, response_text)

        elif "image" in message['text']:
            content_url = 'https://imgflip.com/s/meme/Cute-Cat.jpg'
            ReplyToActivity(fill=message,
                            attachments=[{
                                'contentType': 'image/jpeg',
                                'contentUrl': content_url,
                                'name': 'cute cat.jpg',
                            }]).send()

        elif "asynchronous" in message['text']:
            ReplyToActivity(fill=message,
                            text='Asynchronous Test: {}'.format(message["text"])).send()

        elif 'delete' in message['text']:
            response_info = ReplyToActivity(fill=message,
                                            text='Delete Test: {}'.format(message["text"])).send()

            sleep(5)

            DeleteActivity(fill=message,
                           activityId=response_info.json()['id']).send()

        elif 'personal' in message['text']:
            personal_message(message, 'Personal Message: {}'.format(message['text']))

        elif 'synchronous' not in message["text"]:
            ReplyToActivity(fill=message,
                            text='Nothing was queried').send()


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
