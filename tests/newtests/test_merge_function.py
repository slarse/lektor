from lektor.utils import merge


class TestMergeFunction:

    """Test for util.merge function"""

    def test_merge_condition1(self):
        """Test to check merge function, if parameters a,b are list objects and b is None"""
        assert merge([1, 2, 3, 4], [None]) == [1, 2, 3, 4]

    def test_merge_condition2(self):
        """Test to check merge function, if parameters a,b are list objects and a is None"""
        assert merge([None], [5, 6, 7, 8]) == [5]

    def test_merge_condition3(self):
        """Test to check merge function, if parameters a,b are list objects"""
        assert merge([1, 2, 3, 4], [5, 6, 7, 8]) == [1, 2, 3, 4]

    def test_merge_condition4(self):
        """Test to check merge function, if parameters a,b are dictionary object and b is None"""
        assert merge({"a": "b"}, {}) == {"a": "b"}

    def test_merge_condition5(self):
        """Test to check merge function, if parameters a,b are dictionary object and a is None"""
        assert merge({}, {"x": "y", "q": "w", "e": "r"}) == {
            "x": "y",
            "q": "w",
            "e": "r",
        }

    def test_merge_condition6(self):
        """Test to check merge function, if parameters a,b are dictionary object"""
        assert merge({"a": "b"}, {"x": "y", "q": "w", "e": "r"}) == {
            "a": "b",
            "x": "y",
            "q": "w",
            "e": "r",
        }
