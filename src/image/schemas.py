from pydantic import BaseModel


class Image(BaseModel):
    id: str
    image_data: str

    @classmethod
    def create_list(cls, ids: list, encoded_images: list):
        data = list()
        for id, encoded_image in zip(ids, encoded_images):
            content = {'id': id, 'image_data': encoded_image}
            data.append(content)

        return data
