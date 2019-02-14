import pytest

from lektor.types import flow


class TestDiscoverReleventFlowblockModels:
    """Previously tested requirements of discover_relevant_flowblock_models:
        - None
    Previously untested but now tested requirements:
        - If no list of flowblock names is provided, return all flowblocks.
        - If there are no flowblocks in the pad, return an empty dictionary.
    Untested requirements:
        - If the pad has a flowblock with a name that is not given, it is not returned.
        - If a flowblock name is given that doesn't exist in the pad flowblocks, it is not returned.
        - If two identical flowblock names are given and it exists in the pad flowblocks, that
          flowblock is only returned once.
        - If a matching flowblock contains a nested flow that contains matching flowblocks, these
          flowblocks are also returned.
        - If a matching flowblock contains a nested flow that is empty, raise RuntimeError.
    """

    @pytest.fixture
    def expected_all_flowblocks(self):
        return {
            "key0": "val0",
            "key1": "val1",
            "key2": "val2",
            "key3": "val3",
            "key4": "val4",
        }

    @pytest.fixture
    def mock_all_flowblocks(self, mocker, expected_all_flowblocks):
        flowblocks = {}
        for k, v in expected_all_flowblocks.items():
            flowblocks[k] = mocker.MagicMock(to_json=mocker.MagicMock(return_value=v))
        return flowblocks

    @pytest.fixture
    def mock_pad(self, mocker, mock_all_flowblocks):
        return mocker.MagicMock(db=mocker.MagicMock(flowblocks=mock_all_flowblocks))

    @pytest.fixture
    def mock_empty_pad(self, mocker):
        return mocker.MagicMock(db=mocker.MagicMock(flowblocks={}))

    @pytest.fixture
    def mock_flow(self, mocker):
        """TODO keep meaningful/useful flowblock names in the flow"""
        return mocker.MagicMock(flow_blocks=["this", "is", "not", "done"])

    @pytest.fixture
    def mock_empty_flow(self, mocker):
        return mocker.MagicMock(flow_blocks=None)

    def test_returns_all_flowblocks_if_no_names_provided(
        self, mock_empty_flow, mock_pad, expected_all_flowblocks
    ):
        """Test that if no flowblock names are provided, all flowblocks in the pad are returned."""
        returned_flowblocks = flow.discover_relevant_flowblock_models(
            mock_empty_flow, mock_pad, None, None
        )
        assert returned_flowblocks == expected_all_flowblocks

    def test_returns_empty_dict_if_no_flowblocks_in_pad(
        self, mock_flow, mock_empty_pad
    ):
        """Test that if there are no flowblocks in the pad, no flowblocks are returned."""
        returned_flowblocks = flow.discover_relevant_flowblock_models(
            mock_flow, mock_empty_pad, None, None
        )
        assert returned_flowblocks == {}
