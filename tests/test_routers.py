import os

import tests.utils as test_utils


class TestRouters:

    def test_get_info(self, client):
        """ /info (GET) """
        response = client.get('/v1/storage/info')
        assert response.status_code == 200

        data = response.json()
        assert data['total_size'] >= 0
        assert data['total_images'] >= 0

    def test_get_image(self, client, image_repository):
        """ /images/<image_id> (GET) """

        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        response = client.get(f'/v1/images/{image_id}')
        data = response.json()

        assert 200 == response.status_code

        assert data['id'] == image_id
        assert isinstance(data['image_data'], str)

        test_utils.remove_all_images(image_path)

    def test_get_image_all(self, client, image_repository):
        """ /images (GET) """

        COLLECTION_LIMIT = int(os.getenv('COLLECTION_LIMIT'))
        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.get('/v1/images')
        data = response.json()

        assert 200 == response.status_code
        assert isinstance(data['kind'], str)
        assert isinstance(data['next'], str)
        assert isinstance(data['previous'], str)
        assert COLLECTION_LIMIT == len(data['data'])

        test_utils.remove_all_images(image_path)

    def test_get_image_traversal_all_images(self, client, image_repository):
        """ /images (GET) """

        COLLECTION_LIMIT = int(os.getenv('COLLECTION_LIMIT'))
        NUMBER_OF_IMAGES_TOTAL = 3 * COLLECTION_LIMIT
        for number_of_images in range(NUMBER_OF_IMAGES_TOTAL):
            image_path = image_repository._data_store._path
            test_utils.create_N_images(image_path, number_of_images)

            ids = list()
            NEXT_URL = '/v1/images'

            while NEXT_URL:
                response = client.get(NEXT_URL)
                data = response.json()

                for image in data['data']:
                    ids.append(image['id'])

                if data['next'] is None:
                    break

                images_uri = data['next'].rsplit('/')[1:]
                NEXT_URL = f"/{images_uri[0]}/{images_uri[1]}"

            unique_ids = set(ids)
            assert number_of_images == len(unique_ids)

            test_utils.remove_all_images(image_path)

    def test_create_image(self, client, image_path, image_payload):
        """ /images (POST) """

        response = client.post('/v1/images', json=image_payload)

        assert response.status_code == 201

        test_utils.remove_all_images(image_path)

    def test_create_image_invalid_encoded_image(self, client, image_path,
                                                image_payload_invalid):
        """ /images (POST) """

        response = client.post('/v1/images', json=image_payload_invalid)

        assert response.status_code == 400

        test_utils.remove_all_images(image_path)

    def test_remove_image(self, client, image_repository):
        """ /images/<image_id> (DELETE) """

        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        response = client.delete(f'/v1/images/{image_id}')

        assert 0 == test_utils.count_images(image_path)
        assert response.status_code == 200

    def test_remove_all_images(self, client, image_repository):
        """ /image (DELETE) """

        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.delete('/v1/images')
        image_ids = response.json()['data']

        assert 0 == test_utils.count_images(image_path)
        assert NUMBER_OF_IMAGES == len(image_ids)
