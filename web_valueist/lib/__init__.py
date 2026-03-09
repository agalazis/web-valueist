import requests
from bs4 import BeautifulSoup
from . import parser, operator
from .exception import ValueistException, ValueNotFound
from .parser import Parser, ParserNotSupportedError
from .operator import Operator, OperatorNotSupportedError
import logging

logger = logging.getLogger(__name__)

def _fetch_values(url: str, selector: str):
    response = requests.get(url, timeout=10)
    if logger.isEnabledFor(logging.DEBUG):
        # We only access response.text if we are in debug mode
        # to avoid unnecessary decoding of the response content
        # for large payloads.
        logger.debug("Looking for %s in %s", selector, response.text)
    soup = BeautifulSoup(response.content, "lxml")
    elements=soup.css.select(selector)
    if len(elements)<1:
        raise ValueNotFound
    values = [el.text for el in elements]
    return values


def _apply_operator(
    parser_name: Parser,
    current_value: str,
    operator_name: Operator,
    reference_value: str,
):
    parsed_current_value = parser.parse(parser_name, current_value)
    parsed_reference_value = parser.parse(parser_name, reference_value)
    return operator.apply(operator_name, parsed_current_value, parsed_reference_value)


def evaluate(
    url: str,
    selector: str,
    parser_name: Parser,
    operator_name: Operator,
    value: str,
    quantifier: str = "ANY",
):

    current_values = _fetch_values(url, selector)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug("Found value %s", current_values)
    results = [
        _apply_operator(parser_name, val, operator_name, value)
        for val in current_values
    ]
    if quantifier == "ANY":
        success = any(results)
    elif quantifier == "EVERY":
        success = all(results)
    else:
        # Fallback to ANY if quantifier is unknown, or we could raise an error
        success = any(results)

    return {
        "success": success,
        "value": current_values if len(current_values) > 1 else current_values[0],
    }


__all__ = [
    "evaluate",
    "Parser",
    "Operator",
    "ParserNotSupportedError",
    "OperatorNotSupportedError",
    "ValueistException",
    "ValueNotFound",
]
