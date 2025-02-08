import pytest

from core.redis import redis_client
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture(autouse=True)
def mock_redis():
    yield redis_client
    redis_client.flushdb()
