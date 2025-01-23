from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from api.models import channel
from json import loads

class FRConsumer(WebsocketConsumer):
    def connect(self):
        user = self.scope['user']
        self.grp = f'noti_{user.username}'
        async_to_sync(self.channel_layer.group_add(self.grp, self.channel_name))("frNotifier", self.channel_name)
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard(self.grp, self.channel_name))("frNotifier", self.channel_name)
    
    def receive(self, data):
        jData = loads(data)
        friendRequest = jData["requestID"]

        self.channel_layer.group_send(
            self.channel_name,
            {
                'type': 'notifyFR'
                'requestID': friendRequest,
            }
        )

    def notifyFR(self, event):
        #do stuff
        print()