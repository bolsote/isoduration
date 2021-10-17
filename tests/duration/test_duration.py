from datetime import datetime
from decimal import Decimal

import pytest

from isoduration.duration.parser import parse_duration
from isoduration.duration.types import DateDuration, Duration, TimeDuration


def test_representations():
    duration = Duration(DateDuration(weeks=3), TimeDuration(hours=2, seconds=59))

    date_repr = (
        "DateDuration(years=Decimal('0'), months=Decimal('0'), "
        "days=Decimal('0'), weeks=3)"
    )
    time_repr = "TimeDuration(hours=2, minutes=Decimal('0'), seconds=59)"
    duration_repr = f"Duration({date_repr}, {time_repr})"

    duration_str = "P3WT2H59S"

    assert repr(duration) == duration_repr
    assert str(duration) == duration_str


def test_is_hashable():
    durations = {
        Duration(DateDuration(weeks=7), TimeDuration()),
        Duration(DateDuration(weeks=11), TimeDuration()),
        Duration(DateDuration(weeks=7), TimeDuration()),
    }

    assert len(durations) == 2


def test_iteration():
    duration = Duration(DateDuration(weeks=3), TimeDuration(hours=2, seconds=59))

    assert list(duration) == [
        ("years", Decimal("0")),
        ("months", Decimal("0")),
        ("days", Decimal("0")),
        ("weeks", Decimal("3")),
        ("hours", Decimal("2")),
        ("minutes", Decimal("0")),
        ("seconds", Decimal("59")),
    ]


def test_reverse_iteration():
    duration = Duration(DateDuration(weeks=3), TimeDuration(hours=2, seconds=59))

    assert list(reversed(duration)) == [
        ("seconds", Decimal("59")),
        ("minutes", Decimal("0")),
        ("hours", Decimal("2")),
        ("weeks", Decimal("3")),
        ("days", Decimal("0")),
        ("months", Decimal("0")),
        ("years", Decimal("0")),
    ]


@pytest.mark.parametrize(
    "duration1, duration2",
    (
        (
            Duration(DateDuration(days=1), TimeDuration()),
            Duration(DateDuration(), TimeDuration(hours=24)),
        ),
        (
            Duration(DateDuration(weeks=3), TimeDuration()),
            Duration(DateDuration(days=21), TimeDuration()),
        ),
        (
            Duration(DateDuration(days=3), TimeDuration(hours=25)),
            Duration(DateDuration(days=4), TimeDuration(hours=1)),
        ),
    ),
)
def test_distinguishes_representations(duration1, duration2):
    base = datetime(2000, 6, 1)

    assert base + duration1 == base + duration2
    assert duration1 != duration2


@pytest.mark.parametrize(
    "original, negated",
    (
        (DateDuration(), DateDuration()),
        (DateDuration(years=7), DateDuration(years=-7)),
        (DateDuration(months=3), DateDuration(months=-3)),
        (DateDuration(days=11), DateDuration(days=-11)),
        (DateDuration(weeks=42), DateDuration(weeks=-42)),
        (DateDuration(weeks=-42), DateDuration(weeks=42)),
        (DateDuration(years=3, months=2), DateDuration(years=-3, months=-2)),
        (DateDuration(years=-3, months=2), DateDuration(years=3, months=-2)),
        (DateDuration(years=3, months=-2), DateDuration(years=-3, months=2)),
        (
            DateDuration(years=1, months=2, days=3),
            DateDuration(years=-1, months=-2, days=-3),
        ),
        (
            DateDuration(years=1, months=-2, days=3),
            DateDuration(years=-1, months=2, days=-3),
        ),
        (DateDuration(years=7, weeks=11), DateDuration(years=-7, weeks=-11)),
        (DateDuration(years=-7, weeks=-11), DateDuration(years=7, weeks=11)),
    ),
)
def test_negate_date_duration(original, negated):
    assert -original == negated


@pytest.mark.parametrize(
    "original, negated",
    (
        (TimeDuration(), TimeDuration()),
        (TimeDuration(hours=11), TimeDuration(hours=-11)),
        (TimeDuration(hours=-11), TimeDuration(hours=11)),
        (TimeDuration(minutes=3), TimeDuration(minutes=-3)),
        (TimeDuration(minutes=-3), TimeDuration(minutes=3)),
        (TimeDuration(seconds=9), TimeDuration(seconds=-9)),
        (TimeDuration(seconds=-9), TimeDuration(seconds=9)),
        (TimeDuration(hours=11, minutes=2), TimeDuration(hours=-11, minutes=-2)),
        (TimeDuration(hours=-11, minutes=2), TimeDuration(hours=11, minutes=-2)),
        (
            TimeDuration(hours=3, minutes=2, seconds=1),
            TimeDuration(hours=-3, minutes=-2, seconds=-1),
        ),
        (
            TimeDuration(hours=-3, minutes=2, seconds=-1),
            TimeDuration(hours=3, minutes=-2, seconds=1),
        ),
    ),
)
def test_negate_time_duration(original, negated):
    assert -original == negated


