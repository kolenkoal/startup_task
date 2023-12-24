from django.contrib import admin
from django.utils import timezone
from .models import Link


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('id', 'url', 'last_accessed')
    actions = ['delete_old_links']

    @admin.action(description="Delete links older than 2 weeks")
    def delete_old_links(self, request, queryset):
        two_weeks_ago = timezone.now() - timezone.timedelta(weeks=2)
        old_links = queryset.filter(last_accessed__lt=two_weeks_ago)
        deleted_count, _ = old_links.delete()
        self.message_user(request, f"Deleted {deleted_count} old links.")
