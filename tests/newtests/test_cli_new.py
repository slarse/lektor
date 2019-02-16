from pathlib import Path
import pytest
from lektor.cli import cli


@pytest.fixture
def project_root():
    return Path(__file__).parent.parent / "demo-project"


@pytest.fixture
def contents_file(project_root):
    return project_root / "content" / "contents.lr"


class TestContentFileInfoCmd:
    """Tests for lektor.cli.content_file_info_cmd.

    This function was untested in the initial test suite.
    """

    CMD = "content-file-info"

    @pytest.fixture
    def project_info(self, project_root):
        """This project info is always printed for content-file-info."""
        return [
            "Name: Demo Project",
            f"File: {project_root}/Website.lektorproject",
            f"Tree: {project_root}",
        ]

    def test_errors_when_no_filepath_provided(self, project_cli_runner):
        """Test that an error is emitted if no file is provided."""
        result = project_cli_runner.invoke(cli, [self.CMD])
        assert "Usage: cli content-file-info [OPTIONS] [FILES]" in result.output
        assert (
            "Error: Could not find content file info: no file indicated a project"
            in result.output
        )

    def test_errors_when_files_from_different_projects_provided(
        self, project_cli_runner, contents_file, project_root
    ):
        """Test that providing files from different projects causes an error to be emitted."""
        other_project_contents_file = (
            project_root.parent / "dependency-test-project" / "content" / "contents.lr"
        )
        result = project_cli_runner.invoke(
            cli, [self.CMD, str(contents_file), str(other_project_contents_file)]
        )
        assert (
            "Error: Could not find content file info: multiple projects"
            in result.output
        )

    def test_errors_when_provided_file_is_not_lektor_file(
        self, project_cli_runner, tmpdir
    ):
        """Test that an error is emitted if a provided filepath is not part of
        a Lektor project.
        """
        file = tmpdir.join("somefile.lr")

        result = project_cli_runner.invoke(cli, [self.CMD, str(file)])

        assert (
            "Error: Could not find content file info: no project found" in result.output
        )

    def test_prints_info_when_valid_filepath_provided(
        self, project_cli_runner, contents_file, project_info
    ):
        """Test that the correct info is printed when a filepath to a valid
        project file is provided.
        """
        result = project_cli_runner.invoke(cli, [self.CMD, str(contents_file)])
        assert "Name: Demo Project" in result.output
        for line in project_info:
            assert line in result.output
