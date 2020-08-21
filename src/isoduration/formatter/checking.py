from isoduration.formatter.exceptions import DurationFormattingException
from isoduration.types import DateDuration, Duration, TimeDuration


def check_global_sign(duration: Duration) -> int:
    date_duration, time_duration = duration

    is_date_negative = (
        date_duration.years <= 0
        and date_duration.months <= 0
        and date_duration.days <= 0
        and date_duration.weeks <= 0
    )
    is_time_negative = (
        time_duration.hours <= 0
        and time_duration.minutes <= 0
        and time_duration.seconds <= 0
    )

    if date_duration != DateDuration() and time_duration != TimeDuration():
        if is_date_negative and is_time_negative:
            return -1
    elif date_duration != DateDuration():
        if is_date_negative:
            return -1
    elif time_duration != TimeDuration():
        if is_time_negative:
            return -1

    return +1


def validate_date_duration(date_duration: DateDuration) -> None:
    if date_duration.weeks:
        if date_duration.years or date_duration.months or date_duration.days:
            raise DurationFormattingException(
                "Weeks are incompatible with other date designators"
            )
