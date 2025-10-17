from typing import final

from django.db.models import QuerySet

from server.apps.workers.models import Worker


@final
class WorkerRepo:
    """Repository for Collect model."""

    def get_all(self) -> QuerySet[Worker]:
        """Returns all worker options from DB."""
        return Worker.objects.select_related('created_by').all()

    def get_all_active(self) -> QuerySet[Worker]:
        """Returns all is_active worker options from DB."""
        return self.get_all().filter(is_active=True)

    def get_by_pk(self, pk: int) -> Worker:
        """Returns one worker option from DB by pk."""
        return self.get_all().get(pk=pk)
