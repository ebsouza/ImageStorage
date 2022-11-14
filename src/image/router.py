from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from src.image.service import get_encoded_image, create_image, remove_image, get_total_images, get_total_size
from src.image.utils import decode_image
from src.image.schemas import ImageGet
from src.image.error import ImageNotFound, ImageDecodeError

router = APIRouter()


@router.get('/image')
@router.get('/image/{image_id}')
async def get_image_view(image_id: str = None):
    
    try:
        image_ids, encoded_images = await get_encoded_image(image_id)
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")

    data = ImageGet.create_list(ids=image_ids, encoded_images=encoded_images)

    return JSONResponse(content=data, status_code=200)


@router.post('/image')
async def create_image_view(image: ImageGet):
    try:
        image_64_decoded = decode_image(image.image_data)
    except ImageDecodeError:
        raise HTTPException(status_code=400, detail="Not base64 encoded image")

    await create_image(image.id, image_64_decoded)

    return JSONResponse(content= {'data': image.id},  status_code=201)


@router.delete('/image')
@router.delete('/image/{image_id}')
def remove_image_view(image_id: str = None):
    try:
        image_ids = remove_image(image_id)
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")

    return JSONResponse(content= {'data': image_ids},  status_code=200)


@router.get('/info')
def sys_info_view():
    data = dict()

    data['total_images'] = get_total_images()
    data['total_size'] = get_total_size()
    
    return JSONResponse(content=data,  status_code=200)
