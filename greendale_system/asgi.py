# import os,django
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter, URLRouter
# from chatbot.routing import websocket_urlpatterns

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'greendale_system.settings')
# django.setup()

# application = ProtocolTypeRouter({
#     "http": get_asgi_application(),  # Handles HTTP requests
#     "websocket": URLRouter(websocket_urlpatterns),  # WebSocket routing
# })
