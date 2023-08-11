from src.celery_app import celery
from src.bootstrap import repository_fs

QUEQUE = "image"

@celery.task(queue=QUEQUE)
def create_image_task(image_id: str, image_b64: str):
    repository_fs.add(image_id, image_b64)

@celery.task(queue=QUEQUE)
def remove_image_task(image_id: str):
    repository_fs.remove(image_id)
