import pytest

from lektor.utils import decode_flat_data


class TestDecodeFlatData:
    """Tests for utils.decode_flat_data
    Previously tested requirements of decode_flat_data
        - None
    Previously untested but now tested requirements:
        - Works given an empty iterator
        - Returns a correctly structured dictionary given a valid ini data iterator
    Untested requirements:
        - Supports different kinds of dictionary output
    """

    @pytest.fixture
    def empty_ini_data_iter(self):
        return iter([])

    @pytest.fixture
    def ini_data_iter(self):
        return iter([("pygments.style", "tango")])

    def test_decode_empty_data(self, empty_ini_data_iter):
        """Returns an empty dictionary given an empty iterator."""
        assert len(decode_flat_data(empty_ini_data_iter)) == 0

    def test_decode_parsed_ini_data(self, ini_data_iter):
        """Returns a parsed dictionary of the requested type using the given
        data from a valid ini file.
        """
        assert decode_flat_data(ini_data_iter) == {"pygments": {"style": "tango"}}
