from typing import List

from src.image.model import Image
from src.image.repository import ImageRepository
from src.logging import get_logging
from src.tasks.image import create_image_task, remove_image_task, update_image_task

logger = get_logging(__name__)


def create_image(image_b64: str, repository: ImageRepository) -> Image:
    image = Image.create('xpto')
    repository.add(image)
    create_image_task.delay(image.id, image_b64)
    logger.info(f"Image '{image.id}' was created")

    return image


def remove_image(image_id: str, repository: ImageRepository):
    repository.remove(image_id)
    remove_image_task.delay(image_id)


def get_image(image_id: str, repository: ImageRepository) -> Image:
    return repository.get(image_id)


def get_image_many(repository: ImageRepository, offset: int = 0, limit: int = 10) -> List[Image]:
    return repository.get_many(offset, limit)
