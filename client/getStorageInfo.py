import requests
from settings import URL

"""
http://<URL>/v1/storage (GET)
"""


def get_storage_info():
    resource = f"{URL}v1/storage"
    response = requests.get(url=resource)
    info = response.json()
    print(info)


if __name__ == '__main__':
    get_storage_info()
