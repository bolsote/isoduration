import decimal

import pytest

from isoduration.parser.util import is_integer


@pytest.mark.parametrize(
    "number, expected",
    (
        (decimal.Decimal(0), True),
        (decimal.Decimal(0.0), True),
        (decimal.Decimal(0.00001), False),
        (decimal.Decimal(0.0000000000000001), False),
        (decimal.Decimal(100), True),
        (decimal.Decimal(100.27), False),
        (decimal.Decimal(100.99999999999999), False),
        (decimal.Decimal(-384), True),
        (decimal.Decimal(-384.47231), False),
        (decimal.Decimal(384), True),
        (decimal.Decimal(384.27236), False),
    ),
)
def test_is_integer(number, expected):
    assert is_integer(number) == expected
