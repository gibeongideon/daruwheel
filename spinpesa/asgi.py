"""
ASGI config for spinpesa project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

# import os

# from django.core.asgi import get_asgi_application
# # from channels.http import AsgiHandler#
# from channels.routing import ProtocolTypeRouter

# # import django ##


# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spinpesa.settings')
# # django.setup()

# application =  ProtocolTypeRouter({
#     'http':get_asgi_application(),  # AsgiHandler(),#
    
#     }
# )


import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "spinpesa.settings")

application = ProtocolTypeRouter({
  "http": get_asgi_application(),
  "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})