@pytest.mark.parametrize(
    "original, negated",
    (
        (
            Duration(DateDuration(), TimeDuration()),
            Duration(DateDuration(), TimeDuration()),
        ),
        (
            Duration(DateDuration(years=11, days=3), TimeDuration(hours=8)),
            Duration(DateDuration(years=-11, days=-3), TimeDuration(hours=-8)),
        ),
        (
            Duration(DateDuration(years=8, weeks=-2), TimeDuration()),
            Duration(DateDuration(years=-8, weeks=2), TimeDuration()),
        ),
        (
            Duration(DateDuration(), TimeDuration(hours=9, seconds=11)),
            Duration(DateDuration(), TimeDuration(hours=-9, seconds=-11)),
        ),
        (
            Duration(
                DateDuration(years=6, months=11, days=3),
                TimeDuration(hours=11, minutes=2),
            ),
            Duration(
                DateDuration(years=-6, months=-11, days=-3),
                TimeDuration(hours=-11, minutes=-2),
            ),
        ),
        (
            Duration(
                DateDuration(years=6, months=-11, days=-3),
                TimeDuration(hours=11, minutes=-2),
            ),
            Duration(
                DateDuration(years=-6, months=11, days=3),
                TimeDuration(hours=-11, minutes=2),
            ),
        ),
    ),
)
def test_negate_duration(original, negated):
    assert -original == negated


@pytest.mark.parametrize(
    "start, duration, end",
    (
        (datetime(2000, 1, 12), "PT33H", datetime(2000, 1, 13, 9)),
        (datetime(2000, 1, 12), "P4W", datetime(2000, 2, 9)),
        (datetime(2000, 2, 1), "P1Y1M", datetime(2001, 3, 1)),
        (datetime(2000, 2, 1), "-P1Y1M", datetime(1999, 1, 1)),
        (datetime(2000, 2, 1), "P1Y1M1D", datetime(2001, 3, 2)),
        (datetime(2000, 2, 1), "-P1Y1M1D", datetime(1998, 12, 31)),
        (datetime(2000, 2, 29), "P1Y", datetime(2001, 2, 28)),
        (datetime(1996, 2, 29), "P4Y", datetime(2000, 2, 29)),
        (datetime(2096, 2, 29), "P4Y", datetime(2100, 2, 28)),
        (datetime(2000, 2, 29), "P370D", datetime(2001, 3, 5)),
        (datetime(2000, 2, 29), "P1Y1D", datetime(2001, 3, 1)),
        (datetime(1996, 2, 29), "P4Y1D", datetime(2000, 3, 1)),
        (datetime(2096, 2, 29), "P4Y1D", datetime(2100, 3, 1)),
        (datetime(2000, 2, 29), "P1Y1M", datetime(2001, 3, 29)),
        (datetime(2000, 2, 29), "-P1Y1M", datetime(1999, 1, 29)),
        (datetime(2000, 2, 29), "P1Y1M1D", datetime(2001, 3, 30)),
        (datetime(2000, 2, 29), "-P1Y1M1D", datetime(1999, 1, 28)),
        (datetime(2000, 1, 1), "-P3M", datetime(1999, 10, 1)),
        (datetime(2000, 4, 1), "-P1Y1M1D", datetime(1999, 2, 28)),
        (datetime(2001, 4, 1), "-P1Y1M1D", datetime(2000, 2, 29)),
        (datetime(1987, 2, 11), "P33Y6M11D", datetime(2020, 8, 22)),
        (datetime(2011, 10, 8, 23), "PT1H", datetime(2011, 10, 9)),
        (datetime(2011, 10, 8, 23), "PT90M", datetime(2011, 10, 9, 0, 30)),
        (datetime(2011, 10, 8, 23), "PT26H", datetime(2011, 10, 10, 1)),
        (
            datetime(2000, 1, 12),
            "P1Y3M5DT3.301S",
            datetime(2001, 4, 17, 0, 0, 3, 301000),
        ),
        (
            datetime(2000, 1, 12, 0, 0, 0, 700000),
            "P1Y3M5DT3.301S",
            datetime(2001, 4, 17, 0, 0, 4, 1000),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14),
            "P1Y3M5DT7H10M3.3S",
            datetime(2001, 4, 17, 19, 23, 17, 300000),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 700000),
            "P1Y3M5DT7H10M3.3S",
            datetime(2001, 4, 17, 19, 23, 18),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 699999),
            "P1Y3M5DT7H10M3.3S",
            datetime(2001, 4, 17, 19, 23, 17, 999999),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 700001),
            "P1Y3M5DT7H10M3.3S",
            datetime(2001, 4, 17, 19, 23, 18, 1),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 629000),
            "P1Y3M5DT7H10M3.371S",
            datetime(2001, 4, 17, 19, 23, 18),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14),
            "P1Y3M5DT7H10M3.371001S",
            datetime(2001, 4, 17, 19, 23, 17, 371001),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 803142),
            "P1Y3M5DT7H10M3.992103S",
            datetime(2001, 4, 17, 19, 23, 18, 795245),
        ),
        (
            datetime(2000, 1, 12),
            "-P1Y3M5DT3.301S",
            datetime(1998, 10, 6, 23, 59, 56, 699000),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 700000),
            "P1Y3M5DT-7H10M-3.3S",
            datetime(2001, 4, 17, 5, 23, 11, 400000),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 699999),
            "P1Y3M5DT7H10M-3.7S",
            datetime(2001, 4, 17, 19, 23, 10, 999999),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 700001),
            "P-1Y3M5DT7H10M-3.7S",
            datetime(1999, 4, 17, 19, 23, 11, 1),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14, 629000),
            "P1Y3M5DT7H10M-3.629S",
            datetime(2001, 4, 17, 19, 23, 11),
        ),
        (
            datetime(2000, 1, 12, 12, 13, 14),
            "P1Y3M5DT7H10M-3.371001S",
            datetime(2001, 4, 17, 19, 23, 10, 628999),
        ),
        (
            datetime(2000, 3, 12, 12, 13, 14, 803142),
            "-P1Y2M5DT7H10M3.992103S",
            datetime(1999, 1, 7, 5, 3, 10, 811039),
        ),
        (datetime(2014, 10, 6, 1, 30, 3), "P2WT-3H-3S", datetime(2014, 10, 19, 22, 30)),
    ),
)
def test_add_datetime_duration(start, duration, end):
    assert start + parse_duration(duration) == end
    assert parse_duration(duration) + start == end


