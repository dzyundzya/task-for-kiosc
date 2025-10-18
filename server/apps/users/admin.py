from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from server.apps.users.models import CustomUser

FIELDS = 'fields'


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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
        (None, {FIELDS: ('username', 'password')}),
        ('Personal info', {FIELDS: ('first_name', 'last_name', 'email')}),
        (
            'Permissions',
            {
                FIELDS: (
                    'role',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        ('Important dates', {FIELDS: ('last_login', 'date_joined')}),
    )

    ordering = ('id',)
