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
            self.group_name = f'noti_{user.userID}'
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            print(f"---- {user.username} with a userID of {user.userID} is in the group {self.group_name}.")
            self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
    
    def receive(self, text_data):
        print(f"{text_data}")
        jData = json.loads(text_data)
        reqID = jData["requestID"]
        friend_request = friendRequest.objects.get(requestID=reqID)
        receiver_user_id = friend_request.receiver
        receiver = User.objects.get(userID=receiver_user_id).username
        sender_user_id = friend_request.sender
        sender = User.objects.get(userID=sender_user_id).username
        targetGrp = f'noti_{receiver_user_id}'

        # Truth table variables
        print(f"""------------- TRUTH TABLE -------------
        Target Group: {targetGrp}
        Receiver: {receiver}
        Sender: {sender}
        Own Group Name: {self.group_name}
---------------- OUTPUTS ---------------""")

        try:
            print("Sending to..." + targetGrp)
            async_to_sync(
                self.channel_layer.group_send)(
                targetGrp,
                {
                    'type': 'fr.notifier',
                    'requestID': reqID,
                    'sender': sender,
                    'senderID': str(sender_user_id)
                }
                )
            print("Succesfully sent message to group")
        except Exception as e:
            print(f"ERROR: {e}")

    def fr_notifier(self, text_data):
        print("Fr Notifier has been called")
        try:
            async_to_sync(self.send(text_data=json.dumps(text_data)))
            print("Friend request notification sent")
        except Exception as e:
            print(f"ERROR: {e}")