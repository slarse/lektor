import importlib.util
from pathlib import Path
from unittest.mock import MagicMock
import pytest
from coveragetool.branchtracer import BranchTracer, func_id

SOURCE_DIR = Path(__file__).parent / "sources"

VALIDATOR_PY = SOURCE_DIR / "validator.py"  # "real" source from pyci-backend
LOOPS_PY = SOURCE_DIR / "loops.py"  # artificial source written just for these tests


def load_module_by_filepath(modulename, filepath):
    # from example at SO:
    # https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
    spec = importlib.util.spec_from_file_location("", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


validator = load_module_by_filepath("validator", VALIDATOR_PY)
loops = load_module_by_filepath("loops", LOOPS_PY)


@pytest.fixture
def mock_validate_python(mocker):
    """Manual mocking as dynamically imported modules are apparently difficult
    to patch with mocker.patch.
    """
    orig = validator._validate_python
    mock = MagicMock()
    validator._validate_python = mock
    yield mock
    validator._validate_python = orig


@pytest.fixture
def validator_branches():
    """Return a nested branch dictionary mapping filepath -> function ->
    branch_line_nrs of validator.py
    """
    return {str(VALIDATOR_PY): {"validate_python_files": {40, 41, 42, 45, 50, 31}}}


@pytest.fixture
def loops_branches():
    """Return a nested branch dictionary mapping filepath -> function ->
    branch_line_nrs of loops.py
    """
    return {
        str(LOOPS_PY): {
            "bounded_looping": {8, 10, 13},
            "bounded_looping_break": {24, 25, 19, 21},
        }
    }


class TestBranchTracer:
    """Tests for the BranchFinder class."""

    def test_trace_validator_when_files_validate_true(
        self, mock_validate_python, validator_branches
    ):
        """Test tracing the validator.validate_python_files function when
        the files are valid (i.e. _validate_python returns True).
        """
        mock_validate_python.return_value = True
        expected_coverage = {
            func_id("validate_python_files", str(VALIDATOR_PY)): {
                31: {34},
                40: {41, 52},
                41: {40, 42},
                42: {43, 44},
                45: {50},
                50: {41},
            }
        }
        tracer = BranchTracer(validator_branches)

        tracer.start_trace()
        validator.validate_python_files(str(SOURCE_DIR))
        tracer.stop_trace()

        assert tracer.function_coverage() == expected_coverage

    def test_trace_loops_partial_coverage(self, loops_branches):
        """Test tracing both functions in loops.py with calls that should result
        in partial coverage.
        """
        expected_coverage = {
            func_id("bounded_looping", str(LOOPS_PY)): {
                8: {10},
                10: {12},
                13: {13, 14},
            },
            func_id("bounded_looping_break", str(LOOPS_PY)): {
                19: {21},
                21: {23},
                24: {25},
                25: {26, 28},
            },
        }
        tracer = BranchTracer(loops_branches)

        tracer.start_trace()
        loops.bounded_looping(5, 10)
        loops.bounded_looping_break(5, 10)
        tracer.stop_trace()

        assert tracer.function_coverage() == expected_coverage

    def test_trace_loops_full_coverage(self, loops_branches):
        """Test tracing both functions in loops.py with calls that should
        result in full coverage, except for the while-true which can't do
        anything but enter the loop.
        """
        expected_coverage = {
            func_id("bounded_looping", str(LOOPS_PY)): {
                8: {9, 10},
                10: {11, 12},
                13: {13, 14},
            },
            func_id("bounded_looping_break", str(LOOPS_PY)): {
                19: {20, 21},
                21: {22, 23},
                24: {25},  # while true, can't go anywhere else!
                25: {26, 28},
            },
        }
        tracer = BranchTracer(loops_branches)

        tracer.start_trace()
        for n, limit in [(5, 10), (10, 5), (5, -1)]:
            loops.bounded_looping(n, limit)
            loops.bounded_looping_break(n, limit)

        assert tracer.function_coverage() == expected_coverage
