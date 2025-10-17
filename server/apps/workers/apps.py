from django.apps import AppConfig


class WorkersConfig(AppConfig):
    """Configuration class for the Workers application."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'server.apps.workers'
    verbose_name = 'Workers'
