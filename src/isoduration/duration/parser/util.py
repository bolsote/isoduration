import decimal
from typing import Dict

from isoduration.constants import PERIOD_PREFIX, TIME_PREFIX, WEEK_PREFIX
from isoduration.duration.parser.exceptions import OutOfDesignators


def is_period(ch: str) -> bool:
    return ch == PERIOD_PREFIX


def is_time(ch: str) -> bool:
    return ch == TIME_PREFIX


def is_week(ch: str) -> bool:
    return ch == WEEK_PREFIX


def is_number(ch: str) -> bool:
    return ch in "+-0123456789.,eE"


def is_letter(ch: str) -> bool:
    return ch.isalpha() and ch.lower() != "e"


def is_integer(number: decimal.Decimal) -> bool:
    return number == number.to_integral_value()


def parse_designator(designators: Dict[str, str], target: str) -> str:
    while True:
        try:
            key, value = designators.popitem(last=False)  # type: ignore
        except KeyError as exc:
            raise OutOfDesignators from exc

        if key == target:
            return value
