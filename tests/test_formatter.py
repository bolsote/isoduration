import pytest

from isoduration import format_duration, DurationFormattingException
from isoduration.types import DateDuration, TimeDuration


@pytest.mark.parametrize(
    "duration, duration_str",
    (
        # Zero.
        ((DateDuration(), TimeDuration()), "P0D"),
        # All fields.
        (
            (
                DateDuration(years=3, months=6, days=4),
                TimeDuration(hours=12, minutes=30, seconds=5),
            ),
            "P3Y6M4DT12H30M5S",
        ),
        (
            (
                DateDuration(years=18, months=9, days=4),
                TimeDuration(hours=11, minutes=9, seconds=8),
            ),
            "P18Y9M4DT11H9M8S",
        ),
        # All fields, only date.
        ((DateDuration(years=4, months=5, days=18), TimeDuration()), "P4Y5M18D"),
        # All fields, only time.
        ((DateDuration(), TimeDuration(hours=2, minutes=3, seconds=4)), "PT2H3M4S"),
        # Some fields, date only.
        ((DateDuration(years=4), TimeDuration()), "P4Y"),
        ((DateDuration(weeks=2), TimeDuration()), "P2W"),
        ((DateDuration(months=1), TimeDuration()), "P1M"),
        ((DateDuration(days=6), TimeDuration()), "P6D"),
        # Some fields, time only.
        ((DateDuration(), TimeDuration(hours=2)), "PT2H"),
        ((DateDuration(), TimeDuration(hours=36)), "PT36H"),
        ((DateDuration(), TimeDuration(minutes=1)), "PT1M"),
        ((DateDuration(), TimeDuration(seconds=22)), "PT22S"),
        ((DateDuration(), TimeDuration(minutes=3, seconds=4)), "PT3M4S"),
        ((DateDuration(), TimeDuration(hours=6, seconds=59)), "PT6H59S"),
        # Some fields, date and time.
        (
            (DateDuration(days=1), TimeDuration(hours=2, minutes=3, seconds=4)),
            "P1DT2H3M4S",
        ),
        ((DateDuration(weeks=3), TimeDuration(hours=2, seconds=59)), "P3WT2H59S"),
        ((DateDuration(days=1), TimeDuration(hours=2)), "P1DT2H"),
        ((DateDuration(days=1), TimeDuration(hours=12)), "P1DT12H"),
        ((DateDuration(days=23), TimeDuration(hours=23)), "P23DT23H"),
        ((DateDuration(days=1), TimeDuration(hours=2, minutes=3)), "P1DT2H3M"),
        # Floating point.
        ((DateDuration(years=0.5), TimeDuration()), "P0.5Y"),
        ((DateDuration(), TimeDuration(hours=8.5, seconds=3)), "PT8.5H3S"),
        ((DateDuration(), TimeDuration(hours=2.3)), "PT2.3H"),
        ((DateDuration(), TimeDuration(seconds=22.22)), "PT22.22S"),
        # Signs.
        ((DateDuration(years=-2), TimeDuration()), "-P2Y"),
        ((DateDuration(weeks=-2), TimeDuration()), "-P2W"),
        ((DateDuration(weeks=-2.2), TimeDuration()), "-P2.2W"),
        (
            (
                DateDuration(years=-3, months=-6, days=-4),
                TimeDuration(hours=-12, minutes=-30, seconds=-5),
            ),
            "-P3Y6M4DT12H30M5S",
        ),
        (
            (
                DateDuration(years=-3, months=-6, days=-4),
                TimeDuration(hours=12, minutes=30, seconds=5),
            ),
            "P-3Y-6M-4DT12H30M5S",
        ),
        (
            (
                DateDuration(years=-3, months=-6, days=-4),
                TimeDuration(hours=-12, minutes=30, seconds=-5),
            ),
            "P-3Y-6M-4DT-12H30M-5S",
        ),
        (
            (DateDuration(days=-1), TimeDuration(hours=-2, minutes=-3, seconds=-4)),
            "-P1DT2H3M4S",
        ),
        ((DateDuration(years=-3, months=-6, days=-4), TimeDuration(),), "-P3Y6M4D",),
        ((DateDuration(), TimeDuration(hours=-6, minutes=-3)), "-PT6H3M"),
        ((DateDuration(), TimeDuration(hours=-6, minutes=3)), "PT-6H3M"),
        ((DateDuration(), TimeDuration(hours=6, minutes=-3)), "PT6H-3M"),
    ),
)
def test_format_duration(duration, duration_str):
    assert format_duration(duration) == duration_str


@pytest.mark.parametrize(
    "duration, exception, error_msg",
    (
        (
            (DateDuration(years=3, months=6, days=4, weeks=12), TimeDuration(),),
            DurationFormattingException,
            r"Weeks are incompatible with other date designators",
        ),
    ),
)
def test_format_duration_errors(duration, exception, error_msg):
    with pytest.raises(DurationFormattingException) as exc:
        format_duration(duration)

    assert exc.match(error_msg)
