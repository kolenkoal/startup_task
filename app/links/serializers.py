from rest_framework import serializers

from .models import Link


class LinkSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Link.

    Attributes:
    - Meta: Метаинформация о сериализаторе, включая модель и поля, которые будут сериализованы.

    Fields:
    - url: Поле URL для сериализации.
    """

    class Meta:
        model = Link
        fields = ("url",)


class LinkDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для детальной информации о модели Link.

    Attributes:
    - shortened_url: Дополнительное поле для сериализации, представляющее укороченный URL.

    Fields:
    - url: Поле URL для сериализации.
    - shortened_url: Поле укороченного URL для сериализации.
    """
    shortened_url = serializers.SerializerMethodField()

    class Meta:
        model = Link
        fields = ("url", "shortened_url")

    def get_shortened_url(self, obj):
        """
        Получает укороченный URL на основе объекта Link.

        Args:
        - obj: Объект Link.

        Returns:
        - str: Укороченный URL, состоящий из домена запроса и идентификатора объекта.
        """
        request = self.context.get('request')
        domain = self._get_request_domain(request)
        return f"{domain}/{obj.id}"

    def _get_request_domain(self, request):
        """
        Получает домен из объекта запроса.

        Args:
        - request: Объект запроса.

        Returns:
        - str: Домен (схема и хост) запроса.
        """
        scheme = request.scheme
        host = request.get_host()
        return f"{scheme}://{host}"
