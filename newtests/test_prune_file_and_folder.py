import os

import pytest

from lektor.utils import prune_file_and_folder


class TestPruneFileAndFolder:
    @pytest.fixture
    def valid_file_structure(self, tmp_path):
        """Constructs a valid file structure which should make the
        prune_file_and_folder method return True.
        """
        base = tmp_path
        dir1 = base / "dir1"
        dir1_file = dir1 / "file"
        dir2 = dir1 / "dir2"
        dir3 = dir2 / "dir3"
        dir1.mkdir()
        dir1_file.touch()
        dir2.mkdir()
        dir3.mkdir()
        return base, dir1, dir2, dir3

    def test_prune_file_unsafe_to_delete(self, tmp_path):
        """Returns Flase if given path is not safe to delete based on the given
        base path.

        This happens when the path is not a child of the base path in the
        hierarchy.
        """
        path = tmp_path / "abc"
        base = tmp_path / "def"
        assert not prune_file_and_folder(path, base)

    def test_prune_folder_safe_to_delete_returns_true(self, valid_file_structure):
        """Returns True given arguments that allows pruning the file structure
        without encountering directories that are unsafe to delete.
        """
        base, _, _, dir3 = valid_file_structure
        assert prune_file_and_folder(dir3, base)

    def test_prune_folder_safe_to_delete_expected_side_effects(
        self, valid_file_structure
    ):
        """A function call with a valid file structure results in the expected
        side effects.

        The example structure consists of a base directory with three layers of
        subdirectories, of the form 'base -> dir1 -> dir2 -> dir3', where dir1
        also contains a file.  Given this file structure, the function should
        delete the two deepest directories, dir3 and dir2, and leave the
        shallowest subdirectory, dir1, because it is not empty after removing
        its child directory, dir2.
        """
        base, dir1, dir2, dir3 = valid_file_structure
        prune_file_and_folder(dir3, base)
        assert not dir3.exists()
        assert not dir2.exists()
        assert dir1.exists()
        assert os.listdir(dir1)
