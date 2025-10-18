import logging
from typing import Any

from django.db.models import QuerySet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, views, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
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
from server.apps.workers.services.import_workers import WorkerImportService
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
        return self.repo.get_all_active()

    def get_serializer_class(self) -> type[serializers.BaseSerializer[Worker]]:
        """Method for selecting serializer."""
        return {
            'list': WorkerListSerializer,
            'retrieve': WorkerDetailSerializer,
        }.get(self.action, WorkerCreateUpdateSerializer)

    def perform_create(self, serializer: WorkerCreateUpdateSerializer) -> None:
        """Save a new Worker instance and log the creation event."""
        worker = serializer.save(created_by=self.request.user)
        logger.info(
            'Worker created (id=%s) by user={%s}',
            worker.id,
            self.request.user.id,
        )

    def destroy(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Soft delete a worker."""
        self.repo.soft_delete(pk=kwargs['pk'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @property
    def repo(self) -> WorkerRepo:
        """Get WorkerRepo instance from dependency container."""
        return resolve(WorkerRepo)


class WorkerImportView(views.APIView):  # type: ignore[misc]
    """Importing workers from Excel."""

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (IsAdmibOrReadOnly,)

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Post request to import workers from the uploaded Excel file."""
        excel_file = request.FILES.get('file')
        if not excel_file:
            return Response(
                {'error': 'File was not transferred.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = WorkerImportService()
        added_workers = service.import_from_excel(excel_file)

        return Response(added_workers, status=status.HTTP_200_OK)
