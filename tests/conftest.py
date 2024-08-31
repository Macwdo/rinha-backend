from fastapi.testclient import TestClient
import pytest
from src.main import app


@pytest.fixture(scope="function")
def client():
    return TestClient(app)
