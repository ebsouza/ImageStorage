import os
import json
import shutil
import unittest

from app import create_app
from instance.config import app_config
from app.image.utils import get_total_images, create_image_encode


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
        self.assertTrue(data['total size (Mb)'] >= 0)
        self.assertTrue(data['number of images'] >= 0)

    def test_get_image_all(self):
        """ /image/all (GET) """
        base_path = 'test-assets/'

        # Copy images to storage
        shutil.copyfile(base_path + 'example1' + self.image_extension, self.image_path + 'example1' + self.image_extension)
        shutil.copyfile(base_path + 'example2' + self.image_extension, self.image_path + 'example2' + self.image_extension)
        shutil.copyfile(base_path + 'example3' + self.image_extension, self.image_path + 'example3' + self.image_extension)

        # Get image size
        example1_size = os.stat(self.image_path + 'example1' + self.image_extension).st_size / 1000000
        example2_size = os.stat(self.image_path + 'example2' + self.image_extension).st_size / 1000000
        example3_size = os.stat(self.image_path + 'example3' + self.image_extension).st_size / 1000000

        # Request
        res = self.client().get('/image/all')
        
        # Expected Json
        json_file_1 = {'file_name': 'example1' + self.image_extension, 'size (Mb)': example1_size}
        json_file_2 = {'file_name': 'example2' + self.image_extension, 'size (Mb)': example2_size}
        json_file_3 = {'file_name': 'example3' + self.image_extension, 'size (Mb)': example3_size}

        # Test
        self.assertIn(json_file_1, json.loads(res.data))
        self.assertIn(json_file_2, json.loads(res.data))
        self.assertIn(json_file_3, json.loads(res.data))
        
        # Cleaning up the storage
        os.remove(self.image_path + 'example1' + self.image_extension)
        os.remove(self.image_path + 'example2' + self.image_extension)
        os.remove(self.image_path + 'example3' + self.image_extension)

    def test_get_image_all_empty_return(self):
        """ /image/all (GET) """
        try:
            path, dirs, files = next(os.walk(self.image_path))
        except Exception as e:
            print('I wasnt possible to open images .Reason: %s' % (e))

        # Remove all images in storage
        for file_ in files:
            if not is_gitignore(file_):
                os.remove(self.image_path + file_)

        response = self.client().get('/image/all')
        self.assertEqual(response.status_code, 404)

    def test_send_image(self):
        """ /image/<image_id> (POST) """
        image_id = 'example1'
        image_path = f"test-assets/{image_id}{self.image_extension}"
        absolute_path = os.path.abspath(image_path)

        json_file = dict()
        json_file['ID'] = image_id
        json_file['image_data'] = create_image_encode(absolute_path)

        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 201)

    def test_send_empty_json(self):
        """ /image/<image_id> (POST) """
        json_file = dict()
        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 500)
    
    def test_send_invalid_image_data(self):
        """ /image/<image_id> (POST) """
        json_file = {'ID': 'any_ID', 'image_data': '123456'}
        response = self.client().post('/image', json=json_file)

        self.assertEqual(response.status_code, 500)

    def test_send_invalid_json(self):
        """ /image/<image_id> (POST) """
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
        """ /image/all (DELETE) """

        base_path = 'test-assets/'

        shutil.copyfile(base_path + "example1" + self.image_extension, self.image_path + "example1" + self.image_extension)
        shutil.copyfile(base_path + "example2" + self.image_extension, self.image_path + "example2" + self.image_extension)
        shutil.copyfile(base_path + "example3" + self.image_extension, self.image_path + "example3" + self.image_extension)

        self.client().delete('/image/all')

        total_images = get_total_images(self.image_path)

        self.assertEqual(total_images, 0)


if __name__ == "__main__":
    unittest.main()
