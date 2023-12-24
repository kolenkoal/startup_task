from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSignUpSerializer, UserLoginSerializer


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        """
        Обработка входа пользователя.

        Проверяет предоставленные электронную почту и пароль в данных запроса. Извлекает пользователя по электронной почте
        и проверяет, соответствует ли предоставленный пароль хранимому паролю пользователя. В случае успеха,
        генерирует или извлекает аутентификационный токен пользователя и возвращает его вместе с основной информацией о пользователе.

        Args:
        - request (HttpRequest): Объект HTTP-запроса, содержащий учетные данные для входа.

        Returns:
        - Response: JSON-ответ, содержащий аутентификационный токен пользователя и основную информацию о пользователе,
                    если вход выполнен успешно. Возвращает ответ "404 Not Found" в случае неверной электронной почты
                    или пароля.
        """
        user = get_object_or_404(User, email=request.data["email"])

        if not user.check_password(request.data["password"]):
            return Response({"detail": "Not found."},
                            status=status.HTTP_404_NOT_FOUND)

        token, created = Token.objects.get_or_create(user=user)

        UserSignUpSerializer(instance=user)
        user_data = prepare_user_data(user)

        return Response(
            {"token": token.key, "user": user_data}, status=status.HTTP_200_OK
        )


class SignupAPIView(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        """
        Обработка регистрации пользователя.

        Проверяет предоставленные данные для регистрации пользователя с использованием указанного сериализатора.
        Если данные корректны, создает нового пользователя с предоставленной информацией, генерирует
        аутентификационный токен для пользователя и возвращает токен вместе с основными данными пользователя
        в случае успешной регистрации.

        Args:
        - request (HttpRequest): Объект HTTP-запроса, содержащий данные для регистрации пользователя.

        Returns:
        - Response: JSON-ответ, содержащий аутентификационный токен пользователя и основные данные пользователя
                    в случае успешной регистрации. Возвращает ответ "400 Bad Request" в случае неверных данных
                    для регистрации пользователя.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = Token.objects.create(user=user)
            user_data = prepare_user_data(user)

            return Response(
                {
                    "token": token.key,
                    "user": user_data,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def prepare_user_data(user):
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
