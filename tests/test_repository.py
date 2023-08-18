import pytest

import tests.utils as test_utils
from src.image.data import ImageBinary
from src.image.errors import ImageNotFound


class TestImageRepositoryFS:

    def test_add_image(self, image_repository, image_binary):
        image_path = image_repository._data_store._path

        image_repository.add(image_binary)

        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    def test_get_image(self, image_repository):
        image_path = image_repository._data_store._path
        image_id = '<any_id>'
        test_utils.create_image(image_path, image_id)

        image = image_repository.get(image_id)

        assert isinstance(image, ImageBinary)
        assert image_id == image.id
        assert 1 == test_utils.count_images(image_path)

        test_utils.remove_all_images(image_path)

    def test_get_image_not_found(self, image_repository):
        with pytest.raises(ImageNotFound):
            image_repository.get('<any_id>')

    def test_get_image_many(self, image_repository):
        NUMBER_OF_IMAGES = 5
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        images = image_repository.get_many()

        for image in images:
            assert isinstance(image, ImageBinary)

        assert NUMBER_OF_IMAGES == len(images)

        test_utils.remove_all_images(image_path)

    def test_get_image_many_limit(self, image_repository):
        NUMBER_OF_IMAGES = 5
        LIMIT_OF_IMAGES = 3
        image_path = image_repository._data_store._path
        test_utils.create_N_images(image_path, NUMBER_OF_IMAGES)

        images = image_repository.get_many(LIMIT_OF_IMAGES)

        for image in images:
            assert isinstance(image, ImageBinary)

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
