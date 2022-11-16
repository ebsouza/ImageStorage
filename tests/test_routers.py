import os
import shutil

import pytest

from src.image.service import get_total_images
from tests.utils import create_image_encode, create_N_images, remove_all_images, create_image


class TestRouters:

    def test_get_info(self, client):
        """ /info (GET) """
        response = client.get('/info')
        assert response.status_code == 200

        data = response.json()
        assert data['total_size'] >= 0
        assert data['total_images'] >= 0

    def test_get_image(self, setup, client, image_path):
        """ /image/<image_id> (GET) """

        image_id = 'test'
        create_image(image_path, image_id)

        response = client.get(f'/image/{image_id}')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == 1
        assert data[0]['id'] == image_id
        assert isinstance(data[0]['image_data'], str)

        remove_all_images(image_path)

    def test_get_image_all(self, setup, client, image_path):
        """ /image (GET) """

        NUMBER_OF_IMAGES = 3
        create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.get('/image')
        data = response.json()

        assert response.status_code == 200
        assert len(data) == NUMBER_OF_IMAGES
        assert 'id' in data[0]
        assert 'image_data' in data[0]

        remove_all_images(image_path)

    def test_create_image(self, setup, client, image_path, image_payload):
        """ /image (POST) """

        response = client.post('/image', json=image_payload)

        assert response.status_code == 201

        remove_all_images(image_path)

    def test_send_invalid_image_data(self, setup, client):
        """ /image (POST) """
        json_file = {'id': 'any_ID', 'image_data': '123456'}
        response = client.post('/image', json=json_file)

        assert response.status_code == 400

    def test_remove_image(self, setup, client, image_path):
        """ /image/<image_id> (DELETE) """
        image_id = 'example2'

        create_image(image_path, image_id)

        response = client.delete(f'/image/{image_id}')

        assert get_total_images() == 0
        assert response.status_code == 200

        remove_all_images(image_path)

    def test_remove_all_images(self, setup, client, image_path):
        """ /image (DELETE) """

        NUMBER_OF_IMAGES = 3
        create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.delete('/image')
        image_ids = response.json()['data']

        assert get_total_images() == 0
        assert len(image_ids) == NUMBER_OF_IMAGES

        remove_all_images(image_path)
