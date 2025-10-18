import logging

import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from server.apps.users.models import CustomUser
from server.apps.workers.admin import WorkerAdmin
from server.apps.workers.models import Worker


@pytest.mark.django_db
def test_admin_save_model_logs_creation(
    auth_admin: CustomUser,
    caplog: pytest.LogCaptureFixture,
) -> None:
    """Test that WorkerAdmin.save_model logs creation and sets created_by."""
    site = AdminSite()
    admin = WorkerAdmin(Worker, site)
    request = RequestFactory().get('/')
    request.user = auth_admin

    worker = Worker(
        first_name='John',
        last_name='Doe',
        email='john.doe@test.ru',
    )

    caplog.set_level(logging.INFO)

    admin.save_model(request, worker, form=None, change=False)

    assert worker.created_by == auth_admin


@pytest.mark.django_db
def test_save_model_preserves_creator(
    auth_admin: CustomUser, worker: Worker
) -> None:
    site = AdminSite()
    admin = WorkerAdmin(Worker, site)
    request = RequestFactory().get('/')
    request.user = auth_admin

    old_creator = worker.created_by
    admin.save_model(request, worker, form=None, change=True)

    assert worker.created_by == old_creator
