from typing import List

from pydantic import BaseModel

from src.config import settings
from src.image.model import Image


class ImageIn(BaseModel):
    data: str


class ImageOut(BaseModel):
    id: str
    path: str

    @classmethod
    def from_model_to_schema(cls, image: Image):
        if image is None:
            return {}

        return cls(id=str(image.id), path=image.path).model_dump()


class ImageManyOut:

    INVALID_OFFSET = -1

    def __init__(self, images: List[Image], offset: int, limit: int):
        self.data = self._get_image_collection(images, offset, limit)

    def _get_image_collection(self,
                              images: List[Image],
                              offset: int = 0,
                              limit: int = 10):
        next_offset = self._get_next_offset(offset, limit, len(images))
        previous_offset = self._get_previous_offset(offset, limit)

        data = {
            "kind": "Collection",
            "next": self._build_link(next_offset, limit),
            "previous": self._build_link(previous_offset, limit),
            "data": list()
        }

        for image in images:
            content = {'id': str(image.id), 'path': image.path}
            data["data"].append(content)

        return data

    def _get_next_offset(self, offset: int, limit: int, total_images: int):
        next_offset = offset + limit

        if total_images < limit:
            next_offset = self.INVALID_OFFSET

        return next_offset

    def _get_previous_offset(self, offset: int, limit: int):
        previous_offset = offset - limit

        if previous_offset <= 0:
            previous_offset = 0

        return previous_offset

    def _build_link(self, offset: int, limit: int):
        if offset == self.INVALID_OFFSET:
            return None

        HOST = settings.EXPOSED_URL
        return f'{HOST}/v1/images?offset={offset}&limit={limit}'
