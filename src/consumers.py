from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from api.models import friendRequest, chat, ChatLine
from src.models import User
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
            self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)
    
    def receive(self, text_data):
        jData = json.loads(text_data)

        if jData["type"] == "sendFR":
            reqID = jData["requestID"]
            friend_request = friendRequest.objects.get(requestID=reqID)
            receiver_user_id = friend_request.receiver
            sender_user_id = friend_request.sender
            sender = User.objects.get(userID=sender_user_id).username
            targetGrp = f'noti_{receiver_user_id}'

            try:
                async_to_sync(
                    self.channel_layer.group_send)(
                    targetGrp,
                    {
                        'type': 'fr.notifier',
                        'requestID': reqID,
                        'sender': sender,
                        'senderID': str(sender_user_id),
                    }
                    )
                print("Succesfully sent message to group")
            except Exception as e:
                print(f"ERROR: {e}")

    def fr_notifier(self, text_data):
        try:
            async_to_sync(self.send(text_data=json.dumps(text_data)))
            print("Friend request notification sent")
        except Exception as e:
            print(f"ERROR: {e}")


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # Accept the connection
            user = self.scope['user']
            self.group_name = f'user_{user.userID}'
            async_to_sync(self.channel_layer.group_add)(self.group_name, self.channel_name)
            self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(self.group_name, self.channel_name)

    def receive(self, text_data):
        jData = json.loads(text_data)

        if jData["type"] == "createChat":
            # check if the chat exists?
            chatID = jData["chatID"]
            fetchedChat = chat.objects.get(chatID=chatID)
            userid_to_send = fetchedChat.sender
            receiver_user_id = fetchedChat.receiver
            crypt_key = fetchedChat.crypt_key
            iv = fetchedChat.iv
            receiverUsername = User.objects.get(userID=receiver_user_id).username

            
            targetGrp = f'user_{userid_to_send}'

            try:
                async_to_sync(
                    self.channel_layer.group_send)(
                    targetGrp,
                    {
                        'type': 'chat.create',
                        'chatID': chatID,
                        'username': receiverUsername,
                        'sender': str(receiver_user_id),
                        'crypt_key': crypt_key,
                        'iv': iv
                    }
                    )
                print("Succesfully sent message to group")
            except Exception as e:
                print(f"ERROR: {e}")
        elif jData["type"] == "sendMsg":
            sendingUser = self.scope["user"].userID

            print("t1")
            if chat.objects.filter(chatID=jData["chatID"]).exists():
                chatToSend = chat.objects.get(chatID=jData["chatID"])
                print("t2")

                if chatToSend.sender == sendingUser or chatToSend.receiver == sendingUser:
                    print("t3")
                    targetGrp = ''
                    if chatToSend.sender == sendingUser:
                        targetGrp = f'user_{chatToSend.receiver}'
                    else:
                        targetGrp = f'user_{chatToSend.sender}'
                    print(f"t4: {targetGrp}")

                    message = ChatLine.objects.create(chatID=chatToSend.chatID, sender=sendingUser, content=jData['cipher_text'])

                    try:
                        async_to_sync(
                            self.channel_layer.group_send)(
                            targetGrp,
                            {
                                'type': 'chat.send.message',
                                'chatID': f'{message.chatID}',
                                'cipher_text': f'{message.content}',
                            }
                            )
                        print("Succesfully sent message to group")
                    except Exception as e:
                        print(f"ERROR: {e}")

            
    def chat_create(self, text_data):
        try:
            async_to_sync(self.send(text_data=json.dumps(text_data)))
            print("Chat updated on receiving user's end")
        except Exception as e:
            print(f"ERROR: {e}")
        
    def chat_send_message(self, text_data):
        try:
            async_to_sync(self.send(text_data=json.dumps(text_data)))
            print(f"Sent message to user {self.scope["user"].username}")
        except Exception as e:
            print(f"ERROR: {e}")