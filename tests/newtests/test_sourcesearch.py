import pytest

from lektor import sourcesearch
from lektor.environment import PRIMARY_ALT


def _formatted_query_string(sql_cursor):
    """get the final formatted query string used to execute the given mocked sql cursor"""
    sql_query = sql_cursor.execute.call_args_list[0][0]
    query_string = sql_query[0]
    query_params = sql_query[1]
    res = query_string
    for param in query_params:
        res = res.replace("?", str(param), 1)
    return res


class TestFindFiles:
    """Previously tested requirements of find_files:
        - None
    Previously untested but now tested requirements:
        - Query only files with type in the given types.
        - Query only page files if no types are provided.
        - If a language is provided, query only files that are in either English or that language.
        - If no language is provided, query only English files.
        - If an alt is provided, query only files with the alt PRIMARY_ALT or the provided alt.
    Untested requirements:
        - If the database query errors out, do not return.
        - If the database query is successful, query every file with a name or path that includes
          the given query as a substring, and that satisfies the above constraints.
    """

    @pytest.fixture
    def expected_db_name(self):
        return "dbname"

    @pytest.fixture
    def mock_builder(self, mocker, expected_db_name):
        return mocker.MagicMock(buildstate_database_filename=expected_db_name)

    @pytest.fixture
    def mock_sql_cursor(self, mocker):
        return mocker.MagicMock(execute=mocker.MagicMock())

    @pytest.fixture
    def mock_sql_connection(self, mocker, mock_sql_cursor):
        return mocker.MagicMock(cursor=mocker.MagicMock(return_value=mock_sql_cursor))

    @pytest.fixture
    def mock_sql_connect(self, mocker, mock_sql_connection):
        return mocker.patch(
            "sqlite3.connect", autospec=True, return_value=mock_sql_connection
        )

    def test_query_only_given_types(
        self, mock_builder, mock_sql_connect, mock_sql_cursor
    ):
        """Test that the SQL query for the files only includes the provided types"""
        expected_types = ["type1", "type2"]
        sourcesearch.find_files(mock_builder, "query", types=expected_types)
        query = _formatted_query_string(mock_sql_cursor)
        expected_type_string = ", ".join(expected_types)
        assert f"type in ({expected_type_string})" in query

    def test_query_only_pages_if_no_types(
        self, mock_builder, mock_sql_connect, mock_sql_cursor
    ):
        """Test that the SQL query for the files only includes the "page" type if no types were
        provided
        """
        sourcesearch.find_files(mock_builder, "query")
        query = _formatted_query_string(mock_sql_cursor)
        assert f"type in (page)" in query

    def test_query_only_given_lang_and_english(
        self, mock_builder, mock_sql_connect, mock_sql_cursor
    ):
        """Test that the SQL query for the files only includes the given language and English"""
        lang = "sv"
        expected_langs = ["en", "sv"]
        sourcesearch.find_files(mock_builder, "query", lang=lang)
        query = _formatted_query_string(mock_sql_cursor)
        expected_lang_string = ", ".join(expected_langs)
        assert f"lang in ({expected_lang_string})" in query

    def test_query_only_english_if_no_langs(
        self, mock_builder, mock_sql_connect, mock_sql_cursor
    ):
        """Test that the SQL query for the files only includes English if no language was
        provided
        """
        expected_lang = "en"
        sourcesearch.find_files(mock_builder, "query")
        query = _formatted_query_string(mock_sql_cursor)
        assert "lang in (en)" in query

    def test_query_both_primary_alt_and_provided_alt(
        self, mock_builder, mock_sql_connect, mock_sql_cursor
    ):
        """Test that the SQL query for the files includes both PRIMARY_ALT and the provided alt"""
        alt = "my_alt"
        sourcesearch.find_files(mock_builder, "query", alt=alt)
        query = _formatted_query_string(mock_sql_cursor)
        assert f"alt in ({PRIMARY_ALT}, {alt})" in query
