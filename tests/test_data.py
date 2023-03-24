import pytest

import tests.utils as test_utils
from src.image.error import ImageNotFound, ImageDecodeError


class TestImageFileSystem:

    @pytest.mark.asyncio
    async def test_create_image(self, image_file_system, image_encoded):
        image_path = image_file_system._path

        NUMBER_OF_IMAGES = 3
        for index in range(NUMBER_OF_IMAGES):
            await image_file_system.create(f'image_{index}', image_encoded)

        assert NUMBER_OF_IMAGES == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_create_image_invalid_data(self, image_file_system, image_encoded):
        image_path = image_file_system._path

        with pytest.raises(ImageDecodeError):
            await image_file_system.create('image', 'invalid_image_data_<123456>')

        assert 0 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_create_image_override(self, image_file_system,
                                         image_encoded):
        image_path = image_file_system._path

        NUMBER_OF_IMAGES = 3
        for _ in range(NUMBER_OF_IMAGES):
            await image_file_system.create('image_id', image_encoded)

        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    def test_remove_image(self, image_file_system):
        image_path = image_file_system._path
        image_id = 'any_id'

        test_utils.create_image(image_path, image_id)

        assert 1 == test_utils.count_images(image_path)

        image_file_system.remove(image_id)

        assert 0 == test_utils.count_images(image_path)

    def test_remove_all_images(self, image_file_system):
        NUMBER_OF_IMAGES = 3
        image_path = image_file_system._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == test_utils.count_images(image_path)

        image_ids = image_file_system.remove_all()

        assert 0 == test_utils.count_images(image_path)
        assert 3 == len(image_ids)

    @pytest.mark.asyncio
    async def test_get_image(self, image_file_system):
        image_path = image_file_system._path
        image_id = 'any_id'

        test_utils.create_image(image_path, image_id)

        encoded_image = await image_file_system.get(image_id)

        assert isinstance(encoded_image, str)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_image_not_found(self, image_file_system):
        assert 0 == test_utils.count_images(image_file_system._path)

        with pytest.raises(ImageNotFound):
            await image_file_system.get('any_id')

    @pytest.mark.asyncio
    async def test_get_image_all(self, image_file_system):
        NUMBER_OF_IMAGES = 3
        image_path = image_file_system._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        data = await image_file_system.get_all()

        assert isinstance(data, dict)
        assert NUMBER_OF_IMAGES == len(data)

        test_utils.remove_all_images(image_path)

    def test_images_data_property(self, image_file_system):
        NUMBER_OF_IMAGES = 3
        image_path = image_file_system._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        counter = 0
        for data in image_file_system.images_data:
            assert isinstance(data['image_path'], str)
            assert isinstance(data['filename'], str)
            assert isinstance(data['image_id'], str)
            counter += 1

        assert NUMBER_OF_IMAGES == counter

        test_utils.remove_all_images(image_path)

    def test_size_property(self, image_file_system):
        NUMBER_OF_IMAGES = 3
        image_path = image_file_system._path

        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        assert image_file_system.size > 0

        test_utils.remove_all_images(image_path)
