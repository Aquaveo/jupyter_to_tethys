# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import djangobokeh.routing


application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            djangobokeh.routing.websocket_urlpatterns
        )
    ),
    'http': AuthMiddlewareStack(
        URLRouter(
            djangobokeh.routing.http_urlpatterns
        )
    ),
})