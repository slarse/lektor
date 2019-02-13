"""Build validator module for pyci_backend.

.. module:: settings
    :platform: Linux
    :synopsis: Build validator module for pyci_backend.
.. moduleauthor:: Martin Nilsson <mnil2@kth.se>
"""
import os
import sys
import subprocess


def validate_python_files(topdirpath: str, verbose: bool = False) -> bool:
    """Static syntax check of all python modules in the directory tree.

    Recursively iterates through each subdirectory to find modules to check. Checks any
    file that ends with ".py". By default, only reports failed checks. But if verbose
    is set to True, this function will report all checks.

    Uses flake8 to find errors in each module. Errors are set so that it tries not to
    emit false positives and does not consider style.

    Args:
        topdirpath: The directory.
        verbose: Whether to report every check, not just failed ones.
    Returns:
        Whether all the modules passed the check.
    Raises:
        NotADirectoryError if topdirpath is not a directory.
    """
    if not os.path.isdir(topdirpath):
        raise NotADirectoryError(f"{topdirpath} is not a directory")

    def walk_error(oserror: OSError):
        sys.stderr.write(
            f'unexpected os error while walking directory tree at "{oserror.filename}"'
        )

    all_valid = True
    for dirpath, _, filenames in os.walk(topdirpath, onerror=walk_error):
        for filename in filenames:
            if not filename.endswith(".py"):
                continue
            filepath = os.path.join(dirpath, filename)
            if verbose:
                relative_filepath = os.path.relpath(
                    filepath, start=os.path.dirname(topdirpath)
                )
                print(f'checking module "{relative_filepath}"')
            if not _validate_python(filepath):
                all_valid = False
    return all_valid


def _validate_python(filepath: str) -> bool:
    """Static syntax check of a python module using flake8."""
    result = subprocess.run(
        [
            "flake8",
            filepath,
            "--select=F,E999",
            "--ignore=F401,F402,F403,F404,F405,F406,F632,F811,F812,F841",
        ],
        capture_output=True,
    )
    print(result.stdout.decode(encoding=sys.getdefaultencoding()))
    print(result.stderr.decode(encoding=sys.getdefaultencoding()), file=sys.stderr)
    return result.returncode == 0
