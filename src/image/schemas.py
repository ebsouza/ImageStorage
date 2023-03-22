from typing import List

from src.image.model import Image


def get_image_view(images: List[Image]):
    data = list()
    for image in images:
        content = {'id': image.id, 'image_data': image.image_data}
        data.append(content)

    return data
