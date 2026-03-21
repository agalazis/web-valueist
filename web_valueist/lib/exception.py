class ValueistException(Exception):
    pass


class ValueNotFound(ValueistException):
    def __init__(self, *args: object) -> None:
        super().__init__("Value not found")


class ParserError(ValueistException):
    def __init__(self, value: str, parser_name: str) -> None:
        self.value = value
        self.parser_name = parser_name
        super().__init__(f"Could not parse '{value}' as '{parser_name}'")
