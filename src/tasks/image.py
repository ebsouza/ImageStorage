from src.bootstrap import repository_fs
from src.celery_app import celery
from src.image.data import ImageBinary

QUEQUE = "image"


@celery.task(queue=QUEQUE)
def create_image_task(image_id: str, image_b64: str):
    image = ImageBinary(id=image_id, image_data=image_b64)
    repository_fs.add(image)


@celery.task(queue=QUEQUE)
def remove_image_task(image_id: str):
    repository_fs.remove(image_id)
