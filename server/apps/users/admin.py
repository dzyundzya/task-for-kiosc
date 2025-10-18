from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):  # type: ignore[type-arg]
    """Admin interface for CustomUser."""

    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'is_superuser',
    )

    list_filter = (
        'is_active',
        'role',
    )
    search_fields = (
        'username',
        'email',
        'first_name',
        'last_name',
    )
    readonly_fields = ('last_login', 'date_joined')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),  # noqa: WPS226
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        (
            'Permissions',
            {
                'fields': (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),  # noqa: WPS226
    )

    ordering = ('id',)
