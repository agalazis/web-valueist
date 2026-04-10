class ValueistException(Exception):
    pass


class ValueNotFound(ValueistException):
    def __init__(self, message: str | None = None) -> None:
        base_message = "Value not found"
        if message:
            base_message = f"{base_message}: ({message})"
        super().__init__(base_message)


class ParserError(ValueistException):
    def __init__(self, value: str, parser_name: str) -> None:
        self.value = value
        self.parser_name = parser_name
        super().__init__(f"Could not parse '{value}' as '{parser_name}'")
