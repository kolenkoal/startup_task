from django.contrib import admin
from django.utils import timezone

from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Панель админа для модели Link.

    Attributes:
    - list_display: Отображаемые поля при просмотре списка объектов в административной панели.
    - actions: Доступные действия для выбранных объектов в административной панели.

    Methods:
    - delete_old_links(): Метод, позволяющий удалять ссылки, которые не активировались более 2 недель.
    """
    list_display = ('id', 'url', 'last_accessed')
    actions = ['delete_old_links']

    @admin.action(description="Delete links older than 2 weeks")
    def delete_old_links(self, request, queryset):
        """
        Удаляет ссылки, которые не активировались более 2 недель.

        Args:
        - request: Объект запроса от администратора.
        - queryset: Выбранные объекты, на которых будет выполнено действие.

        Returns:
        - message_user(): Уведомление администратору о количестве удаленных старых ссылок.
        """
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=2)
        old_links = queryset.filter(last_accessed__lt=two_weeks_ago)
        deleted_count, _ = old_links.delete()
        self.message_user(request, f"Deleted {deleted_count} old links.")
