from django.urls import path
from .views import MessageAPIView, FetchMessagesAPIView,FetchConversationsAPIView

urlpatterns = [
    path('conversations/', FetchConversationsAPIView.as_view(), name='send-message'),
    path('send-message/', MessageAPIView.as_view(), name='send-message'),
    path('send-message/<str:conversation_id>/', MessageAPIView.as_view(), name='send-message'),
    path('fetch-messages/<str:conversation_id>/', FetchMessagesAPIView.as_view(), name='fetch-messages'),
]