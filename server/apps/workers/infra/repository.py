from typing import final

from django.db.models import QuerySet
from django.utils import timezone

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
    
    def soft_delete(self, pk: int) -> Worker:
        worker = self.get_by_pk(pk=pk)
        worker.is_active = False
        worker.deleted_at = timezone.now()
        worker.save(update_fields=('is_active', 'updated_at', 'deleted_at'))
        return worker
