from decimal import Decimal

import pytest

from isoduration.parser.exceptions import InvalidFractional
from isoduration.parser.validation import validate_fractional
from isoduration.types import DateDuration, Duration, TimeDuration


@pytest.mark.parametrize(
    "date_duration, time_duration",
    (
        (DateDuration(), TimeDuration()),
        (DateDuration(years=Decimal("1.3")), TimeDuration()),
        (DateDuration(years=Decimal("1"), months=Decimal("2.5")), TimeDuration()),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6.9")),
            TimeDuration(),
        ),
        (DateDuration(weeks=Decimal("14.2")), TimeDuration()),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(hours=Decimal("6.18")),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(hours=Decimal("6"), minutes=Decimal("18.11")),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(minutes=Decimal("18"), seconds=Decimal("11.42")),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(hours=Decimal("6"), seconds=Decimal("11.42")),
        ),
        (
            DateDuration(days=Decimal("6")),
            TimeDuration(hours=Decimal("6"), seconds=Decimal("11.42")),
        ),
        (
            DateDuration(years=Decimal("1"), days=Decimal("6")),
            TimeDuration(minutes=Decimal("18.11")),
        ),
    ),
)
def test_correct_fractional_duration(date_duration, time_duration):
    validate_fractional(Duration(date_duration, time_duration))


@pytest.mark.parametrize(
    "date_duration, time_duration",
    (
        (
            DateDuration(years=Decimal("1.5"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2.4"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6.3")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6.2"), minutes=Decimal("18"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18.1"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(years=Decimal("1.5"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2.4"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6.3")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6.2"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1"), months=Decimal("2"), days=Decimal("6")),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18.1"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(
                years=Decimal("1"), months=Decimal("2.003"), days=Decimal("6")
            ),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18.3"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(
                years=Decimal("1"), months=Decimal("2.003"), days=Decimal("6.1")
            ),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11")
            ),
        ),
        (
            DateDuration(
                years=Decimal("1"), months=Decimal("2.003"), days=Decimal("6")
            ),
            TimeDuration(
                hours=Decimal("6"), minutes=Decimal("18"), seconds=Decimal("11.42")
            ),
        ),
        (
            DateDuration(years=Decimal("1.5")),
            TimeDuration(seconds=Decimal("11.42")),
        ),
        (
            DateDuration(years=Decimal("1.5")),
            TimeDuration(seconds=Decimal("11")),
        ),
        (
            DateDuration(years=Decimal("7"), days=Decimal("1.5")),
            TimeDuration(seconds=Decimal("11")),
        ),
        (
            DateDuration(),
            TimeDuration(hours=Decimal("3.5"), seconds=Decimal("11")),
        ),
    ),
)
def test_incorrect_fractional_duration(date_duration, time_duration):
    with pytest.raises(InvalidFractional):
        validate_fractional(Duration(date_duration, time_duration))
