import requests
from bs4 import BeautifulSoup
from . import parser, operator
from .exception import ValueistException
from .parser import Parser, ParserNotSupportedError
from .operator import Operator, OperatorNotSupportedError
import logging

logger = logging.getLogger(__name__)


def _fetch_value(url: str, selector: str):
    response = requests.get(url, timeout=10)
    logger.debug("Looking for %s in %s", selector, response.text)
    soup = BeautifulSoup(response.content, "lxml")
    value = soup.css.select(selector)[0].text
    logger.debug("Found value %s", value)
    return value


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
    url: str, selector: str, parser_name: Parser, operator_name: Operator, value: str
):

    current_value = _fetch_value(url, selector)
    return _apply_operator(parser_name, current_value, operator_name, value)


__all__ = [
    "evaluate",
    "Parser",
    "Operator",
    "ParserNotSupportedError",
    "OperatorNotSupportedError",
    "ValueistException",
]
