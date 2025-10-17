from django.db.models import QuerySet
from rest_framework import  serializers, status, viewsets

from server.apps.workers.infra.repository import WorkerRepo
from server.apps.workers.models import Worker
from server.apps.workers.permissions import IsAdmibOrReadOnly
from server.apps.workers.serializers import (
    WorkerDetailSerializer,
    WorkerListSerializer,
)
from server.di import resolve

class WorkerViewSet(viewsets.ModelViewSet[Worker]):  # type: ignore[misc]
    """Viewsets for Worker model."""

    permission_classes = (IsAdmibOrReadOnly,)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self) -> QuerySet[Worker]:
        """Get queryset."""
        return self.repo.get_all_active()
    
    def get_serializer_class(self) -> type[serializers.BaseSerializer[Worker]]:
        """Method for selecting serializer."""
        return {
            'retrieve': WorkerDetailSerializer,
        }.get(self.action, WorkerListSerializer)
    
    @property
    def repo(self) -> WorkerRepo:
        """Get WorkerRepo instance from dependency container."""
        return resolve(WorkerRepo)