@pytest.mark.parametrize(
    "start, duration, end",
    (
        (datetime(2000, 1, 1), "P3M", datetime(1999, 10, 1)),
        (datetime(2000, 1, 1), "P6W", datetime(1999, 11, 20)),
        (datetime(2000, 2, 1), "P1Y1M", datetime(1999, 1, 1)),
        (datetime(2000, 2, 1), "P1Y1M1D", datetime(1998, 12, 31)),
        (datetime(2000, 2, 29), "P1Y1M", datetime(1999, 1, 29)),
        (datetime(2000, 2, 29), "P1Y1M1D", datetime(1999, 1, 28)),
        (datetime(2001, 4, 1), "P1Y1M1D", datetime(2000, 2, 29)),
        (datetime(2000, 4, 1), "P1Y1M1D", datetime(1999, 2, 28)),
        (datetime(2011, 10, 9), "PT1H", datetime(2011, 10, 8, 23)),
        (datetime(2014, 10, 20, 1, 30), "P2WT2H", datetime(2014, 10, 5, 23, 30)),
        (
            datetime(2014, 10, 20, 1, 30, 2, 200000),
            "P2WT2H2.2S",
            datetime(2014, 10, 5, 23, 30),
        ),
        (
            datetime(2014, 10, 20, 1, 30, 2, 800000),
            "P2WT2H2.2S",
            datetime(2014, 10, 5, 23, 30, 0, 600000),
        ),
        (
            datetime(2014, 10, 20, 1, 30, 2),
            "P2WT2H2.2S",
            datetime(2014, 10, 5, 23, 29, 59, 800000),
        ),
        (
            datetime(2014, 10, 20, 1, 30, 2, 104000),
            "P2WT2H2.204S",
            datetime(2014, 10, 5, 23, 29, 59, 900000),
        ),
    ),
)
def test_sub_datetime_duration(start, duration, end):
    assert start - parse_duration(duration) == end


def test_non_commutativity():
    """
    https://www.w3.org/TR/xmlschema-2/#adding-durations-to-instants-commutativity-associativity
    """

    start = datetime(2000, 3, 30)

    duration1 = parse_duration("P1D")
    duration2 = parse_duration("P1M")

    assert start + duration1 + duration2 == datetime(2000, 4, 30)
    assert start + duration2 + duration1 == datetime(2000, 5, 1)
