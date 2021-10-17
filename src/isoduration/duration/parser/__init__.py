from isoduration.duration.parser.exceptions import EmptyDuration
from isoduration.duration.parser.parsing import parse_date_duration
from isoduration.duration.parser.util import is_period
from isoduration.duration.parser.validation import validate_fractional
from isoduration.duration.types import Duration


def parse_duration(duration_str: str) -> Duration:
    if len(duration_str) < 2:
        raise EmptyDuration("No duration information provided")

    beginning = 1
    first = duration_str[beginning - 1]

    sign = +1

    if first == "+":
        beginning += 1
    if first == "-":
        sign = -1
        beginning += 1

    prefix = duration_str[beginning - 1]
    duration = duration_str[beginning:]

    if not is_period(prefix):
        raise EmptyDuration("No prefix provided")

    parsed_duration = parse_date_duration(duration, sign)

    validate_fractional(parsed_duration)

    return parsed_duration
