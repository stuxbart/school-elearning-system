from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_index', 'full_name', 'email', "is_teacher",
                  'is_staff', 'is_admin']


class SnippetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['full_name', 'email']


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'password']
        extra_kwargs = {
            'passowrd': {'write_only': True}
        }

    def create(self, validated_data):
        if 'email' not in validated_data:
            raise serializers.ValidationError("Email is required")
        if 'password' not in validated_data:
            raise serializers.ValidationError("You have to set password")

        user = User.objects.create_user(
            **validated_data
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user:
            return user
        raise serializers.ValidationError("Incorrect Login or Password")
