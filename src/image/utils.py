import base64
import binascii
import re

import aiofiles

from src.config import load_config
from src.image.error import ImageDecodeError, ImageNotFound

PATH_TO_IMAGE = load_config()['storage']
IMAGE_EXTENSION = load_config()['file_extension']


def is_image_file(path_to_image):
    if not re.search(f'.{IMAGE_EXTENSION}', path_to_image):
        return False

    return True


def get_path_to_image(image_id):
    return f'{PATH_TO_IMAGE}/{image_id}.{IMAGE_EXTENSION}'


async def encode_image(image_id):
    image_path = get_path_to_image(image_id)
    try:
        async with aiofiles.open(image_path, 'rb') as image:
            image_read = await image.read()
            image_64_encode = base64.b64encode(image_read)
            encoded_image = image_64_encode.decode("utf-8")

        return encoded_image

    except FileNotFoundError:
        raise ImageNotFound


def decode_image(encoded_image):
    try:
        return base64.decodebytes(encoded_image.encode('utf-8'))
    except binascii.Error:
        raise ImageDecodeError
