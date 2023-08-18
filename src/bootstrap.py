import sqlalchemy as db

from src.config import get_db_config, settings
from src.image.data import ClientSQL, ImageFileSystem
from src.image.repository import ImageRepositoryDB, ImageRepositoryFS

fs = ImageFileSystem(settings.STORAGE_FS, settings.FILE_EXTENSION)
repository_fs = ImageRepositoryFS(fs)

engine = db.create_engine(get_db_config(), future=True)
client = ClientSQL(engine)
repository = ImageRepositoryDB(client)
