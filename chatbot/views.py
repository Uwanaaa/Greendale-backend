# from rest_framework.views import APIView
# from .models import Conversation, Message  # Import the Conversation model
# from rest_framework.response import Response
# from rest_framework import status
# from huggingface_hub import InferenceClient
# from .models import Message
# import redis,random
# import requests


# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

# from rest_framework.permissions import IsAuthenticated

# class MessageAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def post(self, request,conversation_id=None):
#         user_question = request.data.get('question')
#         # if not request.user.is_authenticated:
#         #     return Response({'response': 'Oops. It looks like you are not logged in'}, status=status.HTTP_403_FORBIDDEN)
#         # print(f'User: {request.headers}')        
        
#         if conversation_id:
#             conversation = Conversation.objects.get(id=conversation_id)
#         conversation = Conversation.objects.create()

#         possible_starters = ['hi','hey','hello']
#         replies = [
#             'Hi! How can I help you today?',
#             'Hey! What can I do for you?',
#             'Hello! What issue do you need help with?',
#             'Good day fellow farmer',
#             'Hi, I am GreenDale your helpful chatbot'
#         ]
        
        
#         if user_question.lower() in possible_starters:
#             response = random.sample(replies, 1)
            
#             message = Message.objects.create(
#                 sender='AI Chatbot',
#                 receiver=request.user,
#                 content=response[0],  
#                 conversation=conversation
#             )
#             return Response({'response': response,'conversation_id':conversation.id}, status=status.HTTP_200_OK)
#         try:
#             client = InferenceClient(
#             provider="hf-inference",
#             api_key="#",
#             )

#             messages = [
#                 {
#                     "role": "user",
#                     "content": user_question,
#                 }
#             ]

#             completion = client.chat.completions.create(
#                 model="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
#                 messages=messages, 
#                 max_tokens=500,
#             )
#             ai_response = completion.choices[0].message
            
#             if ai_response:
#                 model_response = completion.choices[0].message

    
                
#                 message = Message.objects.create(
#                     sender='AI Chatbot',
#                     receiver=request.user,  
#                     content=user_question,
#                     conversation=conversation  
#                 )
            
#                 # redis_client.set(f'latest_message_{request.user.id}', model_response)
                
#                 return Response({'response': model_response.content,'id':message.id,'conversation_id':conversation.id}, status=status.HTTP_200_OK)
#             else:
#              return Response({'error': 'Failed to get response from AI model'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#         except Exception as e:
#             print(f'Error: {e}')
#             return Response({'response':'There was an error when parsing the request. Please try again.'}, status=status.HTTP_200_OK)
        

# class FetchMessagesAPIView(APIView):
#     def get(self, request, conversation_id):
#         messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
#         message_data = [{'sender': msg.sender, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
#         return Response(message_data, status=status.HTTP_200_OK)



from rest_framework.views import APIView
from .models import Conversation, Message
from rest_framework.response import Response
from rest_framework import status
from huggingface_hub import InferenceClient
import redis, random,io,os,torch,torchaudio
from django.core.files.base import ContentFile
# from transformers import AutoModelForTextToSpeech, AutoTokenizer
# from django.conf import settings
from .models import Message

# redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)
# from rest_framework.permissions import IsAuthenticated

# model_name = "saheedniyi02/yarngpt"
# device = "cuda" if torch.cuda.is_available() else "cpu"
# model = AutoModelForTextToSpeech.from_pretrained(model_name).to(device)
# tokenizer = AutoTokenizer.from_pretrained(model_name)

class MessageAPIView(APIView):
    def post(self, request, conversation_id=None):
        user_question = request.data.get('question')
        
        if conversation_id:
            conversation, created = Conversation.objects.get_or_create(id=conversation_id)
        else:
            conversation = Conversation.objects.create()
        
        possible_starters = ['hi', 'hey', 'hello']
        replies = [
            'Hi! How can I help you today?',
            'Hey! What can I do for you?',
            'Hello! What issue do you need help with?',
            'Good day fellow farmer',
            'Hi, I am GreenDale your helpful chatbot'
        ]
        
        if user_question.lower() in possible_starters:
            response = random.choice(replies)
            Message.objects.create(
                sender='AI Chatbot',
                receiver=request.user,
                content=response,
                conversation=conversation
            )
            return Response({'response': response, 'conversation_id': conversation.id}, status=status.HTTP_200_OK)
        
        try:
            client = InferenceClient("TinyLlama/TinyLlama-1.1B-Chat-v1.0", token="#")

            prompt = f"<|user|>\n{user_question}\n<|assistant|>\n"
            ai_response = client.text_generation(
                prompt=prompt,
                max_new_tokens=500,
                temperature=0.7,
            )

            # Save messages as before
            Message.objects.create(
                sender='user',
                receiver=request.user,
                content=user_question,
                conversation=conversation
            )
            
            message = Message.objects.create(
                sender='AI Chatbot',
                receiver=request.user,
                content=ai_response,
                conversation=conversation
            )
    
            
            return Response({'response': ai_response, 'conversation_id': conversation.id},status=status.HTTP_200_OK)
        except Exception as e:
            print(f'Error: {e} ')
            return Response({'response': 'There was an error processing your request.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FetchConversationsAPIView(APIView):
    def get(self, request):
        conversations = Conversation.objects.filter(messages__receiver=request.user.id).distinct()
        conversation_data = [
            {
                'id': conv.id,
                'last_message': conv.messages.order_by('-timestamp').first().content if conv.messages.exists() else ''
            } 
            for conv in conversations
        ]
        return Response(conversation_data, status=status.HTTP_200_OK)

class FetchMessagesAPIView(APIView):
    def get(self, request, conversation_id):
        messages = Message.objects.filter(conversation_id=conversation_id).order_by('timestamp')
        message_data = [{'sender': msg.sender, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]
        return Response(message_data, status=status.HTTP_200_OK)
