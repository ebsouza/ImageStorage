import base64
import os

from PIL import Image

from instance.config import app_config

app_settings = os.getenv('APP_SETTINGS', 'testing')
PATH_TO_IMAGE = app_config[app_settings][1]
IMAGE_EXTENSION = os.getenv('FILE_EXTENSION', '.jpg')


def create_dummy_image(image_path, extension=".jpg"):
    img = Image.new('RGB', (300, 150), color='red')
    file_name = image_path + extension
    img.save(file_name)


def create_image_encode(image_path):
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.encodebytes(image_read)

    return image_64_encode.decode("utf-8")


#def get_total_images(path):
#    try:
#        _, _, files = next(os.walk(path))
#
#        files = [file for file in files if is_image_file(file)]
#
#    except Exception as e:
#        print("Error: %s" % (e))
#
#    return len(files)
#
#
#def get_total_size(path):
#    try:
#        path, dirs, files = next(os.walk(path))
#        total_size = 0
#        for file in files:
#
#            if not is_image_file(file):
#                continue
#
#            file_path = path + file
#            total_size += os.stat(file_path).st_size
#        total_size = total_size / 1000000  # convert to Mb
#    except Exception as e:
#        print("Error: %s" % (e))
#
#    return total_size


def is_image_file(path):
    return path.rsplit(".")[0] != ''


def encode_image(image_id):
    image_path = PATH_TO_IMAGE + image_id + IMAGE_EXTENSION
    with open(image_path, 'rb') as image:
        image_read = image.read()
        image_64_encode = base64.b64encode(image_read)
        image_64_encode = image_64_encode.decode("utf-8")

    return image_64_encode


def decode_image(image_encoded):
    image_64_encode = image_encoded
    image_64_encode = image_64_encode.encode("utf-8")

    return base64.decodebytes(image_64_encode)