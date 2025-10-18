from typing import override

from django.contrib.auth.models import AbstractUser
from django.db import models

from server.apps.users.choices import RoleType


class CustomUser(AbstractUser):
    """Custom User model that replaces Django's default User."""

    role = models.CharField(
        "User's role",
        choices=RoleType.choices,
        default=RoleType.USER,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'user'
        verbose_name_plural = 'Users'
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_role_valid',
                condition=(models.Q(role__in=RoleType.values)),
            ),
        )

    @override
    def __str__(self) -> str:
        return self.username

    @property
    def is_admin(self) -> bool:
        return self.role in RoleType.ADMIN or self.is_superuser
