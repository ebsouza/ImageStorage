import requests
from settings import URL

"""
http://<URL>/v1/images (DELETE)
"""


def remove_all_images():
    url = f"{URL}v1/images"
    response = requests.delete(url=url)
    print(
        f"URL: {url} - Response: {response.content} - Status Code: {response}")


if __name__ == '__main__':
    remove_all_images()
