import requests
from constants import URL
"""
http://<URL>/image/<image_id> (DELETE)
"""


def remove_image(image_id):
    url = f"{URL}image/{image_id}"
    response = requests.delete(url=url)
    print(
        f"URL: {url} - Response: {response.content} - Status Code: {response}")


if __name__ == '__main__':
    image_id = "example"
    remove_image(image_id)
