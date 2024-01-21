# GoLuckyCoreAPI/asgi.py

import os
from django.core.asgi import get_asgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GoLuckyCoreAPI.settings')

# Load Django's ASGI application to handle HTTP requests before importing channels layers
django_asgi_app = get_asgi_application()

# Now we can import the ProtocolTypeRouter and other channels routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from GoLuckyCoreAPI.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    "http": django_asgi_app,  # Ensure Django handles HTTP requests
    "websocket": AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns  # Your WebSocket routing
        )
    ),
})
