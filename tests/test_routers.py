import os
import shutil

from fastapi.testclient import TestClient
import pytest

from src.app import create_app
from src.config import load_config
from src.image.service import get_total_images


def is_gitignore(file):
    return "gitignore" in file


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


class TestRouters:

    def test_get_info(self, client):
        """ /info (GET) """
        response = client.get('/info')
        assert response.status_code == 200

        data = response.json()
        assert data['total_size'] >= 0
        assert data['total_images'] >= 0

    def test_get_image(self, client, image_path, image_extension):
        """ /image/<image_id> (GET) """
        base_path = 'test-assets'

        shutil.copyfile(f'{base_path}/example1.{image_extension}',
                        f'{image_path}/example1.{image_extension}')

        response = client.get('/image/example1')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['id'] == 'example1'
        assert isinstance(data[0]['image_data'], str)

        os.remove(f'{image_path}/example1.{image_extension}')

    def test_get_image_all(self, client, image_path, image_extension):
        """ /image (GET) """
        base_path = 'test-assets'

        NUMBER_OF_IMAGES = 2

        for index in range(1, NUMBER_OF_IMAGES + 1):
            shutil.copyfile(f'{base_path}/example{index}.{image_extension}',
                        f'{image_path}/example{index}.{image_extension}')

        response = client.get('/image')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == NUMBER_OF_IMAGES
        assert 'id' in data[0]
        assert 'image_data' in data[0]

        for index in range(1, NUMBER_OF_IMAGES + 1):
            os.remove(f'{image_path}/example{index}.{image_extension}')

    def test_create_image(self, client, image_path, image_extension):
        """ /image (POST) """
        from src.image.utils import create_image_encode

        image_id = 'example1'
        image_path_ = f"test-assets/{image_id}.{image_extension}"
        absolute_path = os.path.abspath(image_path_)

        json_file = dict()
        json_file['id'] = image_id
        json_file['image_data'] = create_image_encode(absolute_path)

        response = client.post('/image', json=json_file)

        assert response.status_code == 201

        os.remove(f'{image_path}/{image_id}.{image_extension}')

    def test_send_invalid_image_data(self, client):
        """ /image (POST) """
        json_file = {'id': 'any_ID', 'image_data': '123456'}
        response = client.post('/image', json=json_file)

        assert response.status_code == 400

    def test_remove_image(self, client, image_path, image_extension):
        """ /image/<image_id> (DELETE) """
        image_id = 'example2'
        base_path = 'test-assets'

        shutil.copyfile(
            f'{base_path}/{image_id}.{image_extension}',
            f'{image_path}/{image_id}.{image_extension}')

        response = client.delete(f'/image/{image_id}')
        assert response.status_code == 200

    def test_remove_all_images(self, client, image_path, image_extension):
        """ /image (DELETE) """

        base_path = 'test-assets'
        NUMBER_OF_IMAGES = 3

        for index in range(1, NUMBER_OF_IMAGES + 1):
            shutil.copyfile(f'{base_path}/example{index}.{image_extension}',
                        f'{image_path}/example{index}.{image_extension}')

        response = client.delete('/image')
        image_ids = response.json()['data']

        assert get_total_images() == 0
        assert len(image_ids) == NUMBER_OF_IMAGES
