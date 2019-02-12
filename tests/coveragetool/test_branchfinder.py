from pathlib import Path
from coveragetool.branchfinder import BranchFinder

SOURCE_DIR = Path(__file__).parent / Path("sources")

VALIDATOR_PY = SOURCE_DIR / "validator.py"  # "real" source from pyci-backend
LOOPS_PY = SOURCE_DIR / "loops.py"  # artificial source written just for these tests


class TestBranchFinder:
    """Tests for the BranchFinder class."""

    def test_finds_for_and_if(self):
        """Test that BranchFinder finds the for and if statements in
        validator.py.
        """
        validate_python_files_branches = {31, 40, 41, 42, 45, 50}
        _validate_python_branches = {}
        bf = BranchFinder(VALIDATOR_PY)

        assert not bf.branches["_validate_python"]
        assert bf.branches["validate_python_files"] == validate_python_files_branches

    def test_finds_while_for_and_if(self):
        """Test that BranchFinder finds the while, for and if statements in
        loops.py.
        """
        bounded_looping_branches = {8, 10, 13}
        bounded_looping_break_branches = {19, 21, 24, 25}
        bf = BranchFinder(LOOPS_PY)

        assert bf.branches["bounded_looping"] == bounded_looping_branches
        assert bf.branches["bounded_looping_break"] == bounded_looping_break_branches
