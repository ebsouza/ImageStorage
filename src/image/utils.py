import re


def is_image_file(path_to_image):
    if not re.search(f'.jpg', path_to_image):
        return False

    return True
