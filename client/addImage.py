import requests
import base64
from constants import URL, IMAGE_EXTENSION
"""
http://<URL>/image (POST)
"""


def add_image(image_id):
    url = URL + 'image'
    json_file = dict()
    json_file['id'] = image_id

    image = open(image_id + IMAGE_EXTENSION, 'rb')
    image_read = image.read()
    image_64_encode = base64.b64encode(image_read)
    image_64_encode = image_64_encode.decode("utf-8")

    json_file['image_data'] = image_64_encode

    response = requests.post(url=url, json=json_file)
    print(
        f"URL: {url} - Response: {response.content} - Status Code: {response}")


if __name__ == '__main__':
    image_id = "example"
    add_image(image_id)
