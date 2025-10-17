import pytest

from server.apps.workers.infra.repository import WorkerRepo
from server.apps.workers.models import Worker
from server.di import resolve
from tests.plugins.workers import WorkerBatchFactory


@pytest.mark.django_db
def test_get_all(worker_batch: WorkerBatchFactory) -> None:
    """Test the `get_all()` method of WorkerRepo."""
    batch_size = 3
    worker_batch(batch_size)

    repo = resolve(WorkerRepo)
    all_collects = repo.get_all()

    assert all_collects.count() == batch_size


@pytest.mark.django_db
def test_get_by_pk(worker: Worker) -> None:
    """Test the `get_by_pk()` method of WorkerRepo."""
    repo = resolve(WorkerRepo)
    worker_obj = repo.get_by_pk(pk=worker.id)

    assert worker_obj == worker


@pytest.mark.django_db
def test_get_by_pk_none() -> None:
    """get_by_pk raises Worker.DoesNotExist if object is missing."""
    repo = resolve(WorkerRepo)
    with pytest.raises(Worker.DoesNotExist):
        repo.get_by_pk(pk=1)


@pytest.mark.django_db
def test_get_all_active_workers(worker: Worker) -> None:
    """Test the `get_all_active()` method of WorkerRepo."""
    repo = resolve(WorkerRepo)
    worker_non_active = worker
    worker_non_active.is_active = False
    all_active_collect = repo.get_all_active()
    all_collect = repo.get_all()

    assert all_collect != all_active_collect


@pytest.mark.django_db
def test_soft_delete_worker(worker: Worker) -> None:
    """Test the `soft_delete()` method of WorkerRepo."""
    repo = resolve(WorkerRepo)
    old_deleted_at = worker.deleted_at
    delete_worker = repo.soft_delete(pk=worker.id)

    assert delete_worker.deleted_at != old_deleted_at
