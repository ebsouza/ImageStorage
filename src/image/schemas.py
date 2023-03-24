import os
from typing import List

from src.image.model import Image

INVALID_OFFSET = -1

    
def build_schema(image_id: str, images: List[Image], offset: int):
    if image_id is None:
        data = get_image_collection(images, offset)
    else:
        data = get_image(images)

    return data


def get_image(images: List[Image]):
    data = list()

    image = images[0]
    content = {'id': image.id, 'image_data': image.image_data}
    data.append(content)

    return data


def get_image_collection(images: List[Image], offset: int = 0):
    LIMIT = int(os.getenv('COLLECTION_LIMIT'))
    next_offset = get_next_offset(offset, LIMIT, len(images))
    previous_offset = get_previous_offset(offset, LIMIT)

    data = {
        "kind": "Collection",
        "next": build_link(next_offset),
        "previous": build_link(previous_offset),
        "data": list()
    }

    for image in images[offset:offset + LIMIT]:
        content = {'id': image.id, 'image_data': image.image_data}
        data["data"].append(content)

    return data


def get_next_offset(offset: int, limit: int, total_images: int):
    next_offset = offset + limit

    if next_offset >= total_images:
        next_offset = INVALID_OFFSET

    return next_offset


def get_previous_offset(offset: int, limit: int):
    previous_offset = offset - limit

    if previous_offset <= 0:
        previous_offset = 0

    return previous_offset


def build_link(offset: int):
    if offset == INVALID_OFFSET:
        return None

    HOST = os.getenv('EXPOSED_URL')
    return f'{HOST}/image?offset={offset}'
