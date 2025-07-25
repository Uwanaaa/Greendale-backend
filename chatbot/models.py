from django.db import models
from authenticate_service.models import UserModel 

class Conversation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Conversation {self.id}'

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.CharField(max_length=255, default='AI Chatbot')  
    receiver = models.ForeignKey(UserModel, related_name='received_messages', on_delete=models.CASCADE)
    audio_url = models.FileField(upload_to='audios/',default=None,blank=True,null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver.username} at {self.timestamp}'
