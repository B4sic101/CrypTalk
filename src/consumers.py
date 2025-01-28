from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from api.models import friendRequest
from api.models import User
import json

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
    
    def receive(self, text_data):
        print(f"{text_data}")
        jData = json.loads(text_data)
        reqID = jData["requestID"]
        receiverUserID = friendRequest.objects.filter(requestID=reqID).values("receiver")[0]["receiver"]
        senderUserID = friendRequest.objects.filter(requestID=reqID).values("sender")[0]["sender"]
        sender = User.objects.filter(username=senderUserID).values("username")[0]["username"]
        targetGrp = f'noti_{receiverUserID}'
        receiver = User.objects.filter(userID=receiverUserID).values("username")[0]["username"]

        # Truth table variables
        print(f"""------------- TRUTH TABLE -------------
                        Target Group: {targetGrp}
                        Receiver: {receiver}
                        Sender: {sender}
              ---------------- Outputs ---------------""")

        try:
            async_to_sync(
                self.channel_layer.group_send(
                targetGrp,
                {
                    'type': 'frNotifier',
                    'requestID': reqID,
                    'sender': sender
                }
                )
            )
            print("Succesfully sent message to group")
        except Exception:
            print("User not online")

    def frNotifier(self, textData):
        reqID = textData['requestID']
        sender = textData['sender']

        async_to_sync(self.send(textData=json.dumps({
            'requestID':reqID,
            'senderUsername': sender
        })))


