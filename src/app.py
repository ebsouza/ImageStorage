import os

from fastapi import FastAPI

from src.image.router import router as image_router
from src.config import ALLOWED_EXTENSIONS


def create_app():
    app = FastAPI()

    file_extension = os.getenv('FILE_EXTENSION')
    if file_extension not in ALLOWED_EXTENSIONS:
        raise NameError('Extension is not valid.')

    @app.get('/')
    def about():
        return 'Image Storage API. By: EBSouza'

    app.include_router(image_router)

    return app