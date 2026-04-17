from typing import Any, Literal, TypedDict
import operator

from .exception import ValueistException

type Operator = Literal[
    "gt", ">", "lt", "<", "ge", ">=", "le", "<=", "eq", "=", "ne", "!="
]

type ParsedValue = str | int | float | bool

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
    def __init__(self, message: str | None = None) -> None:
        base_message = f"Operator not supported. Possible operators are: {','.join(_operators.keys())}"
        if message:
            base_message = f"{base_message}: ({message})"
        super().__init__(base_message)


def get_operator(operator_name: str):
    try:
        return _operators[operator_name]
    except KeyError as exception:
        raise OperatorNotSupportedError from exception
