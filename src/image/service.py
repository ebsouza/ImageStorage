import base64
import os
from functools import singledispatch

from instance.config import app_config

from src.image.utils import encode_image, is_image_file

#from .model import (create_image, decode_image, encode_image, remove_image,
#                    remove_images)
#from .utils import get_total_images, get_total_size, is_image_file


app_settings = os.getenv('APP_SETTINGS', 'testing')
PATH_TO_IMAGE = app_config[app_settings][1]
IMAGE_EXTENSION = os.getenv('FILE_EXTENSION', '.jpg')

app_settings = os.getenv('APP_SETTINGS', 'development')
path_to_images = app_config[app_settings][1]
image_extension = os.getenv('FILE_EXTENSION')


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


@singledispatch
def get_encoded_image():
    raise NotImplementedError("Implement process function.")


@get_encoded_image.register
def _(image_id: None):
    _, _, files = next(os.walk(path_to_images))

    image_ids, enconded_images = list(), list()
    for file in files:
        if not is_image_file(file):
            continue

        image_id = file.rsplit(".", 1)[0]

        image_ids.append(image_id)
        enconded_images.append(encode_image(image_id))

    return image_ids, enconded_images


@get_encoded_image.register
def _(image_id: str):
    return [image_id], [encode_image(image_id)]


def get_total_images(path):
    try:
        _, _, files = next(os.walk(path))

        files = [file for file in files if is_image_file(file)]

    except Exception as e:
        print("Error: %s" % (e))

    return len(files)


def get_total_size(path):
    try:
        path, dirs, files = next(os.walk(path))
        total_size = 0
        for file in files:

            if not is_image_file(file):
                continue

            file_path = path + file
            total_size += os.stat(file_path).st_size
        total_size = total_size / 1000000  # convert to Mb
    except Exception as e:
        print("Error: %s" % (e))

    return total_size