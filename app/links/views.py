from django.utils import timezone
from django.shortcuts import redirect

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from string import ascii_letters
from random import choice

from .models import Link
from .serializers import LinkSerializer


class LinkCreateAPIView(APIView):
    """
    Создает новую ссылку при выполнении запроса POST.

    Attributes:
    - permission_classes: Устанавливает требуемые разрешения доступа (только аутентифицированным пользователям).
    - serializer_class: Указывает используемый сериализатор для обработки данных.

    Methods:
    - generate_unique_id(): Генерирует уникальный идентификатор заданной длины.
    - post(): Обрабатывает запрос POST для создания новой ссылки.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LinkSerializer

    def generate_unique_id(self, length=8):
        """
        Генерирует уникальный идентификатор заданной длины.

        Args:
        - length (int): Длина уникального идентификатора (по умолчанию 8 символов).

        Returns:
        - str: Уникальный идентификатор заданной длины.
        """
        characters = ascii_letters
        while True:
            unique_id = ''.join(choice(characters) for _ in range(length))
            if not Link.objects.filter(id=unique_id).exists():
                return unique_id

    def post(self, request):
        """
        Создает новую ссылку на основе данных из запроса POST.

        Args:
        - request (HttpRequest): Объект HTTP-запроса с данными для создания ссылки.

        Returns:
        - Response: JSON-ответ с ID созданной ссылки в случае успеха.
                    Возвращает ответ "400 Bad Request" в случае неверных данных.
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            unique_id = self.generate_unique_id()
            link = Link.objects.create(id=unique_id,
                                       user=request.user,
                                       url=request.data["url"])
            return Response({'id': link.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RedirectLinkAPIView(APIView):
    """
    Перенаправляет на соответствующую URL-адресу ссылку по уникальному идентификатору.

    Methods:
    - get(): Обрабатывает запрос GET для перенаправления на соответствующую ссылку.
    """

    def get(self, request, domain):
        """
        Извлекает соответствующую ссылку и перенаправляет на ее URL-адрес.

        Args:
        - request (HttpRequest): Объект HTTP-запроса.
        - domain (str): Уникальный идентификатор ссылки.

        Returns:
        - redirect(): Перенаправление на URL-адрес, связанный с найденной ссылкой.
                    Возвращает ответ "404 Not Found" в случае отсутствия ссылки.
        """
        try:
            link = Link.objects.get(id=domain)
            link.last_accessed = timezone.now()
            link.save(update_fields=['last_accessed'])
            return redirect(link.url)
        except Link.DoesNotExist:
            return Response({'detail': 'Link not found'},
                            status=status.HTTP_404_NOT_FOUND)
