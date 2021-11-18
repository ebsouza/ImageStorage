import requests
import base64
from constants import URL, IMAGE_EXTENSION

"""
http://<URL>/image (POST)
"""


def add_image(image_id):
    resource = URL + 'image'
    json_file = dict()
    json_file['ID'] = image_id

    image = open(image_id + IMAGE_EXTENSION, 'rb')
    image_read = image.read()
    image_64_encode = base64.encodestring(image_read)
    image_64_encode = image_64_encode.decode("utf-8")

    json_file['image_data'] = image_64_encode

    r = requests.post(url=resource, json=json_file)
    print(r)


if __name__ == '__main__':
    image_id = "example"
    add_image(image_id)
