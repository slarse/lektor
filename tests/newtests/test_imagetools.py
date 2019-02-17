from pathlib import Path

from lektor.imagetools import get_image_info


class TestGetImageInfo:
    """Tests for imagetools.get_image_info. This function should return a tuple of
    (filetype, width, height) for a file descriptor pointing to an image.

    Previously tested requirements:

    * Delegates svg and xml filetypes to ``get_svg_info``
    * Correctly reads the information from a well-formed JPEG image.

    Previously untested requirements:

    * Raises an exception for a malformed JGEP image.
    * Raises an exception if a JPEG image includes DNL (define number of lines)
    * Correctly reads info from a well-formed PNG image.
    * Correctly reads info from a well-formed GIF image.
    * Returns ``(None, None, None)`` if the filetype cannot be identified.

    The requirements tested by these new tests are specified in the tests.
    """

    IMAGE_DIR = Path(__file__).parent / "images"

    GIF_IMAGE = IMAGE_DIR / "hello_world.gif"
    PNG_IMAGE = IMAGE_DIR / "locate_executable_cov.png"

    # image info in the form (filetype, width, height)
    GIF_IMAGE_INFO = ("gif", 1920, 1080)
    PNG_IMAGE_INFO = ("png", 917, 549)

    def test_parses_well_formed_png_correctly(self):
        """Test that the image info for a well-formed PNG image is parsed correctly."""
        with open(str(self.PNG_IMAGE), mode="rb") as image:
            info = get_image_info(image)

        assert info == self.PNG_IMAGE_INFO

    def test_parses_well_formed_gif_correctly(self):
        """Test that the image info for a well-formed GIF image is parsed correctly."""
        with open(str(self.GIF_IMAGE), mode="rb") as image:
            info = get_image_info(image)

        assert info == self.GIF_IMAGE_INFO

    def test_returns_all_none_for_unsupported_file(self):
        """Test that the image info is all None for an unsupported file (here, .py)."""
        with open(__file__, mode="rb") as file:
            info = get_image_info(file)

        assert info == (None,) * 3
