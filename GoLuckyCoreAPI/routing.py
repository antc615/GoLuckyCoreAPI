# GoLuckyCoreAPI/routing.py

from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from apps.chat.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<str:other_user_id>/', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
