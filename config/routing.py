from django.urls import path

from mazugumzo.chats.consumers import ChatConsumer

websocket_urlpatterns = [
    path("", ChatConsumer.as_asgi)
]