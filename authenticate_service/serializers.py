from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import UserModel



class UserData(serializers.Serializer):
    class Meta:
        model = UserModel
        fields = ['email','first_name','last_name','password','mobile_number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','email','password','picture_url','first_name','last_name','mobile_number']
        extra_kwargs = {
            "password": {"write_only": True},
            "id": {"read_only": True}
            }

        def create(self,validated_data):
            validated_data['password'] = make_password(validated_data['password'])
            user = UserModel.objects.create(**validated_data)
            return user

class GoogleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['id','email','first_name','last_name','sub','google_picture']
        extra_kwargs = {
            "sub": {"write_only":True},
            "id": {"read_only": True}
            }

        def create(self,validated_data):
            user = UserModel.objects.create(**validated_data)
            return user 

class CustomSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(required=False,allow_blank=True)
        self.fields['sub'] = serializers.CharField(required=False,allow_blank=True)

    def validate(self, attrs):
        print(f'Data: {attrs} ')
        if 'password' not in attrs:
            sub_field = attrs.get('sub')

            if not sub_field:
                raise AuthenticationFailed('No password or sub value was provided')
            
            try:
                user = UserModel.objects.get(sub=sub_field)
            except UserModel.DoesNotExist:
                    raise AuthenticationFailed('This user does not exist')
            
            if not user.is_active:
                raise AuthenticationFailed('This user is inactive')
            
            token = RefreshToken.for_user(user)

            return {
                'refresh': str(token),
                'access': str(token.access_token),
            }
        print('This is it ')
        data = super().validate(attrs)
        return data