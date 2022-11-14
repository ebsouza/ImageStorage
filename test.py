import os
import shutil
import unittest

from fastapi.testclient import TestClient

from src.app import create_app
from src.config import load_config
from src.image.service import get_total_images


def is_gitignore(file):
    return "gitignore" in file


class ApiStorageTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = TestClient(self.app)
        self.image_path = load_config()['storage']
        self.image_extension = load_config()['file_extension']

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_get_info(self):
        """ /info (GET) """
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertTrue(data['total_size'] >= 0)
        self.assertTrue(data['total_images'] >= 0)

    def test_get_image(self):
        """ /image/<image_id> (GET) """
        base_path = 'test-assets'

        shutil.copyfile(f'{base_path}/example1.{self.image_extension}',
                        f'{self.image_path}/example1.{self.image_extension}')

        response = self.client.get('/image/example1')
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['id'], 'example1')
        self.assertTrue(isinstance(data[0]['image_data'], str))

        os.remove(f'{self.image_path}/example1.{self.image_extension}')

    def test_get_image_all(self):
        """ /image (GET) """
        base_path = 'test-assets'

        NUMBER_OF_IMAGES = 2

        for index in range(1, NUMBER_OF_IMAGES + 1):
            shutil.copyfile(f'{base_path}/example{index}.{self.image_extension}',
                        f'{self.image_path}/example{index}.{self.image_extension}')

        response = self.client.get('/image')

        self.assertEqual(response.status_code, 200)

        data = response.json()
        self.assertEqual(len(data), NUMBER_OF_IMAGES)
        self.assertTrue('id' in data[0])
        self.assertTrue('image_data' in data[0])

        for index in range(1, NUMBER_OF_IMAGES + 1):
            os.remove(f'{self.image_path}/example{index}.{self.image_extension}')

    def test_create_image(self):
        """ /image (POST) """
        from src.image.utils import create_image_encode

        image_id = 'example1'
        image_path = f"test-assets/{image_id}.{self.image_extension}"
        absolute_path = os.path.abspath(image_path)

        json_file = dict()
        json_file['id'] = image_id
        json_file['image_data'] = create_image_encode(absolute_path)

        response = self.client.post('/image', json=json_file)

        self.assertEqual(response.status_code, 201)

        os.remove(f'{self.image_path}/{image_id}.{self.image_extension}')

    def test_send_invalid_image_data(self):
        """ /image (POST) """
        json_file = {'id': 'any_ID', 'image_data': '123456'}
        response = self.client.post('/image', json=json_file)

        self.assertEqual(response.status_code, 400)

    def test_remove_image(self):
        """ /image/<image_id> (DELETE) """
        image_id = 'example2'
        base_path = 'test-assets'

        shutil.copyfile(
            f'{base_path}/{image_id}.{self.image_extension}',
            f'{self.image_path}/{image_id}.{self.image_extension}')

        response = self.client.delete(f'/image/{image_id}')
        self.assertEqual(response.status_code, 200)

    def test_remove_all_images(self):
        """ /image (DELETE) """

        base_path = 'test-assets'
        NUMBER_OF_IMAGES = 3

        for index in range(1, NUMBER_OF_IMAGES + 1):
            shutil.copyfile(f'{base_path}/example{index}.{self.image_extension}',
                        f'{self.image_path}/example{index}.{self.image_extension}')

        response = self.client.delete('/image')
        image_ids = response.json()['data']

        self.assertEqual(get_total_images(), 0)
        self.assertEqual(len(image_ids), NUMBER_OF_IMAGES)


if __name__ == "__main__":
    unittest.main()
