from django.shortcuts import render

# Create your views here.
from .models import UserModel
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken,UntypedToken
from drf_spectacular.utils import extend_schema,OpenApiParameter
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import UserSerializer,GoogleUserSerializer,CustomSerializer
from rest_framework.decorators import api_view



class CustomView(TokenObtainPairView):
    serializer_class = CustomSerializer

class UserCreateView(APIView):
    @extend_schema(
            parameters= [
                OpenApiParameter('email',type=str,required=True,description='The email of the user'),
                OpenApiParameter('password',type=str,required=True,description='The password of the user'),
                OpenApiParameter('google_picture',type=str,required=False,description='The url of the user\'s image'),
            ]
    )
    def post(self,request,*args):
        print(f'Data: {request.data}')
        user_serializer = UserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'User has been created successfully'}, 200)
        error = user_serializer.errors
        for attribute,message in error.items():
         response = message[0][0].upper() + message[0][1:]
         return Response({'message': f'{response}'},400)


class GoogleUserCreateView(APIView):
    @extend_schema(
            parameters= [
                OpenApiParameter('email',type=str,required=True,description='The email of the user'),
                OpenApiParameter('sub',type=str,required=True,description='The sub of the user which is in the json from google oauth'),
                OpenApiParameter('google_picture',type=str,required=False,description='The url of the user\'s image from google oauth'),
            ]
    )
    def post(self,request,*args):
        user_serializer = GoogleUserSerializer(data=request.data)

        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'message':'User has been created successfully'}, 200)
        error = user_serializer.errors
        for attribute,message in error.items():
         response = message[0][0].upper() + message[0][1:]
         return Response({'message': f'{response}'},400)



class GetUser(APIView):
    def get(self,request,*args):
        try:
            token = request.headers['Authorization'].replace('Bearer','').replace(' ','')
            decoded_data = UntypedToken(token)
            id = decoded_data.payload['user_id']
            if id:
                user = UserModel.objects.get(id=id)
                user_serializer = UserSerializer(instance=user)
                return Response({'message': user_serializer.data}, 200)
            return Response({'message': 'No user id was provided'}, 400)
        except (InvalidToken, TokenError) as e:
            return Response({"error": str(e)}, 400)
        # if id:
        #     user = UserModel.objects.get(id=id)
        #     user_serializer = UserSerializer(instance=user)
        #     return Response({'message': user_serializer.data}, 200)
        # return Response({'message': 'No user id was provided'}, 400)




