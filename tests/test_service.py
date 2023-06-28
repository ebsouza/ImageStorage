import pytest

import src.image.service as service
import tests.utils as test_utils
from src.image.errors import ImageNotFound
from src.image.model import Image


class TestService:

    @pytest.mark.asyncio
    async def test_create_image(self, image_repository, image):
        image_path = image_repository._data_store._path

        await service.create_image(image, image_repository)

        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    def test_remove_image(self, image_repository):
        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        assert 1 == test_utils.count_images(image_path)

        image_ids = service.remove_image(image_id, image_repository)

        assert 0 == test_utils.count_images(image_path)
        assert isinstance(image_ids, list)

    def test_remove_all_images(self, image_repository):
        NUMBER_OF_IMAGES = 5
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == test_utils.count_images(image_path)

        image_ids = service.remove_image(None, image_repository)
        assert isinstance(image_ids, list)

        assert 0 == test_utils.count_images(image_path)

    @pytest.mark.asyncio
    async def test_get_encoded_image(self, image_repository):
        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        images = await service.get_encoded_image(image_id, image_repository)
        assert isinstance(images, list)
        assert isinstance(images[0], Image)
        assert images[0].id == image_id

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_encoded_image_not_found(self, image_repository):
        with pytest.raises(ImageNotFound):
            await service.get_encoded_image('<any_id>', image_repository)

    @pytest.mark.asyncio
    async def test_get_encoded_image_all(self, image_repository):
        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        images = await service.get_encoded_image(None, image_repository)

        assert isinstance(images, list)
        for image in images:
            assert isinstance(image, Image)
        assert NUMBER_OF_IMAGES == len(images)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_total_images(self, image_repository):
        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        total_images = await service.get_total_images(image_repository)

        assert NUMBER_OF_IMAGES == total_images

        test_utils.remove_all_images(image_path)

    def test_get_total_size(self, image_repository):
        NUMBER_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        total_size = service.get_total_size(image_repository)

        assert total_size > 0

        test_utils.remove_all_images(image_path)
