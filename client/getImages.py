import requests
from constants import URL

"""
http://<URL>/image/all (GET)
"""


def recover_images():
    resource = f"{URL}image/all"
    r = requests.get(url=resource)
    image_list = r.json()
    print(image_list)
    print(r)


if __name__ == '__main__':
    recover_images()
