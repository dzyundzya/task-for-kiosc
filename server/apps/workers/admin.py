import logging

from django.contrib import admin
from server.apps.workers.models import Worker


logger = logging.getLogger(__name__)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin[Worker]):
    list_display = (
        'id', 
        'last_name', 
        'first_name', 
        'position', 
        'email', 
        'is_active', 
        'created_at'
    )
    list_filter = ('position', 'is_active', 'created_at')
    search_fields = ('first_name', 'last_name', 'email', 'position')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at', 'hired_date')

    def save_model(self, request, obj, form, change):
        if not obj.created_by and request.user and request.user.is_authenticated:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        if not change:
            logger.info(f'[ADMIN] Worker created by {request.user}: {obj}')
