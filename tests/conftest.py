import os 
import base64
from io import BytesIO

from fastapi.testclient import TestClient
import pytest

from src.app import create_app
from src.config import load_config
from tests.utils import create_dummy_image


@pytest.fixture
def setup(image_path):
    if not os.path.exists(image_path):
        os.mkdir(image_path)


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


@pytest.fixture
def image_encoded():
    image = create_dummy_image()

    image_buffer = BytesIO()
    image.save(image_buffer, format='JPEG')
    byte_data = image_buffer.getvalue()
    return base64.b64encode(byte_data).decode("utf-8")


@pytest.fixture
def image_payload(image_encoded):
    json_file = dict()
    json_file['id'] = 'test'
    json_file['image_data'] = image_encoded

    return json_file