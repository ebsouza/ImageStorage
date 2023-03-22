from typing import List

from src.image.model import Image
from src.image.repository import ImageRepository


async def create_image(image: Image, repository: ImageRepository):
    await repository.add(image)


def remove_image(image_id: str, repository: ImageRepository) -> List[str]:
    if image_id is None:
        image_ids = repository.remove_all()
    else:
        repository.remove(image_id)
        image_ids = [image_id]
    return image_ids


async def get_encoded_image(image_id: str,
                            repository: ImageRepository) -> List[Image]:
    if image_id is None:
        images = await repository.get_many()
    else:
        image = await repository.get(image_id)
        images = [image]

    return images


async def get_total_images(repository: ImageRepository) -> int:
    images = await repository.get_many()

    return len(images)


def get_total_size(repository: ImageRepository) -> float:
    return repository.get_total_size()
