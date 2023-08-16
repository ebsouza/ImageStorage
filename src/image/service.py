from typing import List

from src.config import settings
from src.image.model import Image
from src.image.repository import ImageRepositoryDB
from src.logging import get_logging
from src.tasks.image import create_image_task, remove_image_task

logger = get_logging(__name__)


def create_image(image_b64: str, repository: ImageRepositoryDB) -> Image:
    image = Image.create(settings.STORAGE_WEB)
    logger.info(f"Creating image(id={image.id!r})")

    repository.add(image)
    create_image_task.delay(image.id, image_b64)

    return image


def remove_image(image_id: str, repository: ImageRepositoryDB):
    logger.info(f"Removing image(id={image_id!r})")

    repository.remove(image_id)
    remove_image_task.delay(image_id)


def get_image(image_id: str, repository: ImageRepositoryDB) -> Image:
    logger.info(f"Getting image(id={image_id!r})")

    return repository.get(image_id)


def get_image_many(repository: ImageRepositoryDB,
                   offset: int = 0,
                   limit: int = 10) -> List[Image]:
    logger.info(f"Getting many images (offset={offset!r}, limit={limit!r})")

    return repository.get_many(offset, limit)
