from channels.generic.websocket import WebsocketConsumer

class FRConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()