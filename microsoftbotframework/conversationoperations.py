from .activity import Activity


class ReplyToActivity(Activity):
    def __init__(self, **kwargs):
        super(ReplyToActivity, self).__init__(reply_to_activity=True, **kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}".format(
                                    self.conversation['id'],
                                    self.activityId))

        response = self._request(response_url, 'post', self.to_dict())

        self.save_response('ReplyToActivity',
                           self.conversation['id'],
                           self.to_dict(),
                           {'conversationId': self.conversation['id'], 'activityId': self.activityId},
                           response.json())
        return response


class SendToConversation(Activity):
    def __init__(self, **kwargs):
        super(SendToConversation, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities".format(
                                        self.conversation['id']))

        response = self._request(response_url, 'post', self.to_dict())

        self.save_response('SendToConversation',
                           self.conversation['id'],
                           self.to_dict(),
                           {'conversationId': self.conversation['id']},
                           response.json())
        return response


class DeleteActivity(Activity):
    def __init__(self, **kwargs):
        super(DeleteActivity, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}".format(
                                    self.conversation['id'],
                                    self.activityId))

        raw_response = self._request(response_url, 'delete')

        if raw_response.text != '':
            response = raw_response.json()
        else:
            response = None

        self.save_response('DeleteActivity',
                           self.conversation['id'],
                           None,
                           {'conversationId': self.conversation['id'], 'activityId': self.activityId},
                           response)
        return response


class CreateConversation(Activity):
    def __init__(self, **kwargs):
        super(CreateConversation, self).__init__(**kwargs)

    def send(self):
        # make sure that we remove and team or channel data from the request when working in teams.
        if self.channelData is not None and 'tenant' in self.channelData:
            self.channelData = {"tenant": {"id": self.channelData["tenant"]["id"]}}
        self.channelId = None
        self.conversation = None

        request_json = {
            'bot': self.fromAccount if self.bot is None else self.bot,
            'isGroup': False if self.isGroup is None else self.isGroup,
            'members': [self.recipient] if self.members is None else self.members,
            'channelData': self.channelData,
            'activity': self.to_dict(),
        }

        if len(request_json['members']) > 1:
            request_json['isGroup'] = True

        if self.topicName is not None:
            request_json['topicName'] = self.topicName

        response_url = self.urljoin(self.serviceUrl, "/v3/conversations")

        response = self._request(response_url, 'post', request_json)

        # Skype for Business returns the key 'Id', not 'id', fix the response
        # by changing 'Id' to 'id'
        response_json = response.json()
        if 'Id' in response_json and 'id' not in response_json:
            response._content = response._content.replace(b"\"Id\":",
                                                          b"\"id\":")
        response_json = response.json()
        # save the response if it worked, http error codes won't save respones
        if 'id' in response_json:
            self.save_response('CreateConversation',
                               response_json['id'],
                               request_json,
                               {},
                               response_json)
        return response


class GetConversationMembers(Activity):
    def __init__(self, **kwargs):
        super(GetConversationMembers, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/members".format(
                                    self.conversation['id']))

        response = self._request(response_url, 'get')

        self.save_response('GetConversationMembers',
                           self.conversation['id'],
                           None,
                           {'conversationId': self.conversation['id']},
                           response.json())
        return response


class GetActivityMembers(Activity):
    def __init__(self, **kwargs):
        super(GetActivityMembers, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}/members".format(
                                    self.conversation['id'],
                                    self.activityId))

        response = self._request(response_url, 'get')

        self.save_response('GetActivityMembers',
                           self.conversation['id'],
                           None,
                           {'conversationId': self.conversation['id'], 'activityId': self.activityId},
                           response.json())
        return response
