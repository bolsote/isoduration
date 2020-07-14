import pytest
from hypothesis import given
from hypothesis.strategies import builds, decimals, text, SearchStrategy

from isoduration import exceptions, format_duration, parse_duration
from isoduration.types import DateDuration, TimeDuration


item_st = decimals(
    min_value=-1_000_000_000,
    max_value=+1_000_000_000,
    places=8,
    allow_nan=False,
    allow_infinity=False,
)

date_duration_st: SearchStrategy[DateDuration] = builds(
    DateDuration, years=item_st, months=item_st, days=item_st
)
time_duration_st: SearchStrategy[TimeDuration] = builds(
    TimeDuration, hours=item_st, minutes=item_st, seconds=item_st
)


@given(date_duration=date_duration_st, time_duration=time_duration_st)
def test_parse_inverse_of_format(date_duration, time_duration):
    duration = (date_duration, time_duration)
    assert parse_duration(format_duration(duration)) == duration


@given(text())
def test_parser_not_misbehaving(duration):
    with pytest.raises(exceptions.DurationParsingException):
        parse_duration(duration)
