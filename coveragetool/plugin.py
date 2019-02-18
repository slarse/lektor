"""A local pytest plugin for the coveragetool package.

The plugin is hardcoded to trace the specific files and functions that we are looking at
in this project. It could be slightly extended to become a general pytest plugin, but
there is really no call for that here.

.. module:: plugin
    :synopsis: A local pytest plugin for the coveragetool package.

.. moduleauthor:: Simon Larsén
"""
from pathlib import Path

import lektor

from coveragetool.branchfinder import BranchFinder
from coveragetool.branchtracer import BranchTracer, func_id


LEKTOR_DIR = Path(lektor.__file__).parent
UTILS = LEKTOR_DIR / "utils.py"
FLOW = LEKTOR_DIR / "types" / "flow.py"
METAFORMAT = LEKTOR_DIR / "metaformat.py"
CLI = LEKTOR_DIR / "cli.py"
IMAGETOOLS = LEKTOR_DIR / "imagetools.py"
DB = LEKTOR_DIR / "db.py"
FILES = [UTILS, FLOW, DB, IMAGETOOLS, METAFORMAT, CLI]

FUNC_IDS = [
    func_id(func, filepath)
    for func, filepath in [
        ("discover_relevant_flowblock_models", FLOW),
        ("decode_flat_data", UTILS),
        ("prune_file_and_folder", UTILS),
        ("tokenize", METAFORMAT),
        ("merge", UTILS),
        ("get_structure_hash", UTILS),
        ("_hash", UTILS),
        ("locate_executable", UTILS),
        ("content_file_info_cmd", CLI),
        ("coerce", DB),
        ("get_image_info", IMAGETOOLS),
    ]
]


def _create_tracer(files, func_ids):
    """Creates a BranchTracer tracing the given files, and filtering the output
    by the given function ids.
    """
    bfs = [BranchFinder(file) for file in files]
    return BranchTracer.from_branchfinders(*bfs)


def create_hook_methods():
    """Creates and returns the pytest_runtest_call, pytest_runtest_teardown and
    pytest_sessionfinish hook methods. The reason it is done in a method is to
    keep side effects from importing this module minimal.
    """

    tracer = _create_tracer(FILES, FUNC_IDS)

    def pytest_runtest_call(item):
        """Called before every test to activate tracing."""
        tracer.start_trace()

    def pytest_runtest_teardown(item):
        """Called after every test to stop tracing."""
        tracer.stop_trace()

    def pytest_sessionfinish(session, exitstatus):
        """Prints out the results after the pytest session is done."""
        from pprint import pprint

        print()
        pprint(tracer.function_coverage(*FUNC_IDS))

    return pytest_runtest_call, pytest_runtest_teardown, pytest_sessionfinish
