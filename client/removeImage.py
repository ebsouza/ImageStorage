import requests
from constants import URL

"""
http://<URL>/image/<image_id> (DELETE)
"""


def remove_image(image_id):
    resource = f"{URL}image/{image_id}"
    r = requests.delete(url=resource)
    print(r)


if __name__ == '__main__':
    image_id = "example"
    remove_image(image_id)
