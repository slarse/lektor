"""A class for tracing branch execution.

.. module:: branchtracer
    :synopsis: A class for tracing branch execution.

.. moduleauthor:: Simon Larsén
"""
import os
import sys
from itertools import chain
from collections import defaultdict
from coveragetool.branchfinder import BranchFinder


def func_id(function_name: str, filepath: str) -> str:
    """Return a unique id (unique on this system!) for the given function name,
    assuming the function name is unique in the python file at filepath.

    Args:
        function_name: Name of a function.
        filepath: Absolute path to the file containing the function.
    Return:
        A system-unique id for the function.
    """
    return f"{function_name}@{filepath}"


class BranchTracer:
    """Class for tracing branch executions for select files.

    Must be provided with a pre-computed nested dictionary containing mappings
    (filepath -> (function_name -> line_nr_with_conditional)). Can be computed
    for example with the BranchFinder class. The filepaths in this dictionary
    are the only ones that will be traced. Tracing works only for conditional
    statements that are contained on a single line. Multi-line statements
    cause undefined behavior.

    In addition to the constructor, the static method ``from_branchfinders`` can
    be used to create a BranchTracer directly from a variable amount of
    BranchFinders.

    Tracing is started and stopped with the ``start_trace`` and ``stop_trace``
    methods, which sets and unsets the global trace function using
    ``sys.settrace``.
    """

    def __init__(self, branches: dict):
        """
        Args:
            branches: A nested dictionary on the form
            (filepath -> (function_name -> set(line_nrs_with_conditional))).
        """
        self._filepaths = list(branches.keys())

        # mapping on the from (filepath -> set(line_nrs_with_conditional)
        self._lines_with_condition = {
            filepath: set(chain.from_iterable(branches.values()))
            for filepath, branches in branches.items()
        }

        # mapping on the form
        # (function_id -> (line_nr_with_cond -> set(lines_jumped_to)))
        self._branches_taken = {
            func_id(func_name, filepath): {branch: set() for branch in branches}
            for filepath, func_dicts in branches.items()
            for func_name, branches in func_dicts.items()
        }

        self._prev_line = dict()

    def start_trace(self):
        """Start tracing any code execution within the target files."""
        sys.settrace(self._global_tracefunction)

    def stop_trace(self):
        """Stop tracing code execution."""
        sys.settrace(None)

    def function_coverage(self, *function_ids: str) -> dict:
        """Get function coverage from everything traced so far as a nested
        dictionary mapping function ids (as defined by the func_id function)
        to dictionaries containing (line_nr_with_cond -> set of line nrs jumped
        to) mappings.

        The nested structure is thus:

            (function_id ->
                (line_nr_widh_cond -> set(line_nrs_jumped_to))
            )

        Args:
            function_ids: A vararg of function id's to filter by. If no
                function ids are provided, output is not filtered.
        Return:
            A nested dictionary mapping (function_id ->
            (line_nr_with_cond -> set of line nrs jumped to))
        """
        return {
            id_: self._remove_loop_self_jumps(branches)
            for id_, branches in self._branches_taken.items()
            if not function_ids or id_ in function_ids
        }

    @staticmethod
    def from_branchfinders(*bfs: BranchFinder):
        """Create a BranchTracer tracing the files in one or more
        BranchFinders.

        Arg:
            bfs: A vararg of BranchFinders on unique files.
        Return:
            A BranchTracer that can trace the execution of branches in the
            provided BranchFinders.
        """
        branches = {bf.filepath: bf.branches for bf in bfs}
        return BranchTracer(branches)

    def _global_tracefunction(self, frame, event, arg):
        """The global trace function is called when a new scope is entered.
        Delegates to the local tracefunction for any call made within one of
        the targeted filepaths.

        Args:
            frame: A stack frame.
            event: Type of event (should only be 'call' for entering a new
                scope and possibly 'exception' at the module level)
            arg: Arguments passed to a call event.
        Return:
            The local tracefunction if the scope should be traced, otherwise None.
        """
        try:
            filepath = os.path.abspath(frame.f_code.co_filename)
        except AttributeError:
            # os.path is None sometimes when running pytest, don't now how this happens
            return

        if filepath in self._filepaths:
            return self._local_tracefunction

    def _local_tracefunction(self, frame, event, arg):
        """The local trace function that is called for each line in a local
        scope.  Uses the _prev_line dictionary to keep track of the previous
        line on a per-stack frame basis.

        Args:
            frame: A stack frame.
            event: Type of event (every event type but 'call').
            arg: Arguments passed to a call event.
        Return:
            The local tracefunction (i.e. itself) for further tracing.
        """
        if not frame in self._prev_line:
            # first time this frame appears, no previous line!
            self._prev_line[frame] = frame.f_lineno
            return self._local_tracefunction

        filepath = os.path.abspath(frame.f_code.co_filename)
        if self._prev_line[frame] in self._lines_with_condition[filepath]:
            id_ = func_id(frame.f_code.co_name, filepath)
            if not id_ in self._branches_taken:  # anonymous function!
                self._branches_taken[id_] = defaultdict(set)
            self._branches_taken[id_][self._prev_line[frame]].add(frame.f_lineno)

        if event == "return":  # done with this stack frame
            del self._prev_line[frame]
        else:
            self._prev_line[frame] = frame.f_lineno

        return self._local_tracefunction

    @staticmethod
    def _remove_loop_self_jumps(branches):
        """Lops may sometimes "jump" to themselves even when they are not the
        last statement. I am unsure why. Any branching with three jumps is
        a sign of this, and should be trimmed to two jumps.

        If the branching statement is the last statment in its block, it is
        expected to jump to itself, but then there will only be two jumps.
        """
        out = {}
        for branch_line_nr, jumps in branches.items():
            if len(jumps) > 2:
                out[branch_line_nr] = jumps - {branch_line_nr}
            else:
                out[branch_line_nr] = set(jumps)
        return out
