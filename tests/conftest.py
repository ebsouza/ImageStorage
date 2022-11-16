from fastapi.testclient import TestClient
import pytest

from src.app import create_app
from src.config import load_config


@pytest.fixture
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture
def image_path():
    return load_config()['storage']


@pytest.fixture
def image_extension():
    return load_config()['file_extension']
