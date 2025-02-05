import pytest

from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture
def client():
    return APIClient()
