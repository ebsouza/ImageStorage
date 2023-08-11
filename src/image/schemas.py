import os
from typing import List

from pydantic import BaseModel

from src.image.model import Image

INVALID_OFFSET = -1


class ImageIn(BaseModel):
    data: str


class ImageOut(BaseModel):
    data: str


def build_schema(images: List[Image], offset: int, limit: int):
    return get_image_collection(images, offset, limit)


def get_image_collection(images: List[Image], offset: int = 0, limit: int = 10):
    next_offset = get_next_offset(offset, limit, len(images))
    previous_offset = get_previous_offset(offset, limit)

    data = {
        "kind": "Collection",
        "next": build_link(next_offset, limit),
        "previous": build_link(previous_offset, limit),
        "data": list()
    }

    #for image in images[offset:offset + limit]:
    for image in images:
        content = {'id': image.id, 'path': image.path}
        data["data"].append(content)

    return data


def get_next_offset(offset: int, limit: int, total_images: int):
    next_offset = offset + limit

    if total_images < limit:
        next_offset = INVALID_OFFSET

    return next_offset


def get_previous_offset(offset: int, limit: int):
    previous_offset = offset - limit

    if previous_offset <= 0:
        previous_offset = 0

    return previous_offset


def build_link(offset: int, limit: int):
    if offset == INVALID_OFFSET:
        return None

    HOST = os.getenv('EXPOSED_URL')
    return f'{HOST}/v1/images?offset={offset}&limit={limit}'
