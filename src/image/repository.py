from typing import List
from uuid import UUID

from src.image.data import ImageFileSystem, ImageBinary
from src.image.model import Image
from src.image.data import ClientSQL


class ImageRepositoryDB:

    def __init__(self, client: ClientSQL):
        self._client = client

    def add(self, image: Image):
        self._client.add(image)

    def get(self, image_id: str) -> Image:
        return self._client.get(UUID(image_id))
    
    def remove(self, image_id: str):
        self._client.remove(UUID(image_id))

    def get_many(self, offset: int = 0, limit: int = 10) -> List[Image]:
        return list(self._client.get_many(offset, limit))


class ImageRepositoryFS:

    def __init__(self, data_store: ImageFileSystem):
        self._data_store = data_store

    def add(self, image: ImageBinary):
        self._data_store.create(image.id, image.image_data)

    def get(self, image_id: str) -> ImageBinary:

        image_data = self._data_store.get(image_id)
        image = ImageBinary(id=image_id, image_data=image_data)
        return image

    def get_many(self, limit: int = 100) -> List[ImageBinary]:
        image_dict = self._data_store.get_all(limit)
        images = [
            ImageBinary(id=image_id, image_data=image_data)
            for image_id, image_data in image_dict.items()
        ]
        return images

    def remove(self, image_id: str):
        self._data_store.remove(image_id)

    def remove_all(self) -> List[str]:
        image_ids = self._data_store.remove_all()

        return image_ids

    def get_total_size(self) -> float:
        return self._data_store.size
