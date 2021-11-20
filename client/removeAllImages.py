import requests
from constants import URL

"""
http://<URL>/image/all (DELETE)
"""


def remove_all_images():
    url = f"{URL}image/all"
    response = requests.delete(url=url)
    print(f"URL: {url} - Response: {response.content} - Status Code: {response}")


if __name__ == '__main__':
    remove_all_images()
