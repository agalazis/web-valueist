from typing import Literal

from .exception import ValueistException

type Parser = Literal["int", "str", "bool"]
_parsers = {"int": int, "str": str, "bool": bool}


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
