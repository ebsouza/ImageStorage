import base64

import requests
from constants import IMAGE_EXTENSION, URL

"""
http://<URL>/image/<image_id> (GET)
"""


def get_image(image_id):
    resource = f"{URL}image/{image_id}"
    response = requests.get(url=resource)

    data = response.json()[0]

    image_64_encode = data['image_data']
    image_64_encode = image_64_encode.encode("utf-8")
    image_64_decode = base64.decodebytes(image_64_encode)

    file_name = data['id'] + IMAGE_EXTENSION

    with open(file_name, 'wb') as image_result:
        image_result.write(image_64_decode)

    print(response)


if __name__ == '__main__':
    image_id = "example"
    get_image(image_id)
