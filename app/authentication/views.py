from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import UserSignUpSerializer

from users.serializers import UserLoginSerializer


class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        user = get_object_or_404(User, email=request.data["email"])
        if not user.check_password(request.data["password"]):
            return Response({"detail": "Not found."},
                            status=status.HTTP_404_NOT_FOUND)
        token, created = Token.objects.get_or_create(user=user)
        UserSignUpSerializer(instance=user)
        user_data = {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }

        return Response(
            {"token": token.key, "user": user_data}, status=status.HTTP_200_OK
        )


class SignupAPIView(APIView):
    serializer_class = UserSignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            token = Token.objects.create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
