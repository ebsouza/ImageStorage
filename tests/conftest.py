import base64
import os
import uuid
from io import BytesIO

import pytest
import sqlalchemy as db
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.config import load_config
from src.errors import setup_exception_handlers
from src.image.data import ClientSQL, ImageBinary, ImageFileSystem
from src.image.model import Image
from src.image.repository import ImageRepositoryDB, ImageRepositoryFS
from src.image.router import build_images_router
from tests.utils import create_dummy_image, remove_all_images


@pytest.fixture
def client(image_repository_db):
    app = FastAPI()

    @app.get('/')
    def about():
        return 'Image Storage API. By: EBSouza'

    app.include_router(build_images_router(image_repository_db),
                       prefix='/v1/images')

    setup_exception_handlers(app)

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
def image_decoded(image_encoded):
    return base64.decodebytes(image_encoded.encode('utf-8'))


@pytest.fixture
def image_payload(image_encoded):
    json_file = dict()
    json_file['data'] = image_encoded

    return json_file


@pytest.fixture
def image_payload_invalid():
    json_file = dict()
    json_file['data'] = 'invalid_image_data_<123456>'

    return json_file


@pytest.fixture
def image_file_system(image_path, image_extension):
    if not os.path.exists(image_path):
        os.mkdir(image_path)
    else:
        remove_all_images(image_path)

    return ImageFileSystem(image_path, image_extension)


@pytest.fixture
def image_repository(image_file_system):
    return ImageRepositoryFS(image_file_system)


@pytest.fixture
def image_binary(image_encoded):
    return ImageBinary(id='any_data', image_data=image_encoded)


@pytest.fixture
def image_binary_collection_factory(image_encoded):

    def factory(length):
        images = list()
        for index in range(length):
            image = ImageBinary(id=f'image_{index}', image_data=image_encoded)
            images.append(image)
        return images

    return factory


@pytest.fixture
def image_collection_factory():

    def factory(length):
        images = list()
        for index in range(length):
            image = Image(id=uuid.uuid4(), path='<any_path>')
            images.append(image)
        return images

    return factory


@pytest.fixture
def image():
    return Image(id=uuid.uuid4(), path='<any_path>')


@pytest.fixture
def client_sql():
    engine = db.create_engine("sqlite:///database.db", future=True)
    return ClientSQL(engine)


@pytest.fixture
def image_repository_db(client_sql):
    return ImageRepositoryDB(client_sql)
