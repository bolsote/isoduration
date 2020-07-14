from isoduration.exceptions import DurationFormattingException
from isoduration.types import DateDuration, Duration, TimeDuration


def check_global_sign(duration: Duration) -> int:
    # pylint: disable=too-many-return-statements

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
        return +1

    if date_duration != DateDuration():
        if is_date_negative:
            return -1
        return +1

    if time_duration != TimeDuration():
        if is_time_negative:
            return -1
        return +1

    return +1


def validate_date_duration(date_duration: DateDuration) -> bool:
    if date_duration.weeks:
        if date_duration.years or date_duration.months or date_duration.days:
            return False
        return True

    return True


def format_date(date_duration: DateDuration, global_sign: int) -> str:
    if not validate_date_duration(date_duration):
        raise DurationFormattingException(
            "Weeks are incompatible with other date designators"
        )

    date_duration_str = "P"

    if date_duration.weeks != 0:
        date_duration_str += f"{date_duration.weeks * global_sign}W"

    if date_duration.years != 0:
        date_duration_str += f"{date_duration.years * global_sign}Y"
    if date_duration.months != 0:
        date_duration_str += f"{date_duration.months * global_sign}M"
    if date_duration.days != 0:
        date_duration_str += f"{date_duration.days * global_sign}D"

    return date_duration_str


def format_time(time_duration: TimeDuration, global_sign: int) -> str:
    time_duration_str = "T"

    if time_duration.hours != 0:
        time_duration_str += f"{time_duration.hours * global_sign}H"
    if time_duration.minutes != 0:
        time_duration_str += f"{time_duration.minutes * global_sign}M"
    if time_duration.seconds != 0:
        time_duration_str += f"{time_duration.seconds * global_sign}S"

    if time_duration_str == "T":
        return ""
    return time_duration_str


def format_duration(duration: Duration) -> str:
    date_duration, time_duration = duration

    global_sign = check_global_sign(duration)
    date_duration_str = format_date(date_duration, global_sign)
    time_duration_str = format_time(time_duration, global_sign)

    duration_str = f"{date_duration_str}{time_duration_str}"
    sign_str = "-" if global_sign < 0 else ""

    if duration_str == "P":
        return "P0D"

    return f"{sign_str}{duration_str}"
