from dataclasses import dataclass
from decimal import Decimal
from typing import Tuple


@dataclass
class DateDuration:
    years: Decimal = Decimal(0)
    months: Decimal = Decimal(0)
    days: Decimal = Decimal(0)
    weeks: Decimal = Decimal(0)


@dataclass
class TimeDuration:
    hours: Decimal = Decimal(0)
    minutes: Decimal = Decimal(0)
    seconds: Decimal = Decimal(0)


Duration = Tuple[DateDuration, TimeDuration]
