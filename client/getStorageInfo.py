import requests
from constants import URL

"""
http://<URL>/info (GET)
"""


def get_storage_info():
    resource = f"{URL}info"
    r = requests.get(url=resource)
    info = r.json()
    print(info)


if __name__ == '__main__':
    get_storage_info()
