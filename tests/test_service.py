import pytest

from src.image.error import ImageNotFound
from src.image.service import (create_image, get_encoded_image,
                               get_total_images, get_total_size, remove_image)
from tests.utils import create_image as create_image_utils
from tests.utils import create_N_images, remove_all_images


class TestService:

    @pytest.mark.asyncio
    async def test_create_image(self, setup, image_path, image_decoded):
        await create_image('image_id', image_decoded)

        assert 1 == get_total_images()

        remove_all_images(image_path)

    def test_remove_image_one_file(self, setup, image_path):
        image_id = 'any_image_id'
        create_image_utils(image_path, image_id)

        assert 1 == get_total_images()

        remove_image(image_id)

        assert 0 == get_total_images()

    def test_remove_image_not_found(self):
        with pytest.raises(ImageNotFound):
            remove_image('image_id')

    def test_remove_image_all_files(self, setup, image_path):
        NUMBER_OF_IMAGES = 5
        create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == get_total_images()

        remove_image(None)

        assert 0 == get_total_images()

    @pytest.mark.asyncio
    async def test_get_encoded_image_one_file(self, setup, image_path):
        image_id = 'any_image_id'
        create_image_utils(image_path, image_id)

        image_ids, enconded_images = await get_encoded_image(image_id)

        assert 1 == len(image_ids)
        assert image_id == image_ids[0]
        assert 1 == len(enconded_images)

        remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_get_encoded_image_not_found(self):
        image_id = 'any_image_id'

        with pytest.raises(ImageNotFound):
            await get_encoded_image(image_id)

    @pytest.mark.asyncio
    async def test_get_encoded_image_all_files(self, setup, image_path):
        NUMBER_OF_IMAGES = 5
        create_N_images(image_path, NUMBER_OF_IMAGES)

        image_ids, enconded_images = await get_encoded_image(None)

        assert NUMBER_OF_IMAGES == len(image_ids)
        assert NUMBER_OF_IMAGES == len(enconded_images)

        remove_all_images(image_path)

    def test_get_total_images(self, setup, image_path):
        NUMBER_OF_IMAGES = 5
        create_N_images(image_path, NUMBER_OF_IMAGES)

        assert NUMBER_OF_IMAGES == get_total_images()

        remove_all_images(image_path)

    def test_get_total_size(self, setup, image_path):
        NUMBER_OF_IMAGES = 5
        FIVE_TEST_IMAGES_SIZE_MB = 0.006945
        create_N_images(image_path, NUMBER_OF_IMAGES)

        assert FIVE_TEST_IMAGES_SIZE_MB == get_total_size()

        remove_all_images(image_path)
