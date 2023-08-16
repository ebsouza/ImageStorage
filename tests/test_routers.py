import os

import pytest

import tests.utils as test_utils


class TestRouters:

    def test_get_image(self, client, image_repository_db, image):
        image_repository_db.add(image)
        response = client.get(f'/v1/images/{str(image.id)}')
        data = response.json()

        assert 200 == response.status_code
        assert data['id'] == str(image.id)
        assert isinstance(data['path'], str)

    def test_get_image_many(self, client, image_repository_db,
                            image_collection_factory):
        NUMBER_OF_IMAGES = 5
        LIMIT = 3
        images = image_collection_factory(NUMBER_OF_IMAGES)

        for image in images:
            image_repository_db.add(image)

        response = client.get(f'/v1/images?limit={LIMIT}')
        data = response.json()

        assert 200 == response.status_code
        assert isinstance(data['kind'], str)
        assert isinstance(data['next'], str)
        assert isinstance(data['previous'], str)
        assert LIMIT == len(data['data'])

    @pytest.mark.skip
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

    def test_create_image(self, client, image_payload):
        """ /images (POST) """

        response = client.post('/v1/images', json=image_payload)

        assert response.status_code == 201

    def test_remove_image(self, client, image_repository_db, image):
        """ /images/<image_id> (DELETE) """

        image_repository_db.add(image)

        response = client.delete(f'/v1/images/{str(image.id)}')

        assert response.status_code == 200
