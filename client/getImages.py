import base64

import requests
from client.settings import IMAGE_EXTENSION, URL

"""
http://<URL>/image/all (GET)
"""


def recover_images():
    resource = f"{URL}image"
    response = requests.get(url=resource)

    for data in response.json()['data']:
        image_64_encode = data['image_data']
        image_64_encode = image_64_encode.encode("utf-8")
        image_64_decode = base64.decodebytes(image_64_encode)

        file_name = data['id'] + IMAGE_EXTENSION

        with open(file_name, 'wb') as image_result:
            image_result.write(image_64_decode)

    print(response)


if __name__ == '__main__':
    recover_images()
