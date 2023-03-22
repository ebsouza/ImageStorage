import tests.utils as test_utils


class TestRouters:

    def test_get_info(self, client):
        """ /info (GET) """
        response = client.get('/info')
        assert response.status_code == 200

        data = response.json()
        assert data['total_size'] >= 0
        assert data['total_images'] >= 0

    def test_get_image(self, client, image_repository):
        """ /image/<image_id> (GET) """

        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        response = client.get(f'/image/{image_id}')
        data = response.json()

        assert 200 == response.status_code
        assert 1 == len(data)

        assert data[0]['id'] == image_id
        assert isinstance(data[0]['image_data'], str)

        test_utils.remove_all_images(image_path)

    def test_get_image_all(self, client, image_repository):
        """ /image (GET) """

        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.get('/image')
        data = response.json()

        assert 200 == response.status_code
        assert NUMBER_OF_IMAGES == len(data)
        for d in data:
            assert 'id' in d
            assert 'image_data' in d

        test_utils.remove_all_images(image_path)

    def test_create_image(self, client, image_path, image_payload):
        """ /image (POST) """

        response = client.post('/image', json=image_payload)

        assert response.status_code == 201

        test_utils.remove_all_images(image_path)

    def test_remove_image(self, client, image_repository):
        """ /image/<image_id> (DELETE) """

        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        response = client.delete(f'/image/{image_id}')

        assert 0 == test_utils.count_images(image_path)
        assert response.status_code == 200

    def test_remove_all_images(self, client, image_repository):
        """ /image (DELETE) """

        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        response = client.delete('/image')
        image_ids = response.json()['data']

        assert 0 == test_utils.count_images(image_path)
        assert NUMBER_OF_IMAGES == len(image_ids)
