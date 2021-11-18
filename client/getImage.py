import requests
import base64
from constants import URL, IMAGE_EXTENSION

"""
http://<URL>/image/<image_id> (GET)
"""

def get_image(image_id):
    resource = f"{URL}image/{image_id}"
    r = requests.get(url=resource)
    image_json = r.json()

    image_64_encode = image_json['image_data']
    image_64_encode = image_64_encode.encode("utf-8")
    image_64_decode = base64.decodebytes(image_64_encode)

    fileName = image_json['ID'] + IMAGE_EXTENSION

    with open(fileName, 'wb') as image_result:
        image_result.write(image_64_decode)

    print(r)


if __name__ == '__main__':
    image_id = "example"
    get_image(image_id)
