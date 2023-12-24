from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "last_login",
        "is_admin",
        "is_staff",
    )
    search_fields = ["email"]
    readonly_fields = (
        "id",
        "last_login",
    )

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ["id"]


admin.site.register(User, UserAdmin)
