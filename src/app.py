import os
from flask import Flask

from instance.config import app_config

IMAGE_EXTENSION_LIST = ['.jpg', '.png', '.jpeg']


def create_app():
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS', 'development')
    app.config.from_object(app_config[app_settings][0])

    file_extension = os.getenv('FILE_EXTENSION')
    if file_extension not in IMAGE_EXTENSION_LIST:
        raise NameError('Extension is not valid.')

    from .image import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app