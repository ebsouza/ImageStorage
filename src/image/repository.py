from typing import List

from src.image.data import ImageFileSystem
from src.image.model import Image


class ImageRepository:

    def __init__(self, data_store: ImageFileSystem):
        self._data_store = data_store

    async def add(self, image: Image):
        await self._data_store.create(image.id, image.image_data)

    async def get(self, image_id: str) -> Image:

        image_data = await self._data_store.get(image_id)
        image = Image(id=image_id, image_data=image_data)
        return image

    async def get_many(self, limit: int = 100) -> List[Image]:
        image_dict = await self._data_store.get_all(limit)
        images = [
            Image(id=image_id, image_data=image_data)
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
