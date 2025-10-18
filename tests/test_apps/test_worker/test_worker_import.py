from __future__ import annotations

from http import HTTPStatus

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient

from server.apps.workers.models import Worker
from server.apps.workers.serializers import WorkerImportSerializer
from server.apps.workers.services.import_workers import WorkerImportService


@pytest.mark.django_db
def test_import_from_excel_success(success_excel: SimpleUploadedFile) -> None:
    """Test of successful import of workers from Excel."""
    service = WorkerImportService()
    workers = service.import_from_excel(success_excel)

    assert workers['created'] == 2
    assert workers['errors'] == []
    assert Worker.objects.count() == 2


@pytest.mark.django_db
def test_import_from_excel_with_errors(
    not_success_excel: SimpleUploadedFile,
) -> None:
    """An error handling test during import."""
    service = WorkerImportService()
    workers = service.import_from_excel(not_success_excel)

    assert workers['created'] == 0
    assert len(workers['errors']) == 2
    assert 'Required fields are missin' in str(
        workers['errors'][0]['error']
    ) or 'Incorrect email' in str(workers['errors'][1]['error'])


@pytest.mark.django_db
def test_import_from_excel_duplicate_email(
    worker: Worker, success_excel: SimpleUploadedFile
) -> None:
    """Test duplicate email is not created again."""
    service = WorkerImportService()
    workers = service.import_from_excel(success_excel)

    assert workers['created'] == 1
    assert len(workers['errors']) == 1
    assert 'Email already exists' in workers['errors'][0]['error']


@pytest.mark.django_db
def test_import_from_excel_invalid_file() -> None:
    """Test invalid Excel file."""
    invalid_file = SimpleUploadedFile(
        'not_excel.txt',
        b'not an excel content',
        content_type='text/plain',
    )

    service = WorkerImportService()
    workers = service.import_from_excel(invalid_file)

    assert workers == {
        'created': 0,
        'errors': [{'error': 'Excel file cannot be read.'}],
    }


def test_validate_xl_file_valid() -> None:
    """Verifies .xlsx file is being validated."""
    excel_file = SimpleUploadedFile('test.xlsx', b'dummy content')
    serializer = WorkerImportSerializer(data={'xl_file': excel_file})
    assert serializer.is_valid(), serializer.errors


def test_validate_xl_file_invalid_extension() -> None:
    """Checks that it is not .xlsx file causes ValidationError."""
    not_excel_file = SimpleUploadedFile('test.txt', b'dummy content')
    serializer = WorkerImportSerializer()

    with pytest.raises(
        ValidationError, match=r'File must be in the format .xlsx'
    ):
        serializer.validate_xl_file(not_excel_file)


@pytest.mark.django_db
def test_import_view_no_file(auth_admin_client: APIClient) -> None:
    """Checks that 400 is returned without the file."""
    response = auth_admin_client.post('/api/workers/import/', data={})

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.data == {'error': 'File was not transferred.'}


@pytest.mark.django_db
def test_import_view_with_valid_file(
    auth_admin_client: APIClient, success_excel: SimpleUploadedFile
) -> None:
    """Checks the successful download of the Excel file."""
    response = auth_admin_client.post(
        '/api/workers/import/',
        data={'file': success_excel},
        format='multipart',
    )

    assert response.status_code == HTTPStatus.OK
    assert response.data['created'] == Worker.objects.count()
    assert response.data['errors'] == []
