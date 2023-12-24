from django.db import models

from users.models import User


class Link(models.Model):
    """
    Модель представляет собой ссылку с информацией о ее доступе.

    Attributes:
    - id (str): Уникальный идентификатор ссылки (максимальная длина - 8 символов).
    - last_accessed (DateTimeField): Дата и время последнего доступа к ссылке (автоматически обновляется при изменении).
    - user (ForeignKey): Связь с моделью пользователя (пользователь, связанный с данной ссылкой).
    - url (URLField): URL-адрес ссылки (максимальная длина - 200 символов).

    Methods:
    - __str__(): Возвращает строковое представление уникального идентификатора ссылки.
        """
    id = models.CharField(max_length=8, unique=True, primary_key=True)
    last_accessed = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.id
