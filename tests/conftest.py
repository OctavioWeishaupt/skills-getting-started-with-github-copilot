import pytest
from fastapi.testclient import TestClient
from copy import deepcopy

from src.app import app, activities


@pytest.fixture
def client():
    """Test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory `activities` dict before each test."""
    snapshot = deepcopy(activities)
    yield
    activities.clear()
    activities.update(snapshot)
