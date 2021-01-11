from rest_framework import serializers
from .models import User, UserProfile, Client
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings


class ChoicesField(serializers.Field):
    def __init__(self, choices, **kwargs):
        self._choices = choices
        super(ChoicesField, self).__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        return getattr(self._choices, data)

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fileds = ('first_name', 'last_name')
        exclude = (['user'])

class UserRegistrationSerializer(serializers.ModelSerializer):
    profile = UserSerializer(required=False)

    class Meta:
        model = User
        fields = ('email', 'password', 'profile')
        exclude = ()
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(
            user=user,
            first_name=profile_data['first_name'],
            last_name=profile_data['last_name']
        )
        return user

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class UserLoginSerializer(serializers.Serializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Not found.'
            )
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'Not exists'
            )
        return {
            'email':user.email,
            'token': jwt_token
        }

class ClientSerializer(serializers.ModelSerializer):
        # repeat = ChoicesField(choices = Client.repeat_choice)
        # shift = ChoicesField(choices = Client.shift_option)
        # day = ChoicesField(choices = Client.day_option)
        class Meta:
            model = Client
            fields = ['client_user','start_date','arrival_time', 'departure_time','repeat','shift_available','day']
            exclude = ()
        
        def create(self, validated_data):
            return Client.objects.create(**validated_data)

class Client2Serializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('client_user','start_date','arrival_time', 'departure_time','repeat','shift_available','day')