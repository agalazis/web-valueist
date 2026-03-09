class ValueistException(Exception):
    pass


class ValueNotFound(ValueistException):
    def __init__(self, *args: object) -> None:
        super().__init__("Value not found")
