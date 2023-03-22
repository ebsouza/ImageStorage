from src.config import load_config
from src.image.data import ImageFileSystem
from src.image.repository import ImageRepository

PATH_TO_IMAGE = load_config()['storage']
IMAGE_EXTENSION = load_config()['file_extension']

fs = ImageFileSystem(PATH_TO_IMAGE, IMAGE_EXTENSION)
repository = ImageRepository(fs)
