from django.urls import path
from src.consumers import FRConsumer, ChatConsumer

websocket_urlpatterns = {
    path('ws/notifyFR/', FRConsumer.as_asgi()),
    path('ws/chat/', ChatConsumer.as_asgi()),
}

