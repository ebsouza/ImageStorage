import unittest
import os
import json
import base64
import shutil

from app import create_app


def isGitignore(file):
    return "gitignore" in file

class ApiStorageTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""
    image_extension = '.jpg'
    config_name = 'testing'

    def setUp(self):
        """Define test variables and initialize app."""
        os.environ["APP_SETTINGS"] = "testing"
        os.environ["FILE_EXTENSION"] = ".jpg"
        self.app = create_app()
        self.client = self.app.test_client

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    """
    '/info' [GET]
    """
    def test_get_info(self):
        #Test API can responde info (GET request)
        res = self.client().get('/info')
        self.assertEqual(res.status_code, 200)

    def test_is_info_valid(self):
        #Test API can create a bucketlist (GET request)
        res = self.client().get('/info')
        j = json.loads(res.data)
        self.assertTrue(j['total size (Mb)'] >= 0)
        self.assertTrue(j['number of images'] >= 0)



    """
    '/image' [GET]
    """
    def test_image_list(self):
        # ---- Check wheter API return images from storage (GET request) ----
        image_extension = ApiStorageTestCase.image_extension
        base_path = 'test-assets/'
        storage_path = 'test-assets/Images/'

        #Copy images to storage
        shutil.copyfile(base_path + 'example1' + image_extension, storage_path + 'example1' + image_extension)
        shutil.copyfile(base_path + 'example2' + image_extension, storage_path + 'example2' + image_extension)
        shutil.copyfile(base_path + 'example3' + image_extension, storage_path + 'example3' + image_extension)

        #Get image size
        example1_size = os.stat(storage_path + 'example1' + image_extension).st_size / 1000000
        example2_size = os.stat(storage_path + 'example2' + image_extension).st_size / 1000000
        example3_size = os.stat(storage_path + 'example3' + image_extension).st_size / 1000000

        #Request
        res = self.client().get('/image/all')
        
        #Expected Json
        json_file_1 = {'file_name': 'example1' + image_extension, 'size (Mb)': example1_size}
        json_file_2 = {'file_name': 'example2' + image_extension, 'size (Mb)': example2_size}
        json_file_3 = {'file_name': 'example3' + image_extension, 'size (Mb)': example3_size}

        #Test
        self.assertIn(json_file_1, json.loads(res.data))
        self.assertIn(json_file_2, json.loads(res.data))
        self.assertIn(json_file_3, json.loads(res.data))
        
        #Cleaning up the storage
        os.remove(storage_path + 'example1' + image_extension)
        os.remove(storage_path + 'example2' + image_extension)
        os.remove(storage_path + 'example3' + image_extension)

    
    def test_empty_return(self):
        storage_path = 'test-assets/Images/'
        image_extension = ApiStorageTestCase.image_extension
        try:
            path, dirs, files = next(os.walk(storage_path))
        except Exception as e:
            print('I wasnt possible to open images .Reason: %s' % (e))

        #Remove all images in storage
        for file_ in files:
            if not isGitignore(file_): 
                os.remove(storage_path + file_ )

        res = self.client().get('/image/all')
        self.assertEqual(res.status_code, 404)

    def test_send_image(self):
        #Test API post image (POST request)
        imageId = 'example1'
        image_64_encode = ""
        image_extension = ApiStorageTestCase.image_extension

        with open( 'test-assets/' + imageId + image_extension, 'rb') as image:
            image_read = image.read() 
            #image_64_encode = base64.encodestring(image_read) #Deprecated
            image_64_encode = base64.encodebytes(image_read) 
            image_64_encode = image_64_encode.decode("utf-8")

        json_file = {}
        json_file['ID'] = imageId
        json_file['image_data'] = image_64_encode

        
        res = self.client().post('/image', json=json_file)

        self.assertEqual(res.status_code, 201)

        os.remove('test-assets/Images/' + imageId + image_extension)

    def test_send_empty_json(self):
        # ---- Test send empty json return ----
        json_file={}
        res = self.client().post('/image', json=json_file)
        self.assertEqual(res.status_code, 500)
    
    def test_send_invalid_json(self):
        # ---- Test send invalid json return ----
        #1 - Invalid image_data
        json_file={'ID':'any_ID', 'image_data':'123456'}
        res = self.client().post('/image', json=json_file)
        self.assertEqual(res.status_code, 500)

        #2 - Invalid Json
        res = self.client().post('/image', json=123)
        self.assertEqual(res.status_code, 500)

    def test_remove_image(self):
        #Test API remove a specific image (DELETE request)
        image_id = 'example2'
        image_extension = ApiStorageTestCase.image_extension
        base_path = 'test-assets/'
        storage_path = 'test-assets/Images/'

        #Copy image to storage
        shutil.copyfile(base_path + image_id + image_extension, storage_path + image_id + image_extension)

        #Remove with API
        res = self.client().delete('/image/' + image_id)
        self.assertEqual(res.status_code, 200)

    def test_remove_all_images(self):
        #Test API remove all images (DELETE request)
        storage_path = 'test-assets/Images/'

        self.client().delete('/image/all')

        try:
            path, dirs, files = next(os.walk( storage_path ))
        except Exception as e:
            print('I wasnt possible to open images .Reason: %s' % (e))

        #Remove all images in storage
        counter = 0
        for file_ in files:
            counter += 1

        self.assertTrue(counter == 0)


if __name__ == "__main__":
    unittest.main()