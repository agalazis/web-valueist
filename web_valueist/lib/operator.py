from typing import Any, Literal, TypedDict
import operator

from .exception import ValueistException

type Operator = Literal["gt", ">", "lt", "<", "ge", ">=", "le", "<=", "eq", "="]

_operators = {
    "gt": operator.gt,
    ">": operator.gt,
    "lt": operator.lt,
    "<": operator.lt,
    "ge": operator.ge,
    ">=": operator.ge,
    "le": operator.le,
    "<=": operator.le,
    "eq": operator.eq,
    "=": operator.eq,
    "ne": operator.ne,
    "!=": operator.ne,
}


class OperatorNotSupportedError(ValueistException):
    def __init__(self, *args: object) -> None:
        super().__init__(
            f"Operator not supported. Possible operators are: {','.join(_operators.keys())}"
        )


def _get_operator(parser_name: str):
    try:
        return _operators[parser_name]
    except KeyError as exception:
        raise OperatorNotSupportedError from exception


def apply(operator_name: Operator, a: str | int | bool, b: str | int | bool) -> bool:
    return _get_operator(operator_name)(a, b)
