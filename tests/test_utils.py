import pytest

from src.image.utils import is_image_file, get_path_to_image, encode_image, PATH_TO_IMAGE, IMAGE_EXTENSION
from src.image.error import ImageDecodeError, ImageNotFound
from tests.utils import create_image, remove_all_images


class TestUtils:

    def test_is_image_file_correct_extension(self):
        paht_to_image = 'path/to/image/fake_image_id.jpg'

        assert is_image_file(paht_to_image)

    def test_is_image_file_incorrect_extension(self):
        paht_to_image_1 = 'path/to/image/fake_image_id.xpto'
        paht_to_image_2 = 'path/to/image/.xpto_file'

        assert not is_image_file(paht_to_image_1)
        assert not is_image_file(paht_to_image_2)

    def test_get_path_to_image(self):
        image_id = 'any_image_id_value'

        path_to_image = get_path_to_image(image_id)

        assert f'{PATH_TO_IMAGE}/{image_id}.{IMAGE_EXTENSION}' == path_to_image

    @pytest.mark.asyncio
    async def test_encode_image(self, setup, image_path):
        image_id = 'any_image_id'
        create_image(image_path, image_id)

        image_encoded = await encode_image(image_id)

        assert isinstance(image_encoded, str)

        remove_all_images(image_path)

    @pytest.mark.asyncio
    async def test_encode_image_not_found(self):
        with pytest.raises(ImageNotFound):
            await encode_image('any_image_id')
        
