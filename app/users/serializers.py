from django.contrib.auth.hashers import make_password

from rest_framework import serializers

from .models import User


class UserLoginSerializer(serializers.ModelSerializer):
    """
    Сериализатор для входа пользователя.

    Attributes:
    - Meta: Определяет модель и поля, которые будут использоваться для сериализации.

    """

    class Meta:
        model = User
        fields = ["id", "email", "password"]


class UserSignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор для регистрации пользователя.

    Attributes:
    - password: Поле для хранения пароля (не отображается при сериализации).

    Methods:
    - create(): Создает пользователя, хешируя предоставленный пароль перед сохранением.
    """
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        """
        Создает пользователя, хешируя предоставленный пароль перед сохранением.

        Args:
        - validated_data (dict): Проверенные и валидированные данные для создания пользователя.

        Returns:
        - User: Созданный пользователь.
        """
        validated_data['password'] = make_password(
            validated_data['password'])
        return super().create(validated_data)
