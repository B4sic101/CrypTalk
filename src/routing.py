from django.urls import path
from src.consumers import FRConsumer

websocket_urlpatterns = {
    path('ws/notifyFR/', FRConsumer.as_asgi()),
}