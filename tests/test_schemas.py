import os
import uuid

from src.image.model import Image
from src.image.schemas import ImageManyOut, ImageOut


class TestSchemas:

    def test_imageout_from_model_to_schema(self):
        image = Image(id=uuid.uuid4(), path='xpto')
        image_out = ImageOut.from_model_to_schema(image)

        assert str(image.id) == image_out['id']
        assert image.path == image_out['path']

    def test_image_out_limit_lesser_than_total_images(
            self, image_collection_factory):
        OFFSET, LIMIT, TOTAL_IMAGES = 0, 10, 20
        images = image_collection_factory(TOTAL_IMAGES)

        data = ImageManyOut(images, OFFSET, LIMIT).data

        assert LIMIT < TOTAL_IMAGES
        assert isinstance(data['kind'], str)
        assert isinstance(data['next'], str)
        assert isinstance(data['previous'], str)
        assert isinstance(data['data'], list)
        assert data['next'].startswith(os.getenv('EXPOSED_URL'))
        assert data['previous'].startswith(os.getenv('EXPOSED_URL'))
        assert TOTAL_IMAGES == len(data['data'])

    def test_image_out_limit_greater_than_total_images(
            self, image_collection_factory):
        OFFSET, LIMIT, TOTAL_IMAGES = 0, 6, 3
        images = image_collection_factory(TOTAL_IMAGES)

        data = ImageManyOut(images, OFFSET, LIMIT).data

        assert LIMIT > TOTAL_IMAGES
        assert isinstance(data['kind'], str)
        assert data['next'] is None
        assert isinstance(data['previous'], str)
        assert isinstance(data['data'], list)
        assert data['previous'].startswith(os.getenv('EXPOSED_URL'))
        assert TOTAL_IMAGES == len(data['data'])
