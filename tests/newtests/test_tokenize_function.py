from pathlib import Path
from lektor.metaformat import tokenize
from _operator import concat


CONTENTS_FILE = (
    Path(__file__).parent.parent / "demo-project" / "content" / "contents.lr"
)


class TestTokenizeFunction:

    """Tests to check metaformat.tokenize function"""

    def test_tokenize_condition1(self):
        """ Test tokenize function with sample .lr file with encoding utf-8 and no keys"""
        x = 0
        data1 = ("title", ["Welcome"])
        data2 = (
            "body",
            [
                "#### text####\n",
                "content: Welcome to this pretty nifty website.\n",
                "#### quote####\n",
                "text: Pretty cool\n",
                "---\n",
                "citation: A wise guy",
            ],
        )
        with open(CONTENTS_FILE, "rb") as f:
            for i in tokenize(f, encoding="utf-8"):
                temp = concat("data", str(x + 1))
                assert i == vars()[temp]
                x = x + 1

    def test_tokenize_condition2(self):
        """ Test tokenize function with sample .lr file with encoding utf-8 and 'title' as key"""
        x = 0
        data1 = ("title", ["Welcome"])
        data2 = ("body", None)
        with open(CONTENTS_FILE, "rb") as f:
            for i in tokenize(f, ["title"], encoding="utf-8"):
                temp = concat("data", str(x + 1))
                assert i == vars()[temp]
                x = x + 1

    def test_tokenize_condition3(self):
        """ Test tokenize function with sample .lr file with
		encoding utf-8  and random value for key"""
        x = 0
        data1 = ("title", None)
        data2 = ("body", None)
        with open(CONTENTS_FILE, "rb") as f:
            for i in tokenize(f, ["random"], encoding="utf-8"):
                temp = concat("data", str(x + 1))
                assert i == vars()[temp]
                x = x + 1
