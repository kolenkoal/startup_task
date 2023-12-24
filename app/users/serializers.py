from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from .models import User


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password"]


class UserSignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True)  # Ensure password is write-only

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data['password'])  # Hash the password
        return super().create(validated_data)
