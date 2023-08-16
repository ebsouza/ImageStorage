import os
#from functools import lru_cache

ALLOWED_EXTENSIONS = ('jpg', 'png', 'jpeg')


def load_config():
    config = dict()

    config['file_extension'] = os.getenv('FILE_EXTENSION', 'jpg')

    app_settings = os.getenv('APP_SETTINGS')

    if app_settings == 'production':
        config['storage'] = os.getenv('STORAGE_FS')
        config['storage_web'] = os.getenv('STORAGE_WEB')
        config['broker'] = 'amqp://guest:guest@rabbitmq:5672//'
    elif app_settings == 'development':
        config['storage'] = 'Storage-dev'
    elif app_settings == 'testing':
        config['storage'] = 'Storage-test'
        config['broker'] = 'memory://'

    return config
