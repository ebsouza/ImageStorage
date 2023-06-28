import pytest

import tests.utils as test_utils
from src.image.errors import ImageNotFound
from src.image.model import Image


class TestImageRepository:

    @pytest.mark.asyncio
    async def test_add_image(self, image_repository, image):
        image_path = image_repository._data_store._path

        await image_repository.add(image)

        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_image(self, image_repository):
        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        image = await image_repository.get(image_id)

        assert isinstance(image, Image)
        assert image_id == image.id
        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_image_not_found(self, image_repository):
        with pytest.raises(ImageNotFound):
            await image_repository.get('<any_id>')

    @pytest.mark.asyncio
    async def test_get_image_many(self, image_repository):
        NUMBER_OF_IMAGES = 5
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        images = await image_repository.get_many()

        for image in images:
            assert isinstance(image, Image)

        assert NUMBER_OF_IMAGES == len(images)

        test_utils.remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_image_many_limit(self, image_repository):
        NUMBER_OF_IMAGES = 5
        LIMIT_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        images = await image_repository.get_many(LIMIT_OF_IMAGES)

        for image in images:
            assert isinstance(image, Image)

        assert isinstance(images, list)
        assert LIMIT_OF_IMAGES == len(images)
        assert LIMIT_OF_IMAGES != NUMBER_OF_IMAGES

        test_utils.remove_all_images(image_path)

    def test_remove_image(self, image_repository):
        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        assert 1 == test_utils.count_images(image_path)

        image_repository.remove(image_id)

        assert 0 == test_utils.count_images(image_path)

    def test_remove_all_image(self, image_repository):
        NUMBER_OF_IMAGES = 5
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == test_utils.count_images(image_path)

        image_repository.remove_all()

        assert 0 == test_utils.count_images(image_path)

    def test_get_total_size(self, image_repository):
        NUMBER_OF_IMAGES = 5
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == test_utils.count_images(image_path)

        size = image_repository.get_total_size()

        assert size > 0
