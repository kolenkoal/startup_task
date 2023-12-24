from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from links.models import Link
from links.serializers import LinkDetailSerializer


class UserLinksAPIView(ListAPIView):
    """
    API-представление для получения списка ссылок пользователя.

    Attributes:
    - permission_classes: Устанавливает требуемые разрешения доступа (только аутентифицированным пользователям).
    - serializer_class: Указывает используемый сериализатор для отображения данных.

    Methods:
    - get_queryset(): Возвращает набор ссылок, принадлежащих текущему пользователю.
    - get_serializer_context(): Получает контекст сериализатора с объектом запроса.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = LinkDetailSerializer

    def get_queryset(self):
        """
        Получает набор ссылок, принадлежащих текущему пользователю.

        Returns:
        - QuerySet: Набор ссылок, принадлежащих текущему пользователю.
        """
        user = self.request.user
        return Link.objects.filter(user=user)

    def get_serializer_context(self):
        """
        Получает контекст сериализатора с объектом запроса.

        Returns:
        - dict: Контекст сериализатора с объектом запроса.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
