from lektor import db


class TestCompHelperCoerce:
    """Previously tested requirements of coerce:
        - If the arguments are of the same type, return the input
        - If the first argument is Undefined, change it to None in the output
        - If the second argument is Undefined, change it to None in the output
        - If both arguments are strings, normalize them both in the output
    Previously untested but now tested requirements:
        - Given a number and a number-convertible arg s, convert s to a number in the output
        - Given a number-convertible arg s and then a number, convert s to a number in the output
        - Given a non-number-convertible arg and then a number, return the input
        - Given a number and then a non-number-convertible arg, return the input
    Untested requirements:
        - None
    """

    def test_number_and_then_convertible(self):
        """If the first arg is a number, and the second can be converted to a number, the second is
        converted
        """
        number = 1
        assert db._CmpHelper.coerce(1, str(number)) == (number, number)

    def test_convertible_and_then_number(self):
        """If the second arg is a number, and the first is not a number but can be converted to a
        number, the first is converted
        """
        number = 1
        assert db._CmpHelper.coerce(str(number), 1) == (number, number)

    def test_first_number_but_not_second(self):
        """If the first arg is a number, but the second can't be converted to a number, return the
        input
        """
        a, b = 1, []
        assert db._CmpHelper.coerce(1, []) == (a, b)

    def test_second_number_but_not_first(self):
        """If the second arg is a number, but the first can't be converted to a number, return the
        input
        """
        a, b = [], 1
        assert db._CmpHelper.coerce([], 1) == (a, b)
