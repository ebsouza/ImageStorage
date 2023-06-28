from fastapi import APIRouter
from starlette.responses import JSONResponse

import src.image.schemas as schema
from src.image.model import Image
from src.image.repository import ImageRepository
from src.image.service import (create_image, get_encoded_image,
                               get_total_images, get_total_size, remove_image)


def build_images_router(image_repository: ImageRepository):

    router = APIRouter()

    @router.get('/')
    @router.get('/{image_id}')
    async def get_image_view(image_id: str = None, offset: int = 0):
        images = await get_encoded_image(image_id, image_repository)
        data = schema.build_schema(image_id, images, offset)

        return JSONResponse(content=data, status_code=200)

    @router.post('/')
    async def create_image_view(image: Image):
        await create_image(image, image_repository)

        return JSONResponse(content={'data': image.id}, status_code=201)

    @router.delete('/')
    @router.delete('/{image_id}')
    def remove_image_view(image_id: str = None):
        image_ids = remove_image(image_id, image_repository)

        return JSONResponse(content={'data': image_ids}, status_code=200)

    return router


def build_storage_router(image_repository: ImageRepository):

    router = APIRouter()

    @router.get('/info')
    async def sys_info_view():
        data = dict()

        data['total_images'] = await get_total_images(image_repository)
        data['total_size'] = get_total_size(image_repository)

        return JSONResponse(content=data, status_code=200)

    return router
