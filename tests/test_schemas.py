import os

from src.image.schemas import (INVALID_OFFSET, build_link, build_schema,
                               get_image, get_image_collection,
                               get_next_offset, get_previous_offset)


class TestSchemas:

    def test_build_schema_with_image_id(self, image):
        any_offset = 0
        image_id = '<any_image_id>'

        data = build_schema(image_id, [image], any_offset)

        assert isinstance(data['id'], str)
        assert isinstance(data['image_data'], str)

    def test_build_schema_without_image_id(self, image_collection_factory):
        offset = 0
        TOTAL_IMAGES = 5
        COLLECTION_LIMIT = int(os.getenv('COLLECTION_LIMIT'))
        images = image_collection_factory(TOTAL_IMAGES)

        data = build_schema(None, images, offset)

        assert isinstance(data['kind'], str)
        assert isinstance(data['next'], str)
        assert isinstance(data['previous'], str)
        assert isinstance(data['data'], list)
        assert COLLECTION_LIMIT == len(data['data'])

    def test_get_image(self, image):
        data = get_image([image])

        assert isinstance(data['id'], str)
        assert isinstance(data['image_data'], str)

    def test_get_image_collection(self, image_collection_factory):
        offset = 0
        TOTAL_IMAGES = 5
        COLLECTION_LIMIT = int(os.getenv('COLLECTION_LIMIT'))
        images = image_collection_factory(TOTAL_IMAGES)

        data = get_image_collection(images, offset)

        assert isinstance(data['kind'], str)
        assert isinstance(data['next'], str)
        assert isinstance(data['previous'], str)
        assert isinstance(data['data'], list)
        assert COLLECTION_LIMIT == len(data['data'])

    def test_get_next_offset(self):
        total_images = 10
        limit = total_images // 3
        offset = total_images - (limit + 1)
        next_offset = get_next_offset(offset, limit, total_images)

        assert next_offset == offset + limit

    def test_get_next_offset_close_to_total(self):
        total_images = 10
        limit = total_images // 3
        offset = total_images - (limit - 1)
        next_offset = get_next_offset(offset, limit, total_images)

        assert INVALID_OFFSET == next_offset

    def test_get_previous_offset(self):
        offset = 10
        limit = offset // 3
        previous_offset = get_previous_offset(offset, limit)

        assert previous_offset == offset - limit

    def test_get_previous_offset_close_to_beginning(self):
        offset = 3
        limit = offset + 1
        previous_offset = get_previous_offset(offset, limit)

        assert 0 == previous_offset

    def test_build_link(self):
        offset = 5
        host = os.getenv('EXPOSED_URL')
        link = build_link(offset)

        assert f'{host}/image?offset={offset}' == link

    def test_build_link_null_case(self):
        link = build_link(INVALID_OFFSET)

        assert None == link
