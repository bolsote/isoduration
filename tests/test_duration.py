from datetime import datetime

import pytest

from isoduration import parse_duration


@pytest.mark.parametrize(
    "start, duration, end",
    (
        (
            datetime(2000, 1, 12, 12, 13, 14),
            "P1Y3M5DT7H10M3.3S",
            datetime(2001, 4, 17, 19, 23, 17),
        ),
        (datetime(2000, 1, 1), "-P3M", datetime(1999, 10, 1)),
        (datetime(2000, 1, 12), "PT33H", datetime(2000, 1, 13, 9)),
        (datetime(2000, 2, 1), "P1Y1M", datetime(2001, 3, 1)),
        (datetime(2000, 2, 29), "P1Y1M", datetime(2001, 3, 29)),
        (datetime(2000, 2, 29), "P1Y", datetime(2001, 2, 28)),
        (datetime(1996, 2, 29), "P4Y", datetime(2000, 2, 29)),
        (datetime(2096, 2, 29), "P4Y", datetime(2100, 2, 28)),
        (datetime(2000, 2, 1), "-P1Y1M", datetime(1999, 1, 1)),
        (datetime(2000, 2, 29), "-P1Y1M", datetime(1999, 1, 29)),
        (datetime(2000, 2, 1), "P1Y1M1D", datetime(2001, 3, 2)),
        (datetime(2000, 2, 29), "P1Y1M1D", datetime(2001, 3, 30)),
        (datetime(2000, 2, 29), "P1Y1D", datetime(2001, 3, 1)),
        (datetime(1996, 2, 29), "P4Y1D", datetime(2000, 3, 1)),
        (datetime(2096, 2, 29), "P4Y1D", datetime(2100, 3, 1)),
        (datetime(2000, 2, 1), "-P1Y1M1D", datetime(1998, 12, 31)),
        (datetime(2000, 2, 29), "-P1Y1M1D", datetime(1999, 1, 28)),
        (datetime(2001, 4, 1), "-P1Y1M1D", datetime(2000, 2, 29)),
        (datetime(2000, 4, 1), "-P1Y1M1D", datetime(1999, 2, 28)),
    ),
)
def test_add_datetime_duration(start, duration, end):
    assert start + parse_duration(duration) == end
    assert parse_duration(duration) + start == end


@pytest.mark.parametrize(
    "start, duration, end",
    (
        (datetime(2000, 1, 1), "P3M", datetime(1999, 10, 1)),
        (datetime(2000, 2, 1), "P1Y1M", datetime(1999, 1, 1)),
        (datetime(2000, 2, 29), "P1Y1M", datetime(1999, 1, 29)),
        (datetime(2000, 2, 1), "P1Y1M1D", datetime(1998, 12, 31)),
        (datetime(2000, 2, 29), "P1Y1M1D", datetime(1999, 1, 28)),
        (datetime(2001, 4, 1), "P1Y1M1D", datetime(2000, 2, 29)),
        (datetime(2000, 4, 1), "P1Y1M1D", datetime(1999, 2, 28)),
    ),
)
def test_sub_datetime_duration(start, duration, end):
    assert start - parse_duration(duration) == end
