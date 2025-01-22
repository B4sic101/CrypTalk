from django.urls import path
from src.consumers import FRConsumer

websocket_urlpatterns = {
    path("ws/friendrequest/<requestID>", FRConsumer.as_asgi()),
}