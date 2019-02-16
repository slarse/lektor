from unittest.mock import patch, MagicMock
from coveragetool import plugin


def test_create_hook_methods():
    """Happy path test of create_hook_methods asserting that the hook methods are
    callable and the _create_tracer method is called once with the correct args.
    """
    with patch(
        "coveragetool.plugin._create_tracer", autospec=True, callable=MagicMock
    ) as mock_create_tracer:
        pytest_runtest_call, pytest_runtest_teardown, pytest_sessionfinish = (
            plugin.create_hook_methods()
        )

    assert callable(pytest_runtest_call)
    assert callable(pytest_runtest_teardown)
    assert callable(pytest_sessionfinish)
    mock_create_tracer.assert_called_once_with(plugin.FILES, plugin.FUNC_IDS)
