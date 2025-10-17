from django.db import models


class PositionType(models.TextChoices):
    """Choices for type of position."""

    GUARD = 'guard', 'Guard'
    CLEANER = 'cleaner', 'Cleaner'
    ENGINEER = 'engineer', 'Engineer'
    MANAGER = 'manager', 'Manager'
    OTHER = 'other', 'Other'
