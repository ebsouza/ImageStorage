import requests
from constants import URL

"""
http://<URL>/image/all (DELETE)
"""


def remove_all_images():
    resource = f"{URL}image/all"
    r = requests.delete(url=resource)
    print(r)


if __name__ == '__main__':
    remove_all_images()
