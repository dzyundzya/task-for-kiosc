from __future__ import annotations

from collections.abc import Callable
from datetime import datetime, timedelta
from decimal import Decimal
from typing import TYPE_CHECKING, TypedDict, Unpack

import pytest
from django.utils import timezone

from server.apps.workers.choices import PositionType
from server.apps.workers.models import Worker
from server.apps.users.models import CustomUser

if TYPE_CHECKING:
    from tests.plugins.fakery import FakeryM

type WorkerFactory = Callable[[Unpack[_WorkerFactoryParams]], Worker]

type WorkerBatchFactory = Callable[[int], list[Worker]]


class _WorkerFactoryParams(TypedDict, total=False):
    """Base params for WorkerFactory."""

    first_name: str
    middle_name: str
    last_name: str
    email: str
    created_by: CustomUser


@pytest.fixture
def worker_factory(fakery_m: FakeryM[Worker]) -> WorkerFactory:
    """Return a factory to create Worker instances with custom fields."""

    def factory(**kwargs: Unpack[_WorkerFactoryParams]) -> Worker:
        return fakery_m(Worker)(**kwargs)

    return factory


@pytest.fixture
def worker(worker_factory: WorkerFactory, auth_admin: CustomUser) -> Worker:
    """Return a single Worker instance created."""
    return worker_factory(
        first_name='Test first name',
        middle_name='Test middle name',
        last_name='Test last name',
        email='testtest@test.ru',
        created_by=auth_admin,
    )


@pytest.fixture
def worker_batch(worker_factory: WorkerFactory, auth_admin: CustomUser) -> WorkerBatchFactory:
    """Return a factory that creates `batch_size` Worker instances."""

    def factory(batch_size: int) -> list[Worker]:
        return [
            worker_factory(
                first_name=f'Test first name {worker_number}',
                last_name=f'Test last name {worker_number}',
                email=f'test{worker_number}@test.ru',
            )
            for worker_number in range(batch_size)
        ]
    return factory
