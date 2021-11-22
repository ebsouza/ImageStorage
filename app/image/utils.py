import os
import base64
from PIL import Image


def create_dummy_image(image_path, extension=".jpg"):
    img = Image.new('RGB', (300, 150), color='red')
    file_name = image_path + extension
    img.save(file_name)


def create_image_encode(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)

    return image_64_encode.decode("utf-8")


def get_total_images(path):
    try:
        path, dirs, files = next(os.walk(path))
    except Exception as e:
        print('I wasnt possible to open images .Reason: %s' % (e))

    return len(files)
