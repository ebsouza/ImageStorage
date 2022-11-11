import os
import base64
from instance.config import app_config

from .utils import is_image_file


app_settings = os.getenv('APP_SETTINGS', 'testing')
PATH_TO_IMAGE = app_config[app_settings][1]
IMAGE_EXTENSION = os.getenv('FILE_EXTENSION', '.jpg')


def create_image(image_id, image_64_decoded):
    image_path = PATH_TO_IMAGE + image_id + IMAGE_EXTENSION

    with open(image_path, 'wb') as image_result:
        image_result.write(image_64_decoded)


def remove_image(image_id):
    image = f"{PATH_TO_IMAGE}{image_id}{IMAGE_EXTENSION}"
    os.remove(image)

    return image_id


def remove_images():
    images_id = []
    for filename in os.listdir(PATH_TO_IMAGE):

        if not is_image_file(filename):
            continue

        file_path = os.path.join(PATH_TO_IMAGE, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                images_id.append(filename)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return images_id


def get_image(image_id):
    pass


def encode_image(image_id):
    image_path = PATH_TO_IMAGE + image_id + IMAGE_EXTENSION
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodestring(image_read)
        image_64_encode = image_64_encode.decode("utf-8")

    return image_64_encode


def decode_image(image_encoded):
    image_64_encode = image_encoded
    image_64_encode = image_64_encode.encode("utf-8")

    return base64.decodebytes(image_64_encode)
