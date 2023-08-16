import base64
import glob
import os

from PIL import Image

from src.image.model import Image as ImageDB


def create_dummy_image():
    img = Image.new('RGB', (300, 150), color='red')
    return img


def create_image(image_folder, image_id):
    extension = os.getenv('FILE_EXTENSION')
    img = Image.new('RGB', (300, 150), color='red')
    image_path = f'{image_folder}/{image_id}.{extension}'
    img.save(image_path)


def create_N_images(image_folder, N=3):
    for counter in range(N):
        create_image(image_folder, f'image_{counter}')


def remove_all_images(image_folder):
    files = glob.glob(f'{image_folder}/*')
    for image_path in files:
        os.remove(image_path)


def create_image_encode(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)

    return image_64_encode.decode("utf-8")


def count_images(image_path):
    counter = 0

    for _ in os.listdir(image_path):
        counter += 1

    return counter


def clean_repository_db(repository):
    images = repository._client.session.query(ImageDB).all()
    for image in images:
        repository.remove(str(image.id))