from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, TypedDict, Unpack

import pytest
from rest_framework.test import APIClient

from server.apps.users.models import CustomUser

if TYPE_CHECKING:
    from tests.plugins.fakery import FakeryM

type UserFactory = Callable[[Unpack[_UserFactoryParams]], CustomUser]

type UserBatchFactory = Callable[[int], list[CustomUser]]


class _UserFactoryParams(TypedDict, total=False):
    """Base params for UserFactory."""

    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    is_active: bool
    role: str


@pytest.fixture
def user_factory(fakery_m: FakeryM[CustomUser]) -> UserFactory:
    """Factory fixture for creating User instances."""

    def factory(**kwargs: Unpack[_UserFactoryParams]) -> CustomUser:
        return fakery_m(CustomUser)(**kwargs)

    return factory


@pytest.fixture
def auth_admin(user_factory: UserFactory) -> CustomUser:
    """Fixture that create a single admin User instance."""
    return user_factory(
        username='Admin',
        email='testadmin@example.com',
        first_name='first_name_admin',
        last_name='last_name_admin',
        is_active=True,
        role='admin'
    )


@pytest.fixture
def auth_user(user_factory: UserFactory) -> CustomUser:
    """Fixture that create a single User instance."""
    return user_factory(
        username='testuser',
        email='testuser@example.com',
        first_name='first_name_user',
        last_name='last_name_user',
        is_active=True,
        role='user'
    )


@pytest.fixture
def api_client() -> APIClient:
    """API client."""
    return APIClient()


@pytest.fixture
def auth_admin_client(api_client: APIClient, auth_admin: CustomUser) -> APIClient:
    """Return an authenticated APIClient for testing."""
    api_client.force_authenticate(user=auth_admin)
    return api_client


@pytest.fixture
def auth_user_client(
    api_client: APIClient, auth_user: CustomUser
) -> APIClient:
    """Return an authenticated APIClient for testing."""
    api_client.force_authenticate(user=auth_user)
    return api_client