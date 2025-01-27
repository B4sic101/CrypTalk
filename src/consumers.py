from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from api.models import friendRequest
from api.models import User
from json import loads, dumps

class FRConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # Accept the connection
            user = self.scope['user']
            self.grp = f'noti_{user.userID}'

            async_to_sync(self.channel_layer.group_add(self.grp, self.channel_name))
            self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard(self.grp, self.channel_name))
    
    def receive(self, data):
        jData = loads(data)
        reqID = jData["requestID"]
        receiverUserID = friendRequest.objects.filter(requestID=reqID).values("receiver")[0]
        senderUserID = friendRequest.objects.filter(requestID=reqID).values("sender")[0]
        sender = User.objects.filter(username=senderUserID).values("username")[0]
        targetGrp = f'noti_{receiverUserID}'

        try:
            async_to_sync(
                self.channel_layer.group_send(
                targetGrp,
                {
                    'type': 'notifyFR',
                    'requestID': reqID,
                    'sender': sender
                }
                )
            )
        except Exception:
            print("User not online")

    def notifyUser(self, textData):
        reqID = textData['requestID']
        sender = textData['sender']

        async_to_sync(self.send(textData=dumps({
            'requestID':reqID,
            'senderUsername': sender
        })))