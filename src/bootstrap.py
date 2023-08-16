#import os
import sqlalchemy as db

from src.config import load_config
from src.image.data import ImageFileSystem, ClientSQL
from src.image.repository import ImageRepositoryDB, ImageRepositoryFS

PATH_TO_IMAGE = load_config().get('storage')
IMAGE_EXTENSION = load_config().get('file_extension')

fs = ImageFileSystem(PATH_TO_IMAGE, IMAGE_EXTENSION)
repository_fs = ImageRepositoryFS(fs)


#engine = db.create_engine("sqlite:///database.db", echo=True, future=True)
engine = db.create_engine(load_config().get('database'), future=True)
client = ClientSQL(engine)
repository = ImageRepositoryDB(client)
