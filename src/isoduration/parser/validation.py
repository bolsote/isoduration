from decimal import Decimal
from typing import Generator

from isoduration.parser.exceptions import InvalidFractional
from isoduration.parser.util import is_integer
from isoduration.types import Duration


def validate_fractional(duration: Duration) -> None:
    def reverse(duration: Duration) -> Generator[Decimal, None, None]:
        time_duration = duration.time
        time_order = ("seconds", "minutes", "hours")

        date_duration = duration.date
        date_order = ("weeks", "days", "months", "years")

        for element in time_order:
            yield getattr(time_duration, element)
        for element in date_order:
            yield getattr(date_duration, element)

    fractional_allowed = True

    for value in reverse(duration):
        if fractional_allowed:
            if not value.is_zero():
                # Fractional values are only allowed in the lowest order
                # non-zero component.
                fractional_allowed = False
        elif not is_integer(value):
            raise InvalidFractional("Only the lowest order component can be fractional")
