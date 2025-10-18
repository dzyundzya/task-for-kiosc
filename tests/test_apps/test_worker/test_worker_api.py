from http import HTTPStatus

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from server.apps.workers.infra.repository import WorkerRepo
from server.apps.workers.models import Worker
from server.di import resolve
from tests.plugins.workers import WorkerBatchFactory


@pytest.mark.django_db
def test_delete_success(worker: Worker, auth_admin_client: APIClient) -> None:
    """Successfully delete a worker."""
    url = reverse('workers-detail', kwargs={'pk': worker.pk})
    response = auth_admin_client.delete(url, format='json')

    assert response.status_code == HTTPStatus.NO_CONTENT


@pytest.mark.django_db
def test_retrieve_success(worker: Worker, auth_user_client: APIClient) -> None:
    """Test successfully retrieving a single worker."""
    url = reverse('workers-detail', kwargs={'pk': worker.pk})
    response = auth_user_client.get(url, format='json')

    assert response.status_code == HTTPStatus.OK


@pytest.mark.django_db
def test_create_worker(auth_admin_client: APIClient) -> None:
    """Successfully creating a worker returns 201 and correct JSON."""
    url = reverse('workers-list')
    payload = {
        'first_name': 'F Name',
        'middle_name': 'M Name',
        'last_name': 'L Name',
        'email': 'newemail@test.ru',
    }

    response = auth_admin_client.post(url, payload, format='json')
    response_data = response.json()

    assert response.status_code == HTTPStatus.CREATED
    assert response_data['first_name'] == 'F Name'
    assert 'id' in response_data

    worker = Worker.objects.get(id=response_data['id'])
    assert worker.first_name == 'F Name'


@pytest.mark.django_db
def test_email_exists(worker: Worker, auth_admin_client: APIClient) -> None:
    url = reverse('workers-list')
    payload = {
        'first_name': 'F Name',
        'middle_name': 'M Name',
        'last_name': 'L Name',
        'email': 'testtest@test.ru',
    }

    response = auth_admin_client.post(url, payload, format='json')
    assert response.status_code == HTTPStatus.BAD_REQUEST
