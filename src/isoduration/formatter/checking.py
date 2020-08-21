from isoduration.formatter.exceptions import DurationFormattingException
from isoduration.types import DateDuration, Duration, TimeDuration


def check_global_sign(duration: Duration) -> int:
    is_date_negative = (
        duration.date.years <= 0
        and duration.date.months <= 0
        and duration.date.days <= 0
        and duration.date.weeks <= 0
    )
    is_time_negative = (
        duration.time.hours <= 0
        and duration.time.minutes <= 0
        and duration.time.seconds <= 0
    )

    if duration.date != DateDuration() and duration.time != TimeDuration():
        if is_date_negative and is_time_negative:
            return -1
    elif duration.date != DateDuration():
        if is_date_negative:
            return -1
    elif duration.time != TimeDuration():
        if is_time_negative:
            return -1

    return +1


def validate_date_duration(date_duration: DateDuration) -> None:
    if date_duration.weeks:
        if date_duration.years or date_duration.months or date_duration.days:
            raise DurationFormattingException(
                "Weeks are incompatible with other date designators"
            )
