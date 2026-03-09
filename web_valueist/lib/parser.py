from decimal import ROUND_HALF_UP, Decimal
import re
from typing import Literal

from .exception import ValueistException

type Parser = Literal["int", "str", "bool", "float"]

INT_EXPONENT=Decimal('0')

def _clean_float_string(val: str):
    """Cleans up float string and returns float string ready for Decimal/float conversion.
    It attempts to handle thousands separators (both . and ,) by assuming the last
    separator is the decimal point if multiple separators or different types are present.

    Args:
        val (str): a string that is expected to be parsed as float

    Returns:
        str: The normalized float string
    """
    # Keep only digits, dots and commas
    cleaned = re.sub(r"[^\d.,]", "", val)

    # Find all separators
    separators = re.findall(r"[.,]", cleaned)
    if not separators:
        return cleaned

    # If we have multiple separators or both types,
    # the last one is the decimal point, others are thousands separators.
    last_sep = separators[-1]
    other_sep = "," if last_sep == "." else "."

    # Remove all 'other' separators
    cleaned = cleaned.replace(other_sep, "")

    # Now we only have 'last_sep' type. If there are multiple, they are all thousands separators
    # UNLESS it's the last one.
    if cleaned.count(last_sep) > 1:
        # 1.234.567 -> 1234567 (wait, if there's no decimal it's just an int)
        # Actually, if there are multiple, we remove all of them.
        cleaned = cleaned.replace(last_sep, "")
    else:
        # Only one separator left, treat as decimal point
        cleaned = cleaned.replace(last_sep, ".")

    return cleaned


def _parse_bool(val: str):
    """Parses a string into a boolean.
    Supports true/false, yes/no, 1/0, t/f (case-insensitive).

    Args:
        val (str): a string that is expected to be parsed as boolean

    Returns:
        bool: The boolean for the provided string
    """
    normalized = val.strip().lower()
    truthy = {"true", "1", "t", "yes", "y"}
    falsy = {"false", "0", "f", "no", "n"}

    if normalized in truthy:
        return True
    if normalized in falsy:
        return False

    # Fallback/Error handling: if it's not recognized, we could return False or raise
    # Let's be consistent with previous behavior but safer.
    # Previous behavior was int(cleaned_string) which could raise.
    try:
        return bool(int(re.sub(r"\D", "", normalized)))
    except (ValueError, TypeError):
        return False


def _parse_int(val: str):
    """ Cleans up int string and returns int
    The cleanup regex does the following
    1) Cleans up string as float
    2) Rounds it using HALF_UP rather than banker rounding

    Args:
        val (str): a string that is expected to be parsed as integer

    Returns:
        int: The rounded integer for the provided string 
    """
    float_string=_clean_float_string(val)
    return int(Decimal(float_string).quantize(exp=INT_EXPONENT, rounding=ROUND_HALF_UP))

def _parse_float(val: str):
    return float(_clean_float_string(val))


_parsers = {
    "int": _parse_int, 
    "float": _parse_float, 
    "str": str, 
    "bool": _parse_bool
}


class ParserNotSupportedError(ValueistException):
    def __init__(self, *args: object) -> None:
        super().__init__(
            f"Parser not supported. Possible parsers are: {','.join(_parsers.keys())}"
        )


def _get_parser(parser_name: str):
    try:
        return _parsers[parser_name]
    except KeyError as exception:
        raise ParserNotSupportedError from exception


def parse(parser_name: Parser, value: str):
    return _get_parser(parser_name)(value)
