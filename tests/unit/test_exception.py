from web_valueist.lib.exception import ValueistException, ValueNotFound, ParserError

def test_valueist_exception():
    exception = ValueistException("Test message")
    assert str(exception) == "Test message"
    assert isinstance(exception, Exception)

def test_value_not_found():
    exception = ValueNotFound()
    assert str(exception) == "Value not found"
    assert isinstance(exception, ValueistException)

def test_parser_error():
    exception = ParserError("abc", "int")
    assert exception.value == "abc"
    assert exception.parser_name == "int"
    assert str(exception) == "Could not parse 'abc' as 'int'"
    assert isinstance(exception, ValueistException)
