import os

from fastapi import FastAPI

from src.bootstrap import repository
from src.config import ALLOWED_EXTENSIONS
from src.image.router import build_images_router, build_storage_router


def create_app():
    app = FastAPI()

    validate_extension()

    @app.get('/')
    def about():
        return 'Image Storage API. By: EBSouza'

    app.include_router(build_images_router(repository), prefix='/v1/images')
    app.include_router(build_storage_router(repository), prefix='/v1/storage')

    return app


def validate_extension():
    if os.getenv('FILE_EXTENSION') not in ALLOWED_EXTENSIONS:
        raise NameError('Extension is not valid.')
