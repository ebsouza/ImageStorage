import os

from fastapi import FastAPI

from src.bootstrap import repository
from src.config import ALLOWED_EXTENSIONS
from src.image.router import build_router


def create_app():
    app = FastAPI()

    validate_extension()

    @app.get('/')
    def about():
        return 'Image Storage API. By: EBSouza'

    app.include_router(build_router(repository))

    return app


def validate_extension():
    if os.getenv('FILE_EXTENSION') not in ALLOWED_EXTENSIONS:
        raise NameError('Extension is not valid.')
