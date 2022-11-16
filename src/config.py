import os
from functools import lru_cache

ALLOWED_EXTENSIONS = ('jpg', 'png', 'jpeg')


@lru_cache(maxsize=1)
def load_config():
    config = dict()

    config['file_extension'] = os.getenv('FILE_EXTENSION', 'jpg')

    app_settings = os.getenv('APP_SETTINGS')

    if app_settings == 'production':
        config['storage'] = 'Storage'
    elif app_settings == 'development':
        config['storage'] = 'dev-storage'
    elif app_settings == 'testing':
        config['storage'] = 'test-storage'

    return config
