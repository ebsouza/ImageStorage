import os
import base64
import glob

from PIL import Image


def create_dummy_image():
    img = Image.new('RGB', (300, 150), color='red')
    return img


def create_image(image_folder, image_id):
    extension = os.getenv('FILE_EXTENSION')
    img = Image.new('RGB', (300, 150), color='red')
    image_path = f'{image_folder}/{image_id}.{extension}'
    img.save(image_path)


def create_N_images(image_folder, n=3):
    extension = os.getenv('FILE_EXTENSION')
    for counter in range(n):
        img = Image.new('RGB', (300, 150), color='red')
        image_path = f'{image_folder}/image_{counter}.{extension}'
        img.save(image_path)


def remove_all_images(image_folder):
    files = glob.glob(f'{image_folder}/*')
    for image_path in files:
        os.remove(image_path)


def create_image_encode(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)

    return image_64_encode.decode("utf-8")
