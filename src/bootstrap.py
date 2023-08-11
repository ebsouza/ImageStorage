import sqlalchemy as db

from src.config import load_config
from src.image.data import ImageFileSystem, ClientSQL
from src.image.repository import ImageRepository, ImageRepositoryFS

PATH_TO_IMAGE = 'Storage'#load_config()['storage']
IMAGE_EXTENSION = 'jpg'#load_config()['file_extension']

fs = ImageFileSystem(PATH_TO_IMAGE, IMAGE_EXTENSION)
repository_fs = ImageRepositoryFS(fs)


#engine = db.create_engine("sqlite:///database.db", echo=True, future=True)
engine = db.create_engine("sqlite:///database.db", future=True)
client = ClientSQL(engine)
repository = ImageRepository(client)
