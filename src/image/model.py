from pydantic import BaseModel


class Image(BaseModel):
    id: str
    image_data: str
