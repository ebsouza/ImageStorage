import os
import json
import shutil
import unittest

from instance.config import app_config
from src.app import create_app

def is_gitignore(file):
    return "gitignore" in file


class ApiStorageTestCase(unittest.TestCase):

    def setUp(self):
        os.environ["APP_SETTINGS"] = "testing"
        os.environ["FILE_EXTENSION"] = ".jpg"

        self.app = create_app()
        self.client = self.app.test_client
        self.image_path = app_config[os.getenv('APP_SETTINGS')][1]
        self.image_extension = os.getenv('FILE_EXTENSION')

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_get_info(self):
        """ /info (GET) """
        response = self.client().get('/info')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['total_size'] >= 0)
        self.assertTrue(data['total_images'] >= 0)

    def test_get_image(self):
        """ /image/<image_id> (GET) """
        base_path = 'test-assets/'

        shutil.copyfile(base_path + 'example1' + self.image_extension, self.image_path + 'example1' + self.image_extension)

        response = self.client().get('/image/example1')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['id'], 'example1')
        self.assertTrue(isinstance(response.json[0]['encoded_image'], str))

        os.remove(self.image_path + 'example1' + self.image_extension)

    def test_get_image_all(self):
        """ /image (GET) """
        base_path = 'test-assets/'

        shutil.copyfile(base_path + 'example1' + self.image_extension, self.image_path + 'example1' + self.image_extension)
        shutil.copyfile(base_path + 'example2' + self.image_extension, self.image_path + 'example2' + self.image_extension)

        response = self.client().get('/image')
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertTrue(isinstance(response.json[0]['id'], str))
        self.assertTrue(isinstance(response.json[0]['encoded_image'], str))
        self.assertTrue(isinstance(response.json[1]['id'], str))
        self.assertTrue(isinstance(response.json[1]['encoded_image'], str))

        os.remove(self.image_path + 'example1' + self.image_extension)
        os.remove(self.image_path + 'example2' + self.image_extension)

    def test_send_image(self):
        """ /image (POST) """
        from src.image.utils import create_image_encode
        
        image_id = 'example1'
        image_path = f"test-assets/{image_id}{self.image_extension}"
        absolute_path = os.path.abspath(image_path)

        json_file = dict()
        json_file['id'] = image_id
        json_file['image_data'] = create_image_encode(absolute_path)

        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 201)

    def test_send_empty_json(self):
        """ /image (POST) """
        json_file = dict()
        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 500)
    
    def test_send_invalid_image_data(self):
        """ /image (POST) """
        json_file = {'id': 'any_ID', 'image_data': '123456'}
        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 500)

    def test_send_invalid_json(self):
        """ /image (POST) """
        response = self.client().post('/image', json=123)

        self.assertEqual(response.status_code, 500)

    def test_remove_image(self):
        """ /image/<image_id> (DELETE) """
        image_id = 'example2'
        base_path = 'test-assets/'

        shutil.copyfile(base_path + image_id + self.image_extension, self.image_path + image_id + self.image_extension)

        response = self.client().delete('/image/' + image_id)
        self.assertEqual(response.status_code, 200)

    def test_remove_all_images(self):
        """ /image (DELETE) """
        from src.image.utils import get_total_images

        base_path = 'test-assets/'

        shutil.copyfile(base_path + "example1" + self.image_extension, self.image_path + "example1" + self.image_extension)
        shutil.copyfile(base_path + "example2" + self.image_extension, self.image_path + "example2" + self.image_extension)
        shutil.copyfile(base_path + "example3" + self.image_extension, self.image_path + "example3" + self.image_extension)

        self.client().delete('/image')

        total_images = get_total_images(self.image_path)

        self.assertEqual(total_images, 0)


if __name__ == "__main__":
    unittest.main()
