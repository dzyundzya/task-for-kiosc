import logging
from typing import override

from django.contrib import admin
from django.http import HttpRequest

from server.apps.workers.models import Worker

logger = logging.getLogger(__name__)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin[Worker]):
    """Admin configuration for the Worker model."""

    list_display = (
        'last_name',
        'first_name',
        'position',
        'email',
        'is_active',
        'created_at',
    )
    list_filter = ('position', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'position')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'hired_date')

    @override
    def save_model(
        self,
        request: HttpRequest,
        obj: Worker,  # noqa: WPS110
        form: BaseException | None,
        change: bool,
    ) -> None:
        """Set creator on creation and log event."""
        if not change and not obj.created_by and request.user.is_authenticated:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        logger.info('[ADMIN] Worker created by %s: %s', request.user, obj)
