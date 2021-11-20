import os
from instance.config import app_config

app_settings = os.getenv('APP_SETTINGS', 'development')
PATH_TO_IMAGE = app_config[app_settings][1]
image_extension = os.getenv('FILE_EXTENSION')


def create_image():
    pass


def remove_image(image_id):
    image = f"{PATH_TO_IMAGE}{image_id}{image_extension}"
    os.remove(image)


def remove_images():
    for filename in os.listdir(PATH_TO_IMAGE):
        file_path = os.path.join(PATH_TO_IMAGE, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def get_image():
    pass


def encode_image(image):
    pass


def decode_image(image):
    pass