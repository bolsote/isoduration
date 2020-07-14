class DurationParsingException(ValueError):
    ...


class DurationFormattingException(ValueError):
    ...


class OutOfDesignators(KeyError):
    ...


class EmptyDuration(DurationParsingException):
    ...


class IncorrectDesignator(DurationParsingException):
    ...


class NoTime(DurationParsingException):
    ...


class UnknownToken(DurationParsingException):
    ...


class UnparseableValue(DurationParsingException):
    ...
