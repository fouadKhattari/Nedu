import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import users.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EasyWay.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            users.routing.websocket_urlpatterns,
        )
    ),
})