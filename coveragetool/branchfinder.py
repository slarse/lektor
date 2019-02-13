"""A class for finding branch statements in a Python source file.

.. module:: branchfinder
    :synopsis: A class for finding branch statements in a Python source file.

.. moduleauthor:: Simon Larsén
"""
import sys
import os
import ast
import collections


class BranchFinder(ast.NodeVisitor):
    """Traverses the AST of a Python source file and finds all lines containing
    branch statements `if`, `while` and `for`. One instance of BranchFinder
    operates on a single Python source file, and is after that useless.

    The visit_<NODE_TYPE> functions are automatically called upon visiting a
    node of type NODE_TYPE. The conditionals simply add the line number to
    branches[cur_func], where cur_func is the function currently
    in scope. visit_FunctionDef is the only exception, it only tracks function
    scopes for the other visit functions to use.

    Attributes:
        branches: A defaltdict(set), where the key is a function name and the value
            a set of all line numbers with conditional statments in that function.

    TODO add support for try/except/else/finally
    """

    def __init__(self, filepath: str):
        """
        Note:
            All processing on the AST done by the BranchFinder class is
            performed during initialization.

        Args:
            filepath: Path to the file to find branches in.
        """
        super().__init__()
        self.branches = collections.defaultdict(set)
        self._current_function = ""
        tree = self._parse_file(os.path.abspath(filepath))
        self.visit(tree)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        """Visit a FunctionDef node and store the context in
        self.current_function. This is required to be able to do the mapping of
        function to line number.

        Restore the context when the FunctionDef is exited.

        Args:
            node: An function definition.
        """
        enclosing_function = self._current_function
        self._current_function = node.name
        self.generic_visit(node)
        self._current_function = enclosing_function

    def visit_If(self, node: ast.If):
        self._visit_and_register(node)

    def visit_For(self, node: ast.For):
        self._visit_and_register(node)

    def visit_While(self, node: ast.While):
        self._visit_and_register(node)

    def _visit_and_register(self, node: ast.Expression):
        """Register a node in the branches dictionary. Any node with a line
        number will work, but it should be a conditional node for it to make
        sense.
        """
        self.branches[self._current_function].add(node.lineno)
        self.generic_visit(node)

    @staticmethod
    def _parse_file(filepath: str):
        """Parse the file to an AST."""
        with open(filepath, mode="r", encoding=sys.getdefaultencoding()) as f:
            return ast.parse(f.read())
