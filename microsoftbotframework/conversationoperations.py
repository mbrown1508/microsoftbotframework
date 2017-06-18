from . import Activity
import requests
import base64


class ReplyToActivity(Activity):
    def __init__(self, **kwargs):
        super(ReplyToActivity, self).__init__(reply_to_activity=True, **kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}".format(
                                    self.conversation['id'],
                                    self.activityId))

        return self._request(response_url, requests.post, self.to_dict())


class SendToConversation(Activity):
    def __init__(self, **kwargs):
        super(SendToConversation, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities".format(
                                        self.conversation['id']))

        return self._request(response_url, requests.post, self.to_dict())


class DeleteActivity(Activity):
    def __init__(self, **kwargs):
        super(DeleteActivity, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}".format(
                                    self.conversation['id'],
                                    self.activityId))

        return self._request(response_url, requests.delete)


class CreateConversation(Activity):
    def __init__(self, **kwargs):
        super(CreateConversation, self).__init__(**kwargs)

    def send(self):
        # make sure that we remove and team or channel data from the request when working in teams.
        if self.channelData is not None and 'tenant' in self.channelData:
            self.channelData = {"tenant": {"id": self.channelData["tenant"]["id"]}}
        self.channelId = None
        self.conversation = None

        response_json = {
            'bot': self.fromAccount if self.bot is None else self.bot,
            'isGroup': False if self.isGroup is None else self.isGroup,
            'members': [self.recipient] if self.members is None else self.members,
            'channelData': self.channelData,
            'self': self.to_dict(),
        }

        if len(response_json['members']) > 1:
            response_json['isGroup'] = True

        if self.topicName is not None:
            response_json['topicName'] = self.topicName

        response_url = self.urljoin(self.serviceUrl, "/v3/conversations")

        return self._request(response_url, requests.post, response_json)


class GetConversationMembers(Activity):
    def __init__(self, **kwargs):
        super(GetConversationMembers, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/members".format(
                                    self.conversation['id']))

        return self._request(response_url, requests.get)


class GetActivityMembers(Activity):
    def __init__(self, **kwargs):
        super(GetActivityMembers, self).__init__(**kwargs)

    def send(self):
        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/activities/{}/members".format(
                                    self.conversation['id'],
                                    self.activityId))

        return self._request(response_url, requests.get)


class UploadAttachmentToChannel(Activity):
    def __init__(self, **kwargs):
        self.encoded_file = kwargs.pop('encoded_file', None)            # Binary data that represents the contents of the thumbnail version of the file.
        self.encoded_thumbnail = kwargs.pop('encoded_thumbnail', None)  # Binary data that represents the contents of the original version of the file.
        self.upload_filename = kwargs.pop('upload_filename', None)      # Name of the attachment.
        self.upload_type = kwargs.pop('upload_type', None)              # ContentType of the attachment.

        upload_file_path = kwargs.pop('upload_file_path', None)
        upload_thumbnail_path = kwargs.pop('upload_thumbnail_path', None)

        if self.encoded_file is None and upload_file_path is not None:
            self.upload_file(upload_file_path, upload_thumbnail_path)

        super(UploadAttachmentToChannel, self).__init__(**kwargs)

    def send(self):
        response_json = {
            'type': self.fromAccount if self.bot is None else self.bot,
            'name': False if self.isGroup is None else self.isGroup,
            'originalBase64': self.encoded_file,
            'thumbnailBase64': self.encoded_thumbnail,
        }

        response_url = self.urljoin(self.serviceUrl,
                                    "/v3/conversations/{}/attachments".format(
                                    self.conversation['id']))

        return self._request(response_url, requests.post, response_json)

    def upload_file(self, filename, thumbnail_filename=None):
        # Upload file
        with open(filename, "rb") as image_file:
            self.encoded_file = base64.b64encode(image_file.read())

        if thumbnail_filename is not None:
            with open(thumbnail_filename, "rb") as image_file:
                self.encoded_thumbnail = base64.b64encode(image_file.read())
