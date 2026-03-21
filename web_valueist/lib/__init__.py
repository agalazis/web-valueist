import requests
from bs4 import BeautifulSoup
from . import parser, operator
from .exception import ValueistException, ValueNotFound, ParserError
from .parser import Parser, ParserNotSupportedError
from .operator import Operator, OperatorNotSupportedError
import logging
from typing import TypedDict, Generic, TypeVar, Literal, overload

logger = logging.getLogger(__name__)

T = TypeVar("T")

type Quantifier = Literal["ANY", "EVERY"]

class EvaluateResult(TypedDict, Generic[T]):
    success: bool
    values: list[T]

def _fetch_values(url: str, selector: str):
    response = requests.get(url, timeout=10)
    if logger.isEnabledFor(logging.DEBUG):
        # We only access response.text if we are in debug mode
        # to avoid unnecessary decoding of the response content
        # for large payloads.
        logger.debug("Looking for %s in %s", selector, response.text)
    soup = BeautifulSoup(response.content, "html.parser")
    elements=soup.css.select(selector)
    if len(elements)<1:
        raise ValueNotFound
    values = [el.text for el in elements]
    return values


def _apply_operator(
    parsed_current_value: operator.ParsedValue,
    operator_name: Operator,
    parsed_reference_value: operator.ParsedValue,
):
    return operator.apply(operator_name, parsed_current_value, parsed_reference_value)


@overload
def evaluate(
    url: str, selector: str, parser_name: Literal["int"], operator_name: Operator, value: str, quantifier: Quantifier = "ANY", strict_parsing: bool = False
) -> EvaluateResult[int]: ...

@overload
def evaluate(
    url: str, selector: str, parser_name: Literal["float"], operator_name: Operator, value: str, quantifier: Quantifier = "ANY", strict_parsing: bool = False
) -> EvaluateResult[float]: ...

@overload
def evaluate(
    url: str, selector: str, parser_name: Literal["str"], operator_name: Operator, value: str, quantifier: Quantifier = "ANY", strict_parsing: bool = False
) -> EvaluateResult[str]: ...

@overload
def evaluate(
    url: str, selector: str, parser_name: Literal["bool"], operator_name: Operator, value: str, quantifier: Quantifier = "ANY", strict_parsing: bool = False
) -> EvaluateResult[bool]: ...

@overload
def evaluate(
    url: str, selector: str, parser_name: Parser, operator_name: Operator, value: str, quantifier: Quantifier = "ANY", strict_parsing: bool = False
) -> EvaluateResult[int | float | str | bool]: ...

def evaluate(
    url: str,
    selector: str,
    parser_name: Parser,
    operator_name: Operator,
    value: str,
    quantifier: Quantifier = "ANY",
    strict_parsing: bool = False,
) -> EvaluateResult[int | float | str | bool]:

    current_values = _fetch_values(url, selector)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Found value %s", current_values)

    parsed_reference_value = parser.parse(parser_name, value)

    parsed_current_values = []
    for val in current_values:
        try:
            parsed_current_values.append(parser.parse(parser_name, val))
        except ParserError:
            if strict_parsing:
                raise

    results = [
        _apply_operator(parsed_val, operator_name, parsed_reference_value)
        for parsed_val in parsed_current_values
    ]
    if quantifier == "ANY":
        success = any(results) if results else False
    elif quantifier == "EVERY":
        success = all(results) if results else False
    else:
        # Fallback to ANY if quantifier is unknown, or we could raise an error
        success = any(results) if results else False

    return {
        "success": success,
        "values": parsed_current_values,
    }


__all__ = [
    "evaluate",
    "EvaluateResult",
    "Parser",
    "Operator",
    "Quantifier",
    "ParserNotSupportedError",
    "OperatorNotSupportedError",
    "ValueistException",
    "ValueNotFound",
]
