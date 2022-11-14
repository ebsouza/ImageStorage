import os
from functools import lru_cache


ALLOWED_EXTENSIONS = ['jpg', 'png', 'jpeg']


@lru_cache(maxsize=1)
def load_config():
    config = dict()

    config['file_extension'] = os.getenv('FILE_EXTENSION', 'jpg')

    if os.getenv('APP_SETTINGS', 'production'):
        config['storage'] = 'Images'
    else:
        config['storage'] = 'test-assets/Images'

    return config
