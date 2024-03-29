import base64
import binascii
import os
from dataclasses import dataclass
from typing import List

from sqlalchemy.orm import Session

from src.errors import ImageNotFound
from src.image.errors import ImageDecodeError, ImageNotFound
from src.image.model import Image
from src.image.utils import is_image_file


class ClientSQL:

    def __init__(self, engine):
        self.session = Session(engine)

    def add(self, image: Image):
        self.session.add(image)
        self.session.commit()

    def get(self, image_id: str) -> Image:
        image = self.session.query(Image).filter_by(id=image_id).first()
        if image is None:
            raise ImageNotFound
        return image

    def remove(self, image_id: str):
        image = self.get(image_id)
        self.session.delete(image)
        self.session.commit()

    def get_many(self, offset: int = 0, limit: int = 10) -> List[Image]:
        return self.session.query(Image).offset(offset).limit(limit)


class ImageFileSystem:

    def __init__(self, path: str, image_extension: str):
        self._path = path
        self._image_extension = image_extension

    def create(self, image_id: str, image_data: str):
        path_to_image = self._get_path_to_image(image_id)
        try:
            with open(path_to_image, 'wb') as image_created:
                image_64_decoded = base64.decodebytes(
                    image_data.encode('utf-8'))
                image_created.write(image_64_decoded)
        except binascii.Error:
            os.remove(path_to_image)
            raise ImageDecodeError

    def remove(self, image_id: str) -> str:
        try:
            path_to_image = self._get_path_to_image(image_id)
            os.remove(path_to_image)
        except FileNotFoundError:
            raise ImageNotFound

        return image_id

    def remove_all(self) -> List[str]:
        image_ids = list()
        for data in self.images_data:
            os.remove(data['image_path'])
            image_ids.append(data['image_id'])

        return image_ids

    def get(self, image_id: str):
        path_to_image = self._get_path_to_image(image_id)

        try:
            with open(path_to_image, 'rb') as image:
                image_read = image.read()
                image_64_encode = base64.b64encode(image_read)
                encoded_image = image_64_encode.decode("utf-8")

            return encoded_image

        except FileNotFoundError:
            raise ImageNotFound

    def get_all(self, limit: int = 100):
        images = dict()
        for index, data in enumerate(self.images_data):
            if index == limit:
                break

            image_id = data['image_id']

            images[image_id] = self.get(image_id)

        return images

    @property
    def size(self):
        total = 0

        for data in self.images_data:
            total += os.stat(data['image_path']).st_size

        return total / 1000000  # convert to Mb

    @property
    def images_data(self):

        def iterable():
            for filename in os.listdir(self._path):

                if not is_image_file(filename):
                    continue

                data = {
                    'image_path': f'{self._path}/{filename}',
                    'filename': filename,
                    'image_id': filename.rsplit(".", 1)[0]
                }

                yield data

        return iterable()

    def _get_path_to_image(self, image_id: str):
        return f'{self._path}/{image_id}.{self._image_extension}'


@dataclass
class ImageBinary:
    id: str
    image_data: str
