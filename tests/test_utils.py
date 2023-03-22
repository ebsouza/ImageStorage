from src.image.utils import is_image_file


class TestUtils:

    def test_is_image_file_correct_extension(self):
        paht_to_image = 'path/to/image/fake_image_id.jpg'

        assert is_image_file(paht_to_image)

    def test_is_image_file_incorrect_extension(self):
        paht_to_image_1 = 'path/to/image/fake_image_id.xpto'
        paht_to_image_2 = 'path/to/image/.xpto_file'

        assert not is_image_file(paht_to_image_1)
        assert not is_image_file(paht_to_image_2)
