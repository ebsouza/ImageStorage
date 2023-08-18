import re

from src.config import settings


def is_image_file(path_to_image):
    file_extension = settings.FILE_EXTENSION
    if not re.search(f'.{file_extension}', path_to_image):
        return False

    return True
