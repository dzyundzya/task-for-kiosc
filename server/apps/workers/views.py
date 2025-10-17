import logging
from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import  serializers, status, viewsets
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.workers.infra.repository import WorkerRepo
from server.apps.workers.models import Worker
from server.apps.workers.permissions import IsAdmibOrReadOnly
from server.apps.workers.serializers import (
    WorkerCreateUpdateSerializer,
    WorkerDetailSerializer,
    WorkerListSerializer,
)
from server.di import resolve


logger = logging.getLogger(__name__)


class WorkerViewSet(viewsets.ModelViewSet[Worker]):  # type: ignore[misc]
    """Viewsets for Worker model."""

    permission_classes = (IsAdmibOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('is_active', 'position')
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_queryset(self) -> QuerySet[Worker]:
        """Get queryset."""
        return self.repo.get_all()
    
    def get_serializer_class(self) -> type[serializers.BaseSerializer[Worker]]:
        """Method for selecting serializer."""
        return {
            'list': WorkerListSerializer,
            'retrieve': WorkerDetailSerializer,
        }.get(self.action, WorkerCreateUpdateSerializer)
    
    def perform_create(self, serializer: WorkerCreateUpdateSerializer) -> None:
        worker = serializer.save(created_by=self.request.user)
        logger.info(
            f'Worker created (id={worker.id}) by user={self.request.user.id}'
        )
    
    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Soft delete a worker."""
        self.repo.soft_delete(pk=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @property
    def repo(self) -> WorkerRepo:
        """Get WorkerRepo instance from dependency container."""
        return resolve(WorkerRepo)
