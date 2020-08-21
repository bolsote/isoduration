from isoduration.constants import PERIOD_PREFIX
from isoduration.formatter.checking import check_global_sign
from isoduration.formatter.formatting import format_date, format_time
from isoduration.types import Duration


def format_duration(duration: Duration) -> str:
    date_duration, time_duration = duration

    global_sign = check_global_sign(duration)
    date_duration_str = format_date(date_duration, global_sign)
    time_duration_str = format_time(time_duration, global_sign)

    duration_str = f"{date_duration_str}{time_duration_str}"
    sign_str = "-" if global_sign < 0 else ""

    if duration_str == PERIOD_PREFIX:
        return f"{PERIOD_PREFIX}0D"

    return f"{sign_str}{duration_str}"
