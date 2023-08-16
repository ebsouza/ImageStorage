import uuid

import pytest

import src.image.service as service
from src.image.errors import ImageNotFound
from src.image.model import Image
from tests.utils import clean_repository_db

class TestService:

    def test_create_image(self, image_repository_db):
        image_created = service.create_image('image_b64_fake',
                                             image_repository_db)

        image_recovered = image_repository_db.get(str(image_created.id))
        assert image_recovered.id == image_created.id

    def test_get_image(self, image_repository_db, image):
        image_repository_db.add(image)

        image_recovered = service.get_image(str(image.id), image_repository_db)

        assert image_recovered.id == image.id

        image_repository_db.remove(str(image.id))

        with pytest.raises(ImageNotFound):
            image_repository_db.get(str(image.id))

    def test_get_image_no_image(self, image_repository_db, image):
        any_id = uuid.uuid4()

        with pytest.raises(ImageNotFound):
            image_repository_db.get(str(any_id))

    def test_get_image_many(self, image_repository_db,
                            image_collection_factory):
        NUMBER_OF_IMAGES = 5
        LIMIT = 3
        images = image_collection_factory(NUMBER_OF_IMAGES)

        for image in images:
            image_repository_db.add(image)

        images_recovered = service.get_image_many(image_repository_db, 0,
                                                  LIMIT)

        assert LIMIT == len(images_recovered)
        assert isinstance(images_recovered[0], Image)

    def test_get_image_many_no_images(self, image_repository_db):
        clean_repository_db(image_repository_db)
        images_recovered = service.get_image_many(image_repository_db)

        assert 0 == len(images_recovered)

    def test_remove_image(self, image_repository_db, image):
        image_repository_db.add(image)

        service.remove_image(str(image.id), image_repository_db)

        with pytest.raises(ImageNotFound):
            image_repository_db.get(str(image.id))

    def test_remove_image_no_image(self, image_repository_db, image):
        with pytest.raises(ImageNotFound):
            service.remove_image(str(image.id), image_repository_db)
