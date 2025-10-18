import pytest

from server.apps.workers.models import Worker


@pytest.mark.django_db
def test_str_method_collect(worker: Worker) -> None:
    """Test string representation of Worker."""
    assert (
        str(worker)
        == f'{worker.last_name} {worker.first_name} ({worker.position})'
    )
