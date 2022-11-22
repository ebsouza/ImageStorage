import os
from functools import singledispatch

import aiofiles

from src.image.error import ImageNotFound
from src.image.utils import (PATH_TO_IMAGE, encode_image, get_path_to_image,
                             is_image_file)


async def create_image(image_id, image_64_decoded):
    path_to_image = get_path_to_image(image_id)

    async with aiofiles.open(path_to_image, 'wb') as image_created:
        await image_created.write(image_64_decoded)


@singledispatch
def remove_image():
    raise NotImplementedError("Implement remove_image function.")


@remove_image.register
def _(image_id: str):
    path_to_image = get_path_to_image(image_id)
    try:
        os.remove(path_to_image)
    except FileNotFoundError:
        raise ImageNotFound

    return [image_id]


@remove_image.register
def _(image_id: None):
    image_ids = []
    for filename in os.listdir(PATH_TO_IMAGE):

        if not is_image_file(filename):
            continue

        path_to_image = os.path.join(PATH_TO_IMAGE, filename)

        try:
            if os.path.isfile(path_to_image):
                os.remove(path_to_image)
                image_ids.append(filename)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (path_to_image, e))

    return image_ids


@singledispatch
async def get_encoded_image():
    raise NotImplementedError("Implement get_encoded_image function.")


@get_encoded_image.register
async def _(image_id: None):
    _, _, files = next(os.walk(PATH_TO_IMAGE))

    image_ids, enconded_images = list(), list()
    for file in files:
        if not is_image_file(file):
            continue

        image_id = file.rsplit(".", 1)[0]

        image_ids.append(image_id)
        enconded_images.append(await encode_image(image_id))

    return image_ids, enconded_images


@get_encoded_image.register
async def _(image_id: str):
    return [image_id], [ await encode_image(image_id)]


def get_total_images():
    _, _, files = next(os.walk(PATH_TO_IMAGE))

    files = [file for file in files if is_image_file(file)]

    return len(files)


def get_total_size():
    path, _, files = next(os.walk(PATH_TO_IMAGE))
    total_size = 0

    for file in files:
        if not is_image_file(file):
            continue

        total_size += os.stat(f'{path}/{file}').st_size

    return total_size / 1000000  # convert to Mb
