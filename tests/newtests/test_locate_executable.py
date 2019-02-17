import pytest

from lektor import utils


class TestLocateExecutable:
    """Tests for utils.locate_executable
    Previously tested requirements of get_structure_hash:
        - None
    Previously untested but now tested requirements:
        - If global variable lektor._compat.BUNDLE_BIN_PATH is not
        None, add it to paths
    Untested requirements:
        - If global variable lektor._compat.EXTRA_PATHS is not empty,
        add the extra paths to paths
        - If os.name == 'nt', add cwd as path choices
        - Raises OS error
    """

    @pytest.fixture
    def mock_os_access(self, mocker):
        return mocker.patch("os.access", return_value=True)

    @pytest.fixture
    def mock_os_environ_get(self, mocker):
        return mocker.patch("os.environ.get", return_value="")

    def test_bundle_bin_path_not_none(
        self, mock_os_access, mock_os_environ_get, monkeypatch
    ):
        """Test that the BUNDLE_BIN_PATH is added to choices and that path is returned"""
        monkeypatch.setattr("lektor.utils.BUNDLE_BIN_PATH", "test")
        assert utils.locate_executable(".") == "test/."
