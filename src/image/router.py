from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse

from src.image.service import get_encoded_image
from src.image.schemas import ImageGet
from src.image.error import ImageNotFound

router = APIRouter()


@router.get('/image')
@router.get('/image/{image_id}')
def get_image_view(image_id: str):
    
    try:
        image_ids, encoded_images = get_encoded_image(image_id)
    except ImageNotFound:
        raise HTTPException(status_code=404, detail="Image not found")

    data = ImageGet.create_list(ids=image_ids, encoded_images=encoded_images)

    return JSONResponse(content=data, status_code=200)
