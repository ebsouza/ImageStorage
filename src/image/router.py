from fastapi import APIRouter
from starlette.responses import JSONResponse

import src.image.schemas as schema
from src.image.schemas import ImageIn
#from src.image.model import Image
from src.image.repository import ImageRepository
from src.image.service import (create_image, get_image_many, get_image, remove_image)


def build_images_router(image_repository: ImageRepository):

    router = APIRouter()

    @router.get('/')
    def get_images_view(offset: int = 0, limit: int = 10):
        images = get_image_many(image_repository, offset, limit)
        data = schema.build_schema(images, offset, limit)

        return JSONResponse(content=data, status_code=200)

    @router.get('/{image_id}')
    def get_image_view(image_id: str):
        image = get_image(image_id, image_repository)

        if image is None:
            data = {}
        else:
            data = image.as_dict()

        return JSONResponse(content=data, status_code=200)

    @router.post('/')
    def create_image_view(image: ImageIn):
        image_id = create_image(image.data, image_repository)

        return JSONResponse(content={'image_id': image_id}, status_code=201)

    @router.delete('/{image_id}')
    def remove_image_view(image_id: str):
        remove_image(image_id, image_repository)

        return JSONResponse(content={'image_id': image_id}, status_code=200)

    return router
