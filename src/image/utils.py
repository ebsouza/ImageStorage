import base64
import binascii

import aiofiles
from PIL import Image

from src.config import load_config
from src.image.error import ImageDecodeError, ImageNotFound

PATH_TO_IMAGE = load_config()['storage']
IMAGE_EXTENSION = load_config()['file_extension']


# Move to test folder
def create_dummy_image(image_path, extension=".jpg"):
    img = Image.new('RGB', (300, 150), color='red')
    file_name = image_path + extension
    img.save(file_name)


# Move to test folder
def create_image_encode(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)

    return image_64_encode.decode("utf-8")


def is_image_file(path):
    return path.rsplit(".")[0] != ''


async def encode_image(image_id):
    image_path = f'{PATH_TO_IMAGE}/{image_id}.{IMAGE_EXTENSION}'
    try:
        async with aiofiles.open(image_path, 'rb') as image:
            image_read = await image.read()
            image_64_encode = base64.b64encode(image_read)
            encoded_image = image_64_encode.decode("utf-8")

        return encoded_image

    except FileNotFoundError:
        raise ImageNotFound


def decode_image(image_encoded):
    try:
        image_64_encode = image_encoded
        image_64_encode = image_64_encode.encode("utf-8")

        return base64.decodebytes(image_64_encode)
    except binascii.Error:
        raise ImageDecodeError
