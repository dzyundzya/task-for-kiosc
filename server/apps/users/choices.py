from django.db import models


class RoleType(models.TextChoices):
    """Choices for type of role."""

    ADMIN = 'admin', 'Admin'
    USER = 'user', 'User'
