from django.db import models

from server.apps.workers.choices import PositionType
from server.common import constants


class TimeStampedModel(models.Model):
    """Abstract model with time shtamps."""

    created_at = models.DateTimeField('Date created', auto_now_add=True)
    updated_at = models.DateTimeField('Date updated', auto_now=True)
    is_active = models.BooleanField('Active', default=True, db_index=True)

    class Meta:
        abstract = True


class Worker(TimeStampedModel):
    """Worker model."""

    first_name = models.CharField(
        'First name',
        max_length=constants.NAME_LENGTH,
    )
    middle_name = models.CharField(
        'Moddle name',
        max_length=constants.NAME_LENGTH,
        blank=True,
    )
    last_name = models.CharField(
        'Last name',
        max_length=constants.NAME_LENGTH,
    )
    email = models.EmailField(
        'E-mail',
        unique=True,
    )
    position = models.CharField(
        'Position',
        choices=PositionType.choices,
        default=PositionType.OTHER,
        db_index=True,
    )
    hired_date = models.DateField('Date of employment', auto_now_add=True)
    created_by = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='workers',
        verbose_name='User created the employee record',
    )
    deleted_at = models.DateTimeField('Date deleted', blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)
        indexes = (
            models.Index(fields=['email']),
            models.Index(fields=['position']),
            models.Index(fields=['is_active']),
        )
        constraints = (
            models.CheckConstraint(
                name='%(app_label)s_%(class)s_position_valid',
                condition=(models.Q(position__in=PositionType.values)),
            ),
        )

    def __str__(self) -> str:
        """Return a human-readable string representation of the worker."""
        return f'{self.last_name} {self.first_name} ({self.position})'
