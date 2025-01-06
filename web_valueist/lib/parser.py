from decimal import ROUND_HALF_UP, Decimal
import re
from typing import Literal

from .exception import ValueistException

type Parser = Literal["int", "str", "bool"]

INT_EXPONENT=Decimal('0')

def _clean_float_string(val:str):
    """Cleans up float string and returns float
    The cleanup regex does the following
    1) Keeps only digits, commas and dots
    2) Removes commas or dots that do not match coma or dot and the final 1 or 2 digits


    Args:
        val (str): a string that is expected to be parsed as float

    Returns:
        str: The float for the provided string 
    """    
    return re.sub(r"[^\d|\.|\,]|(?![.,]\d{1,2}$)[.,]", "", val).replace(',', '.')

def _clean_bool_tiny_int_string(val: str):
    """Cleans up bool/tiny int values and returns tiny int string

    Args:
        val str: a string that is expected to be parsed as bool/ tiny int

    Returns:
        str: The tiny int for the provided string 
    """
    return re.sub('(?i)(?!true|false|1|0|t|f).', '',val).upper().replace('F','0').replace('T', '1')

def _parse_int(val:str):
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

def _parse_float(val:str):
    return float(_clean_float_string(val))

def _parse_bool(val:str):
    """Cleans up bool/tiny int string and returns bool

    Args:
        val (str): a string that is expected to be parsed as boolean

    Returns:
        bool: The boolean for the provided string
    """    
    tiny_int_string = _clean_bool_tiny_int_string(val)
    return bool(int(tiny_int_string))

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
