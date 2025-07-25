import json, requests
from urllib.parse import parse_qs
from rest_framework_simplejwt.tokens import AccessToken
from authenticate_service.models import UserModel
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from .model_function import generate_followup_question

API_URL = "https://api-inference.huggingface.co/models/uwanaa/greendale"
HEADERS = {"Authorization": "Bearer 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"}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = parse_qs(self.scope["query_string"].decode())
        token = query_string.get("token", [None])[0]
    

        if token:
            try:
                decoded_token = AccessToken(token)
                self.user = await sync_to_async(UserModel.objects.get)(id=decoded_token["user_id"]) 
                await self.accept()

                # self.model = await sync_to_async(T5ForConditionalGeneration.from_pretrained('chatbot/checkpoint-132',ignore_mismatched_sizes=True))
                # self.tokenizer = await sync_to_async(T5Tokenizer.from_pretrained('chatbot/checkpoint-132'))

                await self.send(json.dumps({"message": "WebSocket connection successful"}))
            except Exception as e:
                await self.accept()
                await self.send(json.dumps({"error": str(e)}))  # Send error instead of closing immediately
                await self.close()
        else:
            await self.accept()
            await self.send(json.dumps({"error": "No token provided"}))
            await self.close()
        


    async def disconnect(self, close_code):
        print(f"WebSocket Disconnected with code: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message", "")

        if message.lower() == 'hi':
            await self.send(json.dumps({"message": "Hi, I am Greendale Chatbot"}))
            return
        # followup = generate_followup_question(message)
        # print(message)
        # print(followup)

        # # If it's a follow-up, return it directly
        # if "Could you" in followup or "Do you" in followup:
        #     return followup

        # # If the chatbot is confident, let it generate advice
        input_text = f"Suggest advice for: {message}"
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": input_text})
        if response:
         model_response = response.json()[0]["generated_text"]
        print(response)
        model_response = response.json()[0]["generated_text"]
        await self.send(json.dumps({"message": model_response}))